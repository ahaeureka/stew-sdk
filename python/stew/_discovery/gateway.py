from __future__ import annotations

import asyncio
import json
import logging
import os
import uuid
from types import TracebackType
from typing import Callable

import grpc

from .client import DiscoveryClient
from .errors import ConflictError, DiscoveryError, NotFoundError
from .helpers import endpoint_matches_binding
from .types import Endpoint, EndpointBinding, RegistrationConfig

log = logging.getLogger(__name__)


def _blocks_registration(exc: DiscoveryError) -> bool:
    return exc.code in {
        grpc.StatusCode.UNAVAILABLE,
        grpc.StatusCode.UNAUTHENTICATED,
        grpc.StatusCode.PERMISSION_DENIED,
    }


class GatewayClient:
    """One-stop client for endpoint registration, descriptor upload, and keepalive."""

    def __init__(
        self,
        gateway_addr: str,
        *,
        app_secret: str = "",
        api_key: str = "",
        service_name: str,
        pb_path: str,
        version: str = "",
        description: str = "",
        keepalive_interval: int = 30,
        local_endpoint: Endpoint | None = None,
        endpoint_state_path: str = "",
        endpoint_protocol: str = "grpc",
        endpoint_tls_enabled: bool = False,
        descriptor_refresh_interval: int = 30,
        retry_base_delay: float = 5.0,
        retry_max_delay: float = 300.0,
        use_tls: bool = False,
        timeout: float = 10.0,
        on_registered: Callable[[], None] | None = None,
    ) -> None:
        self._client = DiscoveryClient(
            gateway_addr,
            app_secret=app_secret,
            api_key=api_key,
            use_tls=use_tls,
            timeout=timeout,
            retry_max=0,
        )
        self._service_name = service_name
        self._pb_path = pb_path
        self._version = version
        self._description = description
        self._keepalive_interval = keepalive_interval
        self._local_endpoint = local_endpoint
        self._endpoint_state_path = endpoint_state_path
        self._endpoint_protocol = endpoint_protocol
        self._endpoint_tls_enabled = endpoint_tls_enabled
        self._descriptor_refresh_interval = descriptor_refresh_interval
        self._retry_base_delay = retry_base_delay
        self._retry_max_delay = retry_max_delay
        self._on_registered = on_registered
        self._registered: asyncio.Event = asyncio.Event()
        self._retry_task: asyncio.Task[None] | None = None
        self._endpoint_binding: EndpointBinding | None = None

    @property
    def registered(self) -> asyncio.Event:
        return self._registered

    async def start(self) -> None:
        await self._client.connect()
        try:
            success = await self._register_once()
        except Exception as exc:
            log.warning(
                "initial gateway registration raised for %s: %s",
                self._service_name,
                exc,
            )
            success = False

        if success:
            self._fire_on_registered()
            log.info("gateway registration complete for %s", self._service_name)
        else:
            log.warning(
                "gateway unreachable at startup for %s; background retry task started",
                self._service_name,
            )
            self._retry_task = asyncio.create_task(
                self._retry_loop(),
                name=f"gateway-retry:{self._service_name}",
            )

    async def stop(self) -> None:
        if self._retry_task is not None:
            self._retry_task.cancel()
            self._retry_task = None
        await self._client.close()

    async def __aenter__(self) -> "GatewayClient":
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.stop()

    async def _upload_once(self) -> bool:
        active_version: str | None = None
        try:
            active_version = await self._client.get_active_version(self._service_name)
        except DiscoveryError:
            pass

        try:
            result = await self._client.upload_descriptor_from_file(
                service_name=self._service_name,
                pb_path=self._pb_path,
                version=self._version,
                description=self._description or "auto-submitted at startup",
                previous_version=active_version or "",
            )
            log.info(
                "descriptor uploaded: service=%s version=%s services=%s",
                self._service_name,
                result["applied_version"],
                result["discovered_services"],
            )
            for warning in result["compatibility_warnings"]:
                log.warning(
                    "descriptor compatibility warning [%s]: %s",
                    self._service_name,
                    warning,
                )
            return True
        except ConflictError as exc:
            log.info(
                "descriptor already up-to-date for %s: %s",
                self._service_name,
                exc,
            )
            return True
        except DiscoveryError as exc:
            if _blocks_registration(exc):
                log.warning(
                    "descriptor upload blocked registration [%s]: %s",
                    self._service_name,
                    exc,
                )
                return False
            log.warning(
                "descriptor upload non-retryable failure for %s: %s",
                self._service_name,
                exc,
            )
            return True

    def _build_registration_config(self) -> RegistrationConfig:
        return RegistrationConfig(
            endpoints=[],
            version=self._version,
            descriptor_path=self._pb_path,
        )

    def _endpoint_state_file_path(self) -> str:
        if self._endpoint_state_path:
            return os.path.abspath(self._endpoint_state_path)
        return os.path.abspath(f"{self._pb_path}.endpoint.json")

    def _load_endpoint_binding(self) -> EndpointBinding | None:
        path = self._endpoint_state_file_path()
        if not os.path.isfile(path):
            return None

        try:
            with open(path, "r", encoding="utf-8") as fh:
                payload = json.load(fh)
            return EndpointBinding(
                endpoint_id=str(payload["endpoint_id"]),
                service_name=str(payload["service_name"]),
                address=str(payload["address"]),
                port=int(payload["port"]),
                weight=int(payload.get("weight", 1)),
                protocol=str(payload.get("protocol", "grpc")),
                tls_enabled=bool(payload.get("tls_enabled", False)),
            )
        except (OSError, ValueError, KeyError, TypeError) as exc:
            log.warning("failed to load endpoint binding file %s: %s", path, exc)
            return None

    def _save_endpoint_binding(self, binding: EndpointBinding) -> None:
        path = self._endpoint_state_file_path()
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(
                {
                    "endpoint_id": binding.endpoint_id,
                    "service_name": binding.service_name,
                    "address": binding.address,
                    "port": binding.port,
                    "weight": binding.weight,
                    "protocol": binding.protocol,
                    "tls_enabled": binding.tls_enabled,
                },
                fh,
                ensure_ascii=True,
                indent=2,
            )

    def _build_endpoint_binding(self, endpoint_id: str) -> EndpointBinding:
        if self._local_endpoint is None:
            raise RuntimeError("local_endpoint is required to build an endpoint binding")

        return EndpointBinding(
            endpoint_id=endpoint_id,
            service_name=self._service_name,
            address=self._local_endpoint.address,
            port=self._local_endpoint.port,
            weight=self._local_endpoint.weight,
            protocol=self._endpoint_protocol,
            tls_enabled=self._endpoint_tls_enabled,
        )

    def _resolve_endpoint_binding(self) -> tuple[EndpointBinding | None, EndpointBinding]:
        stored = self._load_endpoint_binding()
        if stored is not None and self._local_endpoint is not None and endpoint_matches_binding(
            stored,
            service_name=self._service_name,
            endpoint=self._local_endpoint,
            protocol=self._endpoint_protocol,
            tls_enabled=self._endpoint_tls_enabled,
        ):
            return None, stored

        stale = stored
        desired = self._build_endpoint_binding(str(uuid.uuid4()))
        return stale, desired

    async def _register_endpoint_once(self) -> bool:
        if self._local_endpoint is None:
            return True
        if not await self._ensure_gateway_ready_once():
            return False

        stale_binding, desired_binding = self._resolve_endpoint_binding()
        if stale_binding is not None:
            try:
                await self._client.deregister_endpoint(
                    service_name=self._service_name,
                    endpoint_id=stale_binding.endpoint_id,
                )
                log.info(
                    "stale endpoint binding removed for %s endpoint_id=%s",
                    self._service_name,
                    stale_binding.endpoint_id,
                )
            except NotFoundError:
                pass
            except DiscoveryError as exc:
                if exc.code == grpc.StatusCode.UNAVAILABLE:
                    log.warning(
                        "gateway unreachable during endpoint deregistration [%s]: %s",
                        self._service_name,
                        exc,
                    )
                    return False
                log.warning(
                    "stale endpoint deregistration failed for %s endpoint_id=%s: %s",
                    self._service_name,
                    stale_binding.endpoint_id,
                    exc,
                )

        candidate_ids = [desired_binding.endpoint_id, str(uuid.uuid4())]

        for candidate_id in candidate_ids:
            try:
                result = await self._client.register_endpoint(
                    service_name=self._service_name,
                    endpoint=self._local_endpoint,
                    endpoint_id=candidate_id,
                    version=self._version,
                    protocol=self._endpoint_protocol,
                    tls_enabled=self._endpoint_tls_enabled,
                )
                self._endpoint_binding = self._build_endpoint_binding(result["endpoint_id"])
                self._save_endpoint_binding(self._endpoint_binding)
                log.info(
                    "endpoint registered: service=%s endpoint_id=%s endpoint=%s:%s weight=%s",
                    self._service_name,
                    self._endpoint_binding.endpoint_id,
                    self._endpoint_binding.address,
                    self._endpoint_binding.port,
                    self._endpoint_binding.weight,
                )
                return True
            except ConflictError as exc:
                log.warning(
                    "endpoint_id conflict for %s endpoint_id=%s: %s",
                    self._service_name,
                    candidate_id,
                    exc,
                )
                continue
            except DiscoveryError as exc:
                if _blocks_registration(exc):
                    log.warning(
                        "endpoint registration blocked startup [%s]: %s",
                        self._service_name,
                        exc,
                    )
                    return False
                log.warning(
                    "endpoint registration non-retryable failure for %s: %s",
                    self._service_name,
                    exc,
                )
                return True

        log.warning(
            "failed to allocate a usable endpoint_id for %s after retrying conflicts",
            self._service_name,
        )
        return True

    async def _start_descriptor_refresh_once(self) -> None:
        if self._descriptor_refresh_interval <= 0:
            return

        try:
            await self._client.start_descriptor_refresh(
                service_name=self._service_name,
                pb_path=self._pb_path,
                interval=self._descriptor_refresh_interval,
                version=self._version,
                description=self._description or "gateway client periodic descriptor refresh",
                upload_on_start=False,
            )
        except RuntimeError:
            pass

    async def _ensure_gateway_ready_once(self) -> bool:
        try:
            await self._client.wait_until_ready()
            return True
        except DiscoveryError as exc:
            if exc.code == grpc.StatusCode.UNAVAILABLE:
                log.warning(
                    "gateway not ready for %s: %s",
                    self._service_name,
                    exc,
                )
                return False
            raise

    async def _start_keepalive_once(self) -> bool:
        if not await self._ensure_gateway_ready_once():
            return False

        if self._endpoint_binding is not None:
            try:
                await self._client.start_keepalive(
                    service_name=self._service_name,
                    instance_id=self._endpoint_binding.endpoint_id,
                    interval=self._keepalive_interval,
                    registration=self._build_registration_config(),
                )
                log.info(
                    "keepalive started: service=%s endpoint_id=%s",
                    self._service_name,
                    self._endpoint_binding.endpoint_id,
                )
            except RuntimeError:
                pass
            return True

        try:
            instances = await self._client.get_instances(
                self._service_name, healthy_only=False
            )
        except DiscoveryError as exc:
            if _blocks_registration(exc):
                log.warning(
                    "instance query blocked registration [%s]: %s",
                    self._service_name,
                    exc,
                )
                return False
            log.warning(
                "failed to query instances for %s: %s",
                self._service_name,
                exc,
            )
            return True

        if not instances:
            log.debug("no instances found for %s after upload", self._service_name)
            return True

        registration = self._build_registration_config()
        for inst in instances:
            instance_id: str = inst["instance_id"]
            try:
                await self._client.start_keepalive(
                    service_name=self._service_name,
                    instance_id=instance_id,
                    interval=self._keepalive_interval,
                    registration=registration,
                )
                log.info(
                    "keepalive started: service=%s instance_id=%s",
                    self._service_name,
                    instance_id,
                )
            except RuntimeError:
                pass

        return True

    async def _register_once(self) -> bool:
        if not await self._ensure_gateway_ready_once():
            return False

        endpoint_registered = await self._register_endpoint_once()
        if not endpoint_registered:
            return False

        uploaded = await self._upload_once()
        if not uploaded:
            return False
        keepalive_started = await self._start_keepalive_once()
        if not keepalive_started:
            return False
        await self._start_descriptor_refresh_once()
        return True

    def _fire_on_registered(self) -> None:
        if self._registered.is_set():
            return
        self._registered.set()
        if self._on_registered is not None:
            try:
                self._on_registered()
            except Exception:
                log.exception("on_registered callback raised for %s", self._service_name)

    async def _retry_loop(self) -> None:
        delay = self._retry_base_delay
        attempt = 0
        while True:
            attempt += 1
            log.info(
                "gateway registration retry #%d for %s in %.0fs",
                attempt,
                self._service_name,
                delay,
            )
            await asyncio.sleep(delay)
            try:
                success = await self._register_once()
            except Exception as exc:
                log.warning(
                    "gateway registration retry #%d raised unexpectedly for %s: %s",
                    attempt,
                    self._service_name,
                    exc,
                )
                success = False

            if success:
                log.info(
                    "gateway registration succeeded for %s on retry #%d",
                    self._service_name,
                    attempt,
                )
                self._fire_on_registered()
                return

            delay = min(delay * 2, self._retry_max_delay)


__all__ = ["GatewayClient"]
"""Stew Gateway service discovery gRPC clients."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Callable

import grpc
import grpc.aio

from stew.api.v1 import service_discovery_pb2 as _pb
from stew.api.v1 import service_discovery_pb2_grpc as _grpc

from .errors import ConflictError, DiscoveryError, NotFoundError
from .helpers import AioGatewayClientBase, SyncGatewayClientBase, as_discovery_error, hash_bytes, wrap_rpc_error
from .types import DescriptorVersion, Endpoint, RegistrationConfig

log = logging.getLogger(__name__)


class DiscoveryClient(AioGatewayClientBase[_grpc.ServiceDiscoveryServiceStub]):
    """
    Async gRPC client for the Stew ServiceDiscoveryService.

    Supports:
    - Descriptor upload with optimistic locking
    - Descriptor rollback and version listing
    - Health status update and keepalive heartbeat loop
    - Service instance querying
    """

    def __init__(
        self,
        gateway_addr: str,
        *,
        app_secret: str = "",
        api_key: str = "",
        use_tls: bool = False,
        timeout: float = 10.0,
        retry_max: int = 10,
        retry_base_delay: float = 2.0,
        retry_max_delay: float = 60.0,
    ) -> None:
        super().__init__(
            gateway_addr,
            app_secret=app_secret,
            api_key=api_key,
            use_tls=use_tls,
            timeout=timeout,
        )
        self._retry_max = retry_max
        self._retry_base_delay = retry_base_delay
        self._retry_max_delay = retry_max_delay
        self._keepalive_tasks: dict[str, asyncio.Task[None]] = {}
        self._descriptor_refresh_tasks: dict[str, asyncio.Task[None]] = {}

    def _create_stub(self, channel: grpc.aio.Channel) -> _grpc.ServiceDiscoveryServiceStub:
        return _grpc.ServiceDiscoveryServiceStub(channel)

    async def connect(self) -> None:
        """Open the gRPC channel."""
        await super().connect()
        log.debug("connected to gateway %s (tls=%s)", self._addr, self._use_tls)

    async def wait_until_ready(self) -> None:
        """Block until the current channel becomes ready, or raise UNAVAILABLE."""
        if self._channel is None:
            raise RuntimeError("Client is not connected. Call connect() or use async with.")

        try:
            await asyncio.wait_for(self._channel.channel_ready(), timeout=self._timeout)
        except asyncio.TimeoutError as exc:
            raise DiscoveryError(
                f"Gateway connection timed out after {self._timeout:.1f}s",
                code=grpc.StatusCode.UNAVAILABLE,
            ) from exc

    async def close(self) -> None:
        """Cancel keepalive tasks and close the channel."""
        for task in self._keepalive_tasks.values():
            task.cancel()
        self._keepalive_tasks.clear()
        for task in self._descriptor_refresh_tasks.values():
            task.cancel()
        self._descriptor_refresh_tasks.clear()
        await super().close()

    async def _call(self, coro):  # type: ignore[no-untyped-def]
        try:
            return await coro
        except grpc.RpcError as exc:
            raise wrap_rpc_error(exc) from exc

    async def _call_with_retry(self, make_coro):  # type: ignore[no-untyped-def]
        delay = self._retry_base_delay
        for attempt in range(self._retry_max + 1):
            try:
                return await self._call(make_coro())
            except DiscoveryError as exc:
                is_unavailable = exc.code == grpc.StatusCode.UNAVAILABLE
                if not is_unavailable or attempt >= self._retry_max:
                    raise
                log.warning(
                    "gateway unavailable, retry %d/%d in %.1fs: %s",
                    attempt + 1,
                    self._retry_max,
                    delay,
                    exc,
                )
                await asyncio.sleep(delay)
                delay = min(delay * 2, self._retry_max_delay)

    async def _read_descriptor_bytes(
        self,
        *,
        descriptor_path: str = "",
        descriptor_data: bytes = b"",
    ) -> bytes:
        if descriptor_path:
            with open(descriptor_path, "rb") as fh:
                return fh.read()
        if descriptor_data:
            return descriptor_data
        raise FileNotFoundError("No descriptor file path or descriptor bytes were provided")

    async def _upload_descriptor_with_active_version(
        self,
        *,
        service_name: str,
        descriptor_data: bytes,
        version: str = "",
        description: str = "",
        force: bool = False,
    ) -> dict:
        active_version: str | None = None
        try:
            active_version = await self.get_active_version(service_name)
        except DiscoveryError:
            pass

        return await self.upload_descriptor(
            service_name=service_name,
            descriptor_data=descriptor_data,
            version=version or active_version or "",
            description=description,
            previous_version=active_version or "",
            force=force,
        )

    async def register(self, **_kwargs: object) -> str:  # type: ignore[override]
        raise PermissionError(
            "register() is an admin-only operation. "
            "Initialise services through the management frontend to obtain an app_secret, "
            "then use upload_descriptor_from_file() to submit your .pb descriptor."
        )

    async def deregister(self, **_kwargs: object) -> None:  # type: ignore[override]
        raise PermissionError(
            "deregister() is an admin-only operation. "
            "Manage service lifecycle through the management frontend."
        )

    async def register_endpoint(
        self,
        *,
        service_name: str,
        endpoint: Endpoint,
        endpoint_id: str = "",
        version: str = "",
        protocol: str = "grpc",
        tls_enabled: bool = False,
        protobuf_descriptor: bytes = b"",
    ) -> dict:
        resolved_endpoint_id = endpoint_id
        resolved_version = version
        resolved_protocol = protocol
        resolved_tls_enabled = tls_enabled

        if not resolved_endpoint_id:
            existing_instance = await self._find_existing_endpoint_instance(
                service_name=service_name,
                endpoint=endpoint,
                protocol=protocol,
                tls_enabled=tls_enabled,
            )
            if existing_instance is not None:
                resolved_endpoint_id = existing_instance["instance_id"]
                if not resolved_version:
                    resolved_version = existing_instance["version"]
                if resolved_protocol == "grpc" and existing_instance["protocol"]:
                    resolved_protocol = existing_instance["protocol"]
                if not resolved_tls_enabled:
                    resolved_tls_enabled = bool(existing_instance["tls_enabled"])
                log.info(
                    "reusing existing endpoint configuration for %s endpoint_id=%s",
                    service_name,
                    resolved_endpoint_id,
                )

        req = _pb.RegisterServiceEndpointRequest(
            service_name=service_name,
            endpoint_id=resolved_endpoint_id,
            endpoint=_pb.Endpoint(
                address=endpoint.address,
                port=endpoint.port,
                weight=endpoint.weight,
            ),
            version=resolved_version,
            protocol=resolved_protocol,
            tls_enabled=resolved_tls_enabled,
            protobuf_descriptor=protobuf_descriptor,
        )
        resp: _pb.RegisterServiceEndpointResponse = await self._call_with_retry(  # type: ignore[assignment]
            lambda: self._s.RegisterServiceEndpoint(req, metadata=self._meta(), timeout=self._timeout)
        )
        if not resp.success:
            raise DiscoveryError(f"Endpoint registration rejected: {resp.message}")

        registered = resp.registered_service
        return {
            "endpoint_id": resp.endpoint_id,
            "instance_id": registered.instance_id or resp.endpoint_id,
            "lease_id": resp.lease_id,
            "service_name": registered.service_name or service_name,
            "version": registered.version,
            "protocol": registered.protocol,
            "tls_enabled": registered.tls_enabled,
            "endpoints": [
                {"address": ep.address, "port": ep.port, "weight": ep.weight}
                for ep in (registered.lb.endpoints if registered.HasField("lb") else [])
            ],
        }

    async def deregister_endpoint(
        self,
        *,
        service_name: str,
        endpoint_id: str,
    ) -> None:
        req = _pb.DeregisterServiceEndpointRequest(
            service_name=service_name,
            endpoint_id=endpoint_id,
        )
        resp: _pb.DeregisterServiceEndpointResponse = await self._call_with_retry(  # type: ignore[assignment]
            lambda: self._s.DeregisterServiceEndpoint(req, metadata=self._meta(), timeout=self._timeout)
        )
        if not resp.success:
            raise DiscoveryError(f"Endpoint deregistration rejected: {resp.message}")

    async def heartbeat(
        self,
        *,
        service_name: str,
        instance_id: str,
        status: int = _pb.SERVICE_STATUS_HEALTHY,
        message: str = "",
    ) -> None:
        req = _pb.UpdateServiceHealthRequest(
            service_name=service_name,
            instance_id=instance_id,
            status=_pb.ServiceStatus.Name(status),
            health_message=message,
        )
        resp: _pb.UpdateServiceHealthResponse = await self._call_with_retry(  # type: ignore[assignment]
            lambda: self._s.UpdateServiceHealth(req, metadata=self._meta(), timeout=self._timeout)
        )
        if not resp.success:
            raise DiscoveryError(f"Health update failed: {resp.message}")

    async def start_keepalive(
        self,
        *,
        service_name: str,
        instance_id: str,
        interval: int = 30,
        on_error: Callable[[DiscoveryError], None] | None = None,
        registration: RegistrationConfig | None = None,
    ) -> None:
        key = f"{service_name}:{instance_id}"
        if key in self._keepalive_tasks:
            raise RuntimeError(f"Keepalive already running for {key}")

        async def _send_heartbeat_once() -> None:
            req = _pb.UpdateServiceHealthRequest(
                service_name=service_name,
                instance_id=instance_id,
                status=_pb.ServiceStatus.Name(_pb.SERVICE_STATUS_HEALTHY),
            )
            resp: _pb.UpdateServiceHealthResponse = await self._call(  # type: ignore[assignment]
                self._s.UpdateServiceHealth(req, metadata=self._meta(), timeout=self._timeout)
            )
            if not resp.success:
                raise DiscoveryError(f"Health update failed: {resp.message}")

        def _report_error(exc: DiscoveryError) -> None:
            if on_error is None:
                return
            try:
                on_error(exc)
            except Exception:
                log.exception("keepalive on_error callback raised for %s", key)

        async def _refresh_descriptor() -> None:
            assert registration is not None
            descriptor_bytes = await self._read_descriptor_bytes(
                descriptor_path=registration.descriptor_path,
                descriptor_data=registration.descriptor_data,
            )

            result = await self._upload_descriptor_with_active_version(
                service_name=service_name,
                descriptor_data=descriptor_bytes,
                version=registration.version,
                description="keepalive recovery descriptor refresh",
            )
            log.info(
                "keepalive: descriptor refreshed for %s (version=%s)",
                key,
                result["applied_version"],
            )

        async def _recover_until_success(initial_exc: Exception) -> None:
            delay = self._retry_base_delay
            current_error = as_discovery_error(initial_exc)

            while True:
                log.warning("keepalive recovery for %s: %s", key, current_error)
                _report_error(current_error)
                try:
                    await self.wait_until_ready()
                    if registration is not None:
                        await _refresh_descriptor()
                    await _send_heartbeat_once()
                    log.info("keepalive recovered for %s", key)
                    return
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    current_error = as_discovery_error(exc)
                    log.warning(
                        "keepalive recovery retry for %s in %.1fs: %s",
                        key,
                        delay,
                        current_error,
                    )
                    await asyncio.sleep(delay)
                    delay = min(delay * 2, self._retry_max_delay)

        async def _loop() -> None:
            while True:
                try:
                    await _send_heartbeat_once()
                    log.debug("keepalive sent for %s", key)
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    await _recover_until_success(exc)
                await asyncio.sleep(interval)

        task = asyncio.create_task(_loop(), name=f"keepalive:{key}")
        self._keepalive_tasks[key] = task
        log.info("keepalive started for %s (interval=%ds, auto_recovery=%s)", key, interval, registration is not None)

    def stop_keepalive(self, *, service_name: str, instance_id: str) -> None:
        key = f"{service_name}:{instance_id}"
        task = self._keepalive_tasks.pop(key, None)
        if task:
            task.cancel()
            log.info("keepalive stopped for %s", key)

    async def refresh_descriptor_from_file(
        self,
        *,
        service_name: str,
        pb_path: str,
        version: str = "",
        description: str = "",
        force: bool = False,
    ) -> dict:
        with open(pb_path, "rb") as fh:
            descriptor_data = fh.read()

        return await self._upload_descriptor_with_active_version(
            service_name=service_name,
            descriptor_data=descriptor_data,
            version=version,
            description=description or "descriptor refresh from file",
            force=force,
        )

    async def start_descriptor_refresh(
        self,
        *,
        service_name: str,
        pb_path: str,
        interval: int = 30,
        version: str = "",
        description: str = "",
        force: bool = False,
        upload_on_start: bool = False,
        on_error: Callable[[DiscoveryError], None] | None = None,
    ) -> None:
        key = f"{service_name}:{os.path.abspath(pb_path)}"
        if key in self._descriptor_refresh_tasks:
            raise RuntimeError(f"Descriptor refresh already running for {key}")

        def _report_error(exc: DiscoveryError) -> None:
            if on_error is None:
                return
            try:
                on_error(exc)
            except Exception:
                log.exception("descriptor refresh on_error callback raised for %s", key)

        async def _sync_descriptor(last_uploaded_hash: str | None) -> str | None:
            try:
                current_bytes = await self._read_descriptor_bytes(descriptor_path=pb_path)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                error = as_discovery_error(exc)
                _report_error(error)
                log.warning("descriptor refresh read failed for %s: %s", key, error)
                return last_uploaded_hash

            current_hash = hash_bytes(current_bytes)
            if current_hash == last_uploaded_hash:
                return last_uploaded_hash

            delay = self._retry_base_delay
            while True:
                try:
                    current_bytes = await self._read_descriptor_bytes(descriptor_path=pb_path)
                    current_hash = hash_bytes(current_bytes)
                    if current_hash == last_uploaded_hash:
                        return last_uploaded_hash

                    await self.wait_until_ready()
                    result = await self.refresh_descriptor_from_file(
                        service_name=service_name,
                        pb_path=pb_path,
                        version=version,
                        description=description or "periodic descriptor refresh",
                        force=force,
                    )
                    log.info(
                        "descriptor refresh applied for %s (version=%s)",
                        key,
                        result["applied_version"],
                    )
                    return current_hash
                except ConflictError as exc:
                    log.info("descriptor refresh conflict for %s: %s", key, exc)
                    return current_hash
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    error = as_discovery_error(exc)
                    _report_error(error)
                    log.warning(
                        "descriptor refresh retry for %s in %.1fs: %s",
                        key,
                        delay,
                        error,
                    )
                    await asyncio.sleep(delay)
                    delay = min(delay * 2, self._retry_max_delay)

        async def _loop() -> None:
            last_uploaded_hash: str | None = None
            if not upload_on_start:
                try:
                    initial_bytes = await self._read_descriptor_bytes(descriptor_path=pb_path)
                    last_uploaded_hash = hash_bytes(initial_bytes)
                except FileNotFoundError:
                    last_uploaded_hash = None

            while True:
                if upload_on_start and last_uploaded_hash is None:
                    last_uploaded_hash = await _sync_descriptor(last_uploaded_hash)
                await asyncio.sleep(interval)
                last_uploaded_hash = await _sync_descriptor(last_uploaded_hash)

        task = asyncio.create_task(_loop(), name=f"descriptor-refresh:{key}")
        self._descriptor_refresh_tasks[key] = task
        log.info("descriptor refresh started for %s (interval=%ds)", key, interval)

    def stop_descriptor_refresh(self, *, service_name: str, pb_path: str) -> None:
        key = f"{service_name}:{os.path.abspath(pb_path)}"
        task = self._descriptor_refresh_tasks.pop(key, None)
        if task:
            task.cancel()
            log.info("descriptor refresh stopped for %s", key)

    async def upload_descriptor(
        self,
        *,
        service_name: str,
        descriptor_data: bytes,
        version: str = "",
        description: str = "",
        previous_version: str = "",
        force: bool = False,
    ) -> dict:
        hash_hex = hash_bytes(descriptor_data)[:12]
        effective_version = version or f"{int(time.time())}-{hash_hex}"

        req = _pb.UploadProtobufDescriptorRequest(
            service_name=service_name,
            descriptor_data=descriptor_data,
            descriptor_version=effective_version,
            description=description or f"auto-submitted hash={hash_hex}",
            force=force,
            previous_version=previous_version,
        )
        resp: _pb.UploadProtobufDescriptorResponse = await self._call(
            self._s.UploadProtobufDescriptor(req, metadata=self._meta(), timeout=self._timeout)
        )
        if not resp.success:
            raise DiscoveryError(f"Descriptor upload rejected: {resp.message}")
        if resp.compatibility_warnings:
            for warning in resp.compatibility_warnings:
                log.warning("descriptor compat warning [%s]: %s", service_name, warning)
        log.info(
            "descriptor uploaded service_name=%s version=%s hash=...%s",
            service_name,
            resp.applied_version,
            hash_hex,
        )
        return {
            "applied_version": resp.applied_version,
            "discovered_services": list(resp.discovered_services),
            "compatibility_warnings": list(resp.compatibility_warnings),
            "descriptor_hash": resp.descriptor_hash,
        }

    async def upload_descriptor_from_file(
        self,
        *,
        service_name: str,
        pb_path: str,
        version: str = "",
        description: str = "",
        previous_version: str = "",
        force: bool = False,
    ) -> dict:
        with open(pb_path, "rb") as fh:
            data = fh.read()
        return await self.upload_descriptor(
            service_name=service_name,
            descriptor_data=data,
            version=version,
            description=description,
            previous_version=previous_version,
            force=force,
        )

    async def rollback_descriptor(
        self,
        *,
        service_name: str,
        target_version: str,
    ) -> str:
        req = _pb.RollbackDescriptorRequest(
            service_name=service_name,
            target_version=target_version,
        )
        resp: _pb.RollbackDescriptorResponse = await self._call(
            self._s.RollbackDescriptor(req, metadata=self._meta(), timeout=self._timeout)
        )
        if not resp.success:
            raise DiscoveryError(f"Rollback failed: {resp.message}")
        log.info(
            "descriptor rolled back service_name=%s active_version=%s",
            service_name,
            resp.active_version,
        )
        return resp.active_version

    async def list_descriptor_versions(self, service_name: str) -> list[DescriptorVersion]:
        req = _pb.ListDescriptorVersionsRequest(service_name=service_name)
        resp: _pb.ListDescriptorVersionsResponse = await self._call(
            self._s.ListDescriptorVersions(req, metadata=self._meta(), timeout=self._timeout)
        )
        return [
            DescriptorVersion(
                version=version.version,
                descriptor_hash=version.descriptor_hash,
                description=version.description,
                services=list(version.services),
                size_bytes=version.size_bytes,
                is_active=version.is_active,
                created_at=str(version.created_at),
            )
            for version in resp.versions
        ]

    async def get_active_version(self, service_name: str) -> str | None:
        try:
            versions = await self.list_descriptor_versions(service_name)
        except NotFoundError:
            return None
        for version in versions:
            if version.is_active:
                return version.version
        return None

    async def list_services(
        self,
        *,
        name_prefix: str = "",
        tag_filters: dict[str, str] | None = None,
    ) -> list[dict]:
        req = _pb.ListServicesRequest(
            name_prefix=name_prefix,
            tag_filters=tag_filters or {},
        )
        resp: _pb.ListServicesResponse = await self._call(
            self._s.ListServices(req, metadata=self._meta(), timeout=self._timeout)
        )
        return [
            {
                "service_name": svc.service_name,
                "instance_id": svc.instance_id,
                "version": svc.version,
                "status": svc.status,
                "protocol": svc.protocol,
                "endpoints": [
                    {"address": ep.address, "port": ep.port, "weight": ep.weight}
                    for ep in (svc.lb.endpoints if svc.lb else [])
                ],
            }
            for svc in (resp.services or [])
        ]

    async def get_instances(
        self,
        service_name: str,
        *,
        healthy_only: bool = True,
        tag_filters: dict[str, str] | None = None,
    ) -> list[dict]:
        req = _pb.GetServiceInstancesRequest(
            service_name=service_name,
            healthy_only=healthy_only,
            tag_filters=tag_filters or {},
        )
        resp: _pb.GetServiceInstancesResponse = await self._call(
            self._s.GetServiceInstances(req, metadata=self._meta(), timeout=self._timeout)
        )
        return [self._service_instance_to_dict(inst) for inst in resp.instances]

    async def _find_existing_endpoint_instance(
        self,
        *,
        service_name: str,
        endpoint: Endpoint,
        protocol: str,
        tls_enabled: bool,
    ) -> dict | None:
        try:
            instances = await self.get_instances(service_name, healthy_only=False)
        except DiscoveryError as exc:
            log.debug(
                "failed to query existing instances before endpoint registration [%s]: %s",
                service_name,
                exc,
            )
            return None

        address_matches = [
            inst
            for inst in instances
            if any(
                existing["address"] == endpoint.address and existing["port"] == endpoint.port
                for existing in inst["endpoints"]
            )
        ]
        if not address_matches:
            return None

        exact_matches = [
            inst
            for inst in address_matches
            if inst["protocol"] == protocol and bool(inst["tls_enabled"]) == tls_enabled
        ]
        if exact_matches:
            return exact_matches[0]

        if len(address_matches) == 1:
            return address_matches[0]

        log.debug(
            "multiple endpoint candidates found for %s %s:%s; skipping automatic reuse",
            service_name,
            endpoint.address,
            endpoint.port,
        )
        return None

    @staticmethod
    def _service_instance_to_dict(inst: _pb.ServiceInstance) -> dict:
        return {
            "service_name": inst.service_name,
            "instance_id": inst.instance_id,
            "version": inst.version,
            "protocol": inst.protocol,
            "tls_enabled": inst.tls_enabled,
            "tags": dict(inst.tags),
            "status": _pb.ServiceStatus.Name(inst.status),
            "endpoints": [
                {"address": endpoint.address, "port": endpoint.port, "weight": endpoint.weight}
                for endpoint in (inst.lb.endpoints if inst.HasField("lb") else [])
            ],
        }


class SyncDiscoveryClient(SyncGatewayClientBase[DiscoveryClient]):
    """Synchronous facade over :class:`DiscoveryClient`."""

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        super().__init__(DiscoveryClient, *args, **kwargs)

    def heartbeat(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
        self._run(self._client.heartbeat(**kwargs))

    def upload_descriptor(self, **kwargs) -> dict:  # type: ignore[no-untyped-def]
        return self._run(self._client.upload_descriptor(**kwargs))

    def upload_descriptor_from_file(self, **kwargs) -> dict:  # type: ignore[no-untyped-def]
        return self._run(self._client.upload_descriptor_from_file(**kwargs))

    def refresh_descriptor_from_file(self, **kwargs) -> dict:  # type: ignore[no-untyped-def]
        return self._run(self._client.refresh_descriptor_from_file(**kwargs))

    def register_endpoint(self, **kwargs) -> dict:  # type: ignore[no-untyped-def]
        return self._run(self._client.register_endpoint(**kwargs))

    def deregister_endpoint(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
        self._run(self._client.deregister_endpoint(**kwargs))

    def rollback_descriptor(self, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self._run(self._client.rollback_descriptor(**kwargs))

    def list_descriptor_versions(self, service_name: str) -> list[DescriptorVersion]:
        return self._run(self._client.list_descriptor_versions(service_name))

    def get_active_version(self, service_name: str) -> str | None:
        return self._run(self._client.get_active_version(service_name))

    def get_instances(self, service_name: str, **kwargs) -> list[dict]:  # type: ignore[no-untyped-def]
        return self._run(self._client.get_instances(service_name, **kwargs))

    def list_services(self, **kwargs) -> list[dict]:  # type: ignore[no-untyped-def]
        return self._run(self._client.list_services(**kwargs))


__all__ = ["DiscoveryClient", "SyncDiscoveryClient"]
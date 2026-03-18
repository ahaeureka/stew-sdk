"""
Stew Gateway — Service Discovery gRPC Client SDK

Provides a high-level client for service registration, health management,
descriptor submission, and version management against the Stew gateway.

Usage:
    from stew.discovery_client import DiscoveryClient, Endpoint, BalanceType

    async with DiscoveryClient("127.0.0.1:3012", api_key="svc_xxx") as client:
        instance_id = await client.register(
            service_name="stew.api.v1.OrderService",
            endpoints=[Endpoint("10.0.0.5", 50051)],
        )
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from enum import IntEnum
from types import TracebackType
from typing import AsyncIterator, Sequence

import grpc
import grpc.aio

from stew.api.v1 import service_discovery_pb2 as _pb
from stew.api.v1 import service_discovery_pb2_grpc as _grpc

# Re-export proto-generated sub-message types as public SDK types.
# Users can construct them with the same keyword arguments documented in
# the .pyi stubs without needing an extra wrapper layer.
CorsConfig = _pb.ServiceCorsConfig
RiskRuleConfig = _pb.ServiceRiskRuleConfig
RiskConfig = _pb.ServiceRiskConfig
TurnstileConfig = _pb.ServiceTurnstileConfig

__all__ = [
    "DiscoveryClient",
    "Endpoint",
    "BalanceType",
    "HealthCheckConfig",
    "MiddlewareConfig",
    "CorsConfig",
    "RiskRuleConfig",
    "RiskConfig",
    "TurnstileConfig",
    "DescriptorVersion",
    "DiscoveryError",
    "ConflictError",
    "NotFoundError",
]

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Public data structures
# ---------------------------------------------------------------------------


class BalanceType(IntEnum):
    ROUND_ROBIN = 1
    WEIGHTED_ROUND_ROBIN = 2
    CONSISTENT_HASH = 3
    LEAST_CONNECTIONS = 4
    SED = 5
    WEIGHTED_LEAST_CONNECTIONS = 6
    NEVER_QUEUE = 7


@dataclass
class Endpoint:
    """Single backend endpoint."""
    address: str
    port: int
    weight: int = 1


@dataclass
class HealthCheckConfig:
    """Active health check configuration."""
    enabled: bool = True
    grpc_method: str = ""
    http_path: str = ""
    interval_seconds: int = 30
    timeout_seconds: int = 5
    healthy_threshold: int = 2
    unhealthy_threshold: int = 3


@dataclass
class MiddlewareConfig:
    """Per-service middleware switches."""
    rate_limit_enabled: bool = True
    rate_limit_rpm: int = 0
    rate_limit_user_rpm: int = 0
    cors_enabled: bool = False
    cors: CorsConfig | None = None
    risk_enabled: bool = False
    risk: RiskConfig | None = None
    turnstile_enabled: bool = False
    turnstile: TurnstileConfig | None = None


@dataclass
class DescriptorVersion:
    """Descriptor version metadata returned by list_descriptor_versions."""
    version: str
    descriptor_hash: str
    description: str
    services: list[str]
    size_bytes: int
    is_active: bool
    created_at: str  # RFC3339 string


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class DiscoveryError(Exception):
    """Base exception for all discovery client errors."""
    def __init__(self, message: str, code: grpc.StatusCode | None = None) -> None:
        super().__init__(message)
        self.code = code


class ConflictError(DiscoveryError):
    """Raised when an optimistic lock check fails (FAILED_PRECONDITION)."""


class NotFoundError(DiscoveryError):
    """Raised when a resource is not found (NOT_FOUND)."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _make_metadata(api_key: str) -> list[tuple[str, str]]:
    if api_key:
        return [("x-api-key", api_key)]
    return []


def _to_proto_lb(
    endpoints: Sequence[Endpoint],
    balance_type: BalanceType,
) -> _pb.LoadBalancer:
    return _pb.LoadBalancer(
        type=f"BALANCE_TYPE_{balance_type.name}",
        endpoints=[
            _pb.Endpoint(address=ep.address, port=ep.port, weight=ep.weight)
            for ep in endpoints
        ],
    )


def _to_proto_hc(cfg: HealthCheckConfig | None) -> _pb.HealthCheckConfig | None:
    if cfg is None:
        return None
    return _pb.HealthCheckConfig(
        enabled=cfg.enabled,
        grpc_method=cfg.grpc_method,
        http_path=cfg.http_path,
        interval_seconds=cfg.interval_seconds,
        timeout_seconds=cfg.timeout_seconds,
        healthy_threshold=cfg.healthy_threshold,
        unhealthy_threshold=cfg.unhealthy_threshold,
    )


def _to_proto_mw(cfg: MiddlewareConfig | None) -> _pb.ServiceMiddlewareConfig | None:
    if cfg is None:
        return None
    kwargs: dict = dict(
        rate_limit_enabled=cfg.rate_limit_enabled,
        rate_limit_rpm=cfg.rate_limit_rpm,
        rate_limit_user_rpm=cfg.rate_limit_user_rpm,
        cors_enabled=cfg.cors_enabled,
        risk_enabled=cfg.risk_enabled,
        turnstile_enabled=cfg.turnstile_enabled,
    )
    if cfg.cors is not None:
        kwargs["cors"] = cfg.cors
    if cfg.risk is not None:
        kwargs["risk"] = cfg.risk
    if cfg.turnstile is not None:
        kwargs["turnstile"] = cfg.turnstile
    return _pb.ServiceMiddlewareConfig(**kwargs)


def _wrap_rpc_error(exc: grpc.RpcError) -> DiscoveryError:
    code: grpc.StatusCode = exc.code()  # type: ignore[attr-defined]
    detail: str = exc.details() or ""  # type: ignore[attr-defined]
    if code == grpc.StatusCode.NOT_FOUND:
        return NotFoundError(detail, code=code)
    if code == grpc.StatusCode.FAILED_PRECONDITION:
        return ConflictError(detail, code=code)
    return DiscoveryError(f"[{code.name}] {detail}", code=code)


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


class DiscoveryClient:
    """
    Async gRPC client for the Stew ServiceDiscoveryService.

    Supports:
    - Service registration & deregistration
    - Keepalive heartbeat loop
    - Descriptor upload with optimistic locking
    - Descriptor rollback & version listing
    - Health status update

    Example::

        async with DiscoveryClient("127.0.0.1:3012", api_key="svc_xxx") as c:
            instance_id = await c.register(
                service_name="stew.api.v1.MyService",
                endpoints=[Endpoint("10.0.0.5", 50051)],
            )
            await c.start_keepalive(
                service_name="stew.api.v1.MyService",
                instance_id=instance_id,
            )
    """

    def __init__(
        self,
        gateway_addr: str,
        *,
        api_key: str = "",
        use_tls: bool = False,
        timeout: float = 10.0,
    ) -> None:
        """
        Parameters
        ----------
        gateway_addr:
            Host:port of the Stew gateway gRPC endpoint, e.g. ``127.0.0.1:3012``.
        api_key:
            Service API key.  Falls back to env var ``SERVICE_API_KEY``.
        use_tls:
            Connect over TLS.
        timeout:
            Default RPC deadline in seconds.
        """
        self._addr = gateway_addr
        self._api_key = api_key or os.environ.get("SERVICE_API_KEY", "")
        self._use_tls = use_tls
        self._timeout = timeout
        self._channel: grpc.aio.Channel | None = None
        self._stub: _grpc.ServiceDiscoveryServiceStub | None = None
        self._keepalive_tasks: dict[str, asyncio.Task[None]] = {}

    # ------------------------------------------------------------------
    # Context manager / lifecycle
    # ------------------------------------------------------------------

    async def connect(self) -> None:
        """Open the gRPC channel."""
        if self._use_tls:
            credentials = grpc.ssl_channel_credentials()
            self._channel = grpc.aio.secure_channel(self._addr, credentials)
        else:
            self._channel = grpc.aio.insecure_channel(self._addr)
        self._stub = _grpc.ServiceDiscoveryServiceStub(self._channel)
        log.debug("connected to gateway %s (tls=%s)", self._addr, self._use_tls)

    async def close(self) -> None:
        """Cancel keepalive tasks and close the channel."""
        for task in self._keepalive_tasks.values():
            task.cancel()
        self._keepalive_tasks.clear()
        if self._channel:
            await self._channel.close()
            self._channel = None
        self._stub = None

    async def __aenter__(self) -> "DiscoveryClient":
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @property
    def _s(self) -> _grpc.ServiceDiscoveryServiceStub:
        if self._stub is None:
            raise RuntimeError("Client is not connected. Call connect() or use async with.")
        return self._stub

    def _meta(self) -> list[tuple[str, str]]:
        return _make_metadata(self._api_key)

    async def _call(self, coro):  # type: ignore[no-untyped-def]
        try:
            return await coro
        except grpc.RpcError as exc:
            raise _wrap_rpc_error(exc) from exc

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    async def register(
        self,
        *,
        service_name: str,
        endpoints: Sequence[Endpoint],
        instance_id: str = "",
        version: str = "1.0.0",
        balance_type: BalanceType = BalanceType.ROUND_ROBIN,
        tags: dict[str, str] | None = None,
        protocol: str = "grpc",
        tls_enabled: bool = False,
        ttl: int = 60,
        health_check: HealthCheckConfig | None = None,
        middleware: MiddlewareConfig | None = None,
        descriptor_data: bytes | None = None,
        metadata: dict | None = None,
    ) -> str:
        """
        Register a service instance with the gateway.

        Parameters
        ----------
        service_name:
            Fully-qualified service name, e.g. ``stew.api.v1.OrderService``.
        endpoints:
            One or more backend endpoints.
        instance_id:
            Unique instance ID.  Auto-generated by the gateway if empty.
        version:
            Service version string.
        balance_type:
            Load balancing algorithm.
        tags:
            Arbitrary string key/value tags for routing and filtering.
        protocol:
            ``"grpc"`` (default) or ``"http"``.
        tls_enabled:
            Whether the backend endpoint uses TLS.
        ttl:
            Registration TTL in seconds.  Must be renewed via :meth:`heartbeat`.
        health_check:
            Active health check configuration.
        middleware:
            Per-service middleware switches.
        descriptor_data:
            Compiled ``.pb`` binary.  If provided the gateway loads routes immediately.
        metadata:
            Arbitrary key/value metadata stored alongside the instance.

        Returns
        -------
        str
            The ``instance_id`` assigned to this registration.

        Raises
        ------
        DiscoveryError
            On any gRPC error.
        """
        lb = _to_proto_lb(endpoints, balance_type)
        hc = _to_proto_hc(health_check)
        mw = _to_proto_mw(middleware)

        instance_kwargs: dict = dict(
            service_name=service_name,
            instance_id=instance_id,
            lb=lb,
            version=version,
            tags=tags or {},
            protocol=protocol,
            tls_enabled=tls_enabled,
            weight=max(ep.weight for ep in endpoints) if endpoints else 1,
            status=_pb.SERVICE_STATUS_HEALTHY,
        )
        if hc is not None:
            instance_kwargs["health_check_config"] = hc
        if mw is not None:
            instance_kwargs["middleware_config"] = mw
        if descriptor_data:
            instance_kwargs["protobuf_descriptor"] = descriptor_data

        req = _pb.RegisterServiceRequest(
            service=_pb.ServiceInstance(**instance_kwargs),
            ttl=ttl,
        )
        resp: _pb.RegisterServiceResponse = await self._call(
            self._s.RegisterService(req, metadata=self._meta(), timeout=self._timeout)
        )
        if not resp.success:
            raise DiscoveryError(f"Registration failed: {resp.message}")
        # Prefer the explicit instance_id echoed back by the server (field 4).
        # Fall back to the caller-supplied id, then to the legacy behaviour of
        # parsing resp.message (which embeds the id as human-readable text and
        # is therefore fragile).
        assigned_id = resp.instance_id or instance_id
        if not assigned_id:
            # Last-resort fallback for old gateway versions without field 4.
            assigned_id = instance_id or resp.message
        log.info(
            "registered service_name=%s instance_id=%s lease_id=%s",
            service_name,
            instance_id or "(auto)",
            resp.lease_id,
        )
        return assigned_id

    async def deregister(self, *, service_name: str, instance_id: str) -> None:
        """
        Deregister a service instance.

        Parameters
        ----------
        service_name:
            Fully-qualified service name.
        instance_id:
            Instance ID returned by :meth:`register`.

        Raises
        ------
        DiscoveryError
            On any gRPC error.
        """
        req = _pb.DeregisterServiceRequest(
            service_name=service_name,
            instance_id=instance_id,
        )
        resp: _pb.DeregisterServiceResponse = await self._call(
            self._s.DeregisterService(req, metadata=self._meta(), timeout=self._timeout)
        )
        if not resp.success:
            raise DiscoveryError(f"Deregistration failed: {resp.message}")
        log.info("deregistered service_name=%s instance_id=%s", service_name, instance_id)

    # ------------------------------------------------------------------
    # Health / keepalive
    # ------------------------------------------------------------------

    async def heartbeat(
        self,
        *,
        service_name: str,
        instance_id: str,
        status: str = "SERVICE_STATUS_HEALTHY",
        message: str = "",
    ) -> None:
        """
        Send a single health update (keepalive tick).

        Parameters
        ----------
        service_name:
            Fully-qualified service name.
        instance_id:
            Instance ID.
        status:
            One of ``SERVICE_STATUS_HEALTHY``, ``SERVICE_STATUS_UNHEALTHY``,
            ``SERVICE_STATUS_MAINTENANCE``, ``SERVICE_STATUS_DRAINING``.
        message:
            Optional human-readable status message.

        Raises
        ------
        DiscoveryError
            On any gRPC error.
        """
        req = _pb.UpdateServiceHealthRequest(
            service_name=service_name,
            instance_id=instance_id,
            status=status,
            health_message=message,
        )
        resp: _pb.UpdateServiceHealthResponse = await self._call(
            self._s.UpdateServiceHealth(req, metadata=self._meta(), timeout=self._timeout)
        )
        if not resp.success:
            raise DiscoveryError(f"Health update failed: {resp.message}")

    async def start_keepalive(
        self,
        *,
        service_name: str,
        instance_id: str,
        interval: int = 30,
        on_error: None = None,
    ) -> None:
        """
        Start a background keepalive loop for this instance.

        Sends a heartbeat every ``interval`` seconds.  The loop runs as a
        background ``asyncio.Task`` and is cancelled automatically when the
        client is closed.

        Parameters
        ----------
        service_name:
            Fully-qualified service name.
        instance_id:
            Instance ID.
        interval:
            Heartbeat interval in seconds.  Should be less than the TTL used
            during registration (default TTL is 60 s, recommended interval ≤ 30 s).

        Raises
        ------
        RuntimeError
            If a keepalive loop is already running for this instance.
        """
        key = f"{service_name}:{instance_id}"
        if key in self._keepalive_tasks:
            raise RuntimeError(f"Keepalive already running for {key}")

        async def _loop() -> None:
            while True:
                await asyncio.sleep(interval)
                try:
                    await self.heartbeat(
                        service_name=service_name,
                        instance_id=instance_id,
                    )
                    log.debug("keepalive sent for %s", key)
                except DiscoveryError as exc:
                    log.warning("keepalive failed for %s: %s", key, exc)

        task = asyncio.create_task(_loop(), name=f"keepalive:{key}")
        self._keepalive_tasks[key] = task
        log.info("keepalive started for %s (interval=%ds)", key, interval)

    def stop_keepalive(self, *, service_name: str, instance_id: str) -> None:
        """Cancel the keepalive loop for a specific instance."""
        key = f"{service_name}:{instance_id}"
        task = self._keepalive_tasks.pop(key, None)
        if task:
            task.cancel()
            log.info("keepalive stopped for %s", key)

    # ------------------------------------------------------------------
    # Descriptor management
    # ------------------------------------------------------------------

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
        """
        Upload a compiled ``.pb`` descriptor to the gateway.

        The gateway validates the descriptor, stores it with versioning, and
        triggers hot-reload of the gRPC routing table.

        Parameters
        ----------
        service_name:
            Fully-qualified service name corresponding to the descriptor.
        descriptor_data:
            Raw binary content of the compiled ``.pb`` file.
        version:
            Explicit version string.  Auto-generated as
            ``{timestamp}-{hash_prefix}`` if empty.
        description:
            Human-readable version note.
        previous_version:
            Current active version for optimistic locking.  If the active
            version on the gateway differs, the request is rejected with
            :class:`ConflictError`.
        force:
            Ignore compatibility warnings and force the update.

        Returns
        -------
        dict
            ``{"applied_version": str, "discovered_services": list[str],
               "compatibility_warnings": list[str], "descriptor_hash": str}``

        Raises
        ------
        ConflictError
            If optimistic lock check fails.
        DiscoveryError
            On validation failure or other gRPC error.
        """
        hash_hex = hashlib.sha256(descriptor_data).hexdigest()[:12]
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
            for w in resp.compatibility_warnings:
                log.warning("descriptor compat warning [%s]: %s", service_name, w)
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
        """
        Convenience wrapper: read a ``.pb`` file and call :meth:`upload_descriptor`.

        Parameters
        ----------
        pb_path:
            Filesystem path to the compiled ``.pb`` file.

        All other parameters are forwarded to :meth:`upload_descriptor`.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        """
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
        """
        Rollback to a previously stored descriptor version.

        Parameters
        ----------
        service_name:
            Fully-qualified service name.
        target_version:
            Version string to activate.

        Returns
        -------
        str
            The active version after rollback (equals ``target_version`` on success).

        Raises
        ------
        NotFoundError
            If the target version does not exist.
        DiscoveryError
            On other gRPC errors.
        """
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
        """
        List all stored descriptor versions for a service.

        Parameters
        ----------
        service_name:
            Fully-qualified service name.

        Returns
        -------
        list[DescriptorVersion]
            Versions sorted by creation time (newest first).  The active
            version has ``is_active=True``.

        Raises
        ------
        DiscoveryError
            On any gRPC error.
        """
        req = _pb.ListDescriptorVersionsRequest(service_name=service_name)
        resp: _pb.ListDescriptorVersionsResponse = await self._call(
            self._s.ListDescriptorVersions(req, metadata=self._meta(), timeout=self._timeout)
        )
        return [
            DescriptorVersion(
                version=v.version,
                descriptor_hash=v.descriptor_hash,
                description=v.description,
                services=list(v.services),
                size_bytes=v.size_bytes,
                is_active=v.is_active,
                created_at=str(v.created_at),
            )
            for v in resp.versions
        ]

    async def get_active_version(self, service_name: str) -> str | None:
        """
        Return the currently active descriptor version, or ``None`` if none exists.

        Parameters
        ----------
        service_name:
            Fully-qualified service name.
        """
        try:
            versions = await self.list_descriptor_versions(service_name)
        except NotFoundError:
            return None
        for v in versions:
            if v.is_active:
                return v.version
        return None

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    async def get_instances(
        self,
        service_name: str,
        *,
        healthy_only: bool = True,
        tag_filters: dict[str, str] | None = None,
    ) -> list[dict]:
        """
        Query registered instances for a service.

        Returns a list of dicts with keys:
        ``service_name``, ``instance_id``, ``version``, ``tags``, ``status``.
        """
        req = _pb.GetServiceInstancesRequest(
            service_name=service_name,
            healthy_only=healthy_only,
            tag_filters=tag_filters or {},
        )
        resp: _pb.GetServiceInstancesResponse = await self._call(
            self._s.GetServiceInstances(req, metadata=self._meta(), timeout=self._timeout)
        )
        return [
            {
                "service_name": inst.service_name,
                "instance_id": inst.instance_id,
                "version": inst.version,
                "tags": dict(inst.tags),
                "status": _pb.ServiceStatus.Name(inst.status),
            }
            for inst in resp.instances
        ]


# ---------------------------------------------------------------------------
# Convenience: synchronous wrapper for non-async code
# ---------------------------------------------------------------------------


class SyncDiscoveryClient:
    """
    Synchronous façade over :class:`DiscoveryClient`.

    Runs an internal event loop.  Not suitable for use inside an already-
    running async event loop — use :class:`DiscoveryClient` directly there.

    Example::

        with SyncDiscoveryClient("127.0.0.1:3012", api_key="svc_xxx") as c:
            instance_id = c.register(
                service_name="stew.api.v1.MyService",
                endpoints=[Endpoint("10.0.0.5", 50051)],
                descriptor_data=open("my_service.pb", "rb").read(),
            )
    """

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        self._client = DiscoveryClient(*args, **kwargs)
        self._loop = asyncio.new_event_loop()

    def _run(self, coro):  # type: ignore[no-untyped-def]
        return self._loop.run_until_complete(coro)

    def __enter__(self) -> "SyncDiscoveryClient":
        self._run(self._client.connect())
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self._run(self._client.close())
        self._loop.close()

    def register(self, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self._run(self._client.register(**kwargs))

    def deregister(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
        self._run(self._client.deregister(**kwargs))

    def heartbeat(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
        self._run(self._client.heartbeat(**kwargs))

    def upload_descriptor(self, **kwargs) -> dict:  # type: ignore[no-untyped-def]
        return self._run(self._client.upload_descriptor(**kwargs))

    def upload_descriptor_from_file(self, **kwargs) -> dict:  # type: ignore[no-untyped-def]
        return self._run(self._client.upload_descriptor_from_file(**kwargs))

    def rollback_descriptor(self, **kwargs) -> str:  # type: ignore[no-untyped-def]
        return self._run(self._client.rollback_descriptor(**kwargs))

    def list_descriptor_versions(self, service_name: str) -> list[DescriptorVersion]:
        return self._run(self._client.list_descriptor_versions(service_name))

    def get_instances(self, service_name: str, **kwargs) -> list[dict]:  # type: ignore[no-untyped-def]
        return self._run(self._client.get_instances(service_name, **kwargs))

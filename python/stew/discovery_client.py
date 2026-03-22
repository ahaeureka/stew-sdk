"""
Stew Gateway -- Service Discovery gRPC Client SDK

Provides a high-level client for descriptor submission, version management,
and health keepalive against the Stew gateway.

Admin-first model
-----------------
Service lifecycle is managed through the admin frontend:

1. Admin initialises a service via the management UI and receives an APP Secret.
2. Business-side code uses the APP Secret to authenticate and upload descriptors.

The ``register()`` and ``deregister()`` methods are **deprecated** and will
raise ``DeprecationWarning``.  Use the admin UI for service registration.

Usage:
    from stew.discovery_client import DiscoveryClient

    async with DiscoveryClient("127.0.0.1:3012", app_secret="ak_xxx") as client:
        await client.upload_descriptor_from_file(
            service_name="stew.api.v1.OrderService",
            pb_path="./order_service.pb",
        )
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import time
from dataclasses import dataclass
from enum import IntEnum
from types import TracebackType
from typing import Callable, Sequence

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
    "RegistrationConfig",
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


@dataclass
class RegistrationConfig:
    """
    Endpoint and metadata used for automatic service re-registration.

    Pass an instance to :meth:`DiscoveryClient.start_keepalive` to enable
    self-healing: when the gateway returns ``NOT_FOUND`` during a heartbeat
    (e.g. after the gateway restarts and fails to recover the ETCD entry),
    the keepalive loop calls ``RegisterService`` with this configuration and
    resumes normal heartbeats once re-registration succeeds.

    Parameters
    ----------
    endpoints:
        List of backend address/port/weight entries.
    balance_type:
        Load-balancing algorithm.  Defaults to :attr:`BalanceType.ROUND_ROBIN`.
    version:
        Service version string for display / routing purposes.
    health_check:
        Optional active health-check configuration.
    middleware:
        Optional per-service middleware switches (rate limit, CORS, etc.).
    tags:
        Arbitrary key/value labels attached to the service instance.
    protocol:
        Transport protocol: ``"grpc"`` (default) or ``"http"``.
    tls_enabled:
        Whether the backend endpoint requires TLS.
    descriptor_data:
        Raw bytes of the compiled ``.pb`` descriptor file.  When provided the
        descriptor is embedded in the registration request so the gateway can
        rebuild its routing table without a separate upload step.
    """
    endpoints: Sequence[Endpoint]
    balance_type: BalanceType = BalanceType.ROUND_ROBIN
    version: str = ""
    health_check: HealthCheckConfig | None = None
    middleware: MiddlewareConfig | None = None
    tags: dict[str, str] | None = None
    protocol: str = "grpc"
    tls_enabled: bool = False
    descriptor_data: bytes = b""


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
    - Descriptor upload with optimistic locking
    - Descriptor rollback & version listing
    - Health status update & keepalive heartbeat loop
    - Service instance querying

    .. note::

       Service registration and deregistration are now admin-only operations
       performed through the management UI.  The ``register()`` and
       ``deregister()`` methods are deprecated.

    Example::

        async with DiscoveryClient("127.0.0.1:3012", app_secret="ak_xxx") as c:
            await c.upload_descriptor_from_file(
                service_name="stew.api.v1.MyService",
                pb_path="./my_service.pb",
            )
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
        """
        Parameters
        ----------
        gateway_addr:
            Host:port of the Stew gateway gRPC endpoint, e.g. ``127.0.0.1:3012``.
        app_secret:
            APP Secret obtained from the admin UI during service initialisation.
            Falls back to ``api_key``, then env var ``SERVICE_API_KEY``.
        api_key:
            Alias for ``app_secret`` (kept for backward compatibility).
        use_tls:
            Connect over TLS.
        timeout:
            Default RPC deadline in seconds.
        retry_max:
            Maximum number of retries when the gateway is unavailable (UNAVAILABLE
            status code).  Set to 0 to disable retries.
        retry_base_delay:
            Initial retry delay in seconds (doubles on each attempt).
        retry_max_delay:
            Maximum retry delay in seconds (caps the exponential growth).
        """
        self._addr = gateway_addr
        self._api_key = (
            app_secret
            or api_key
            or os.environ.get("APP_SECRET")
            or os.environ.get("SERVICE_API_KEY", "")
        )
        self._use_tls = use_tls
        self._timeout = timeout
        self._retry_max = retry_max
        self._retry_base_delay = retry_base_delay
        self._retry_max_delay = retry_max_delay
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

    async def _call_with_retry(self, make_coro):  # type: ignore[no-untyped-def]
        """
        Call an RPC with exponential-backoff retry for UNAVAILABLE errors.

        ``make_coro`` is a zero-argument callable that returns a new coroutine
        on each invocation (required because coroutines can only be awaited once).
        """
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

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    async def register(self, **_kwargs: object) -> str:  # type: ignore[override]
        """
        Raises
        ------
        PermissionError
            Always.  Service registration is an admin-only operation managed
            through the management frontend.  Obtain an ``app_secret`` from the
            admin UI and use :meth:`upload_descriptor_from_file` instead.
        """
        raise PermissionError(
            "register() is an admin-only operation. "
            "Initialise services through the management frontend to obtain an app_secret, "
            "then use upload_descriptor_from_file() to submit your .pb descriptor."
        )

    async def deregister(self, **_kwargs: object) -> None:  # type: ignore[override]
        """
        Raises
        ------
        PermissionError
            Always.  Service deregistration is an admin-only operation managed
            through the management frontend.
        """
        raise PermissionError(
            "deregister() is an admin-only operation. "
            "Manage service lifecycle through the management frontend."
        )

    # ------------------------------------------------------------------
    # Health / keepalive
    # ------------------------------------------------------------------

    async def heartbeat(
        self,
        *,
        service_name: str,
        instance_id: str,
        status: int = _pb.SERVICE_STATUS_HEALTHY,
        message: str = "",
    ) -> None:
        """
        Send a single health update (keepalive tick).

        Parameters
        ----------
        service_name:
            Fully-qualified service name (must match the ``app_secret`` binding).
        instance_id:
            Instance ID assigned by the admin when the service was configured.
            Use :meth:`get_instances` to discover the assigned ID.
        status:
            One of ``_pb.SERVICE_STATUS_HEALTHY``, ``_pb.SERVICE_STATUS_UNHEALTHY``,
            ``_pb.SERVICE_STATUS_MAINTENANCE``, ``_pb.SERVICE_STATUS_DRAINING``.
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
        """
        Start a background keepalive loop for this instance.

        Sends a heartbeat every ``interval`` seconds.  The loop runs as a
        background ``asyncio.Task`` and is cancelled automatically when the
        client is closed.

        If the gateway returns ``NOT_FOUND`` (e.g. after the gateway process
        restarts and its recovery mechanism fails to restore the ETCD entry),
        the loop will automatically re-register the service using the supplied
        ``registration`` config.  Without ``registration``, a ``NOT_FOUND``
        error is treated the same as any other failure and forwarded to
        ``on_error``.

        Parameters
        ----------
        service_name:
            Fully-qualified service name (must match the ``app_secret`` binding).
        instance_id:
            Instance ID assigned by the admin.  Discover it via
            :meth:`get_instances` if it was not provided to you directly.
        interval:
            Heartbeat interval in seconds.  Must be less than the TTL
            configured on the gateway (default TTL is 300 s, recommended
            interval <= 30 s).
        on_error:
            Optional callback invoked with the :class:`DiscoveryError` each
            time a heartbeat or re-registration attempt fails.  If ``None``,
            failures are only logged.
        registration:
            Optional :class:`RegistrationConfig` enabling self-healing
            re-registration when the gateway loses the service entry.
            When provided and ``NOT_FOUND`` is returned by the gateway, the
            loop calls ``RegisterService`` automatically and resumes normal
            heartbeats on success.

        Raises
        ------
        RuntimeError
            If a keepalive loop is already running for this instance.
        """
        key = f"{service_name}:{instance_id}"
        if key in self._keepalive_tasks:
            raise RuntimeError(f"Keepalive already running for {key}")

        async def _try_reregister() -> None:
            log.info(
                "keepalive: re-registering %s after NOT_FOUND (gateway may have restarted)",
                key,
            )
            assert registration is not None  # guarded by caller
            try:
                instance = _pb.ServiceInstance(
                    service_name=service_name,
                    instance_id=instance_id,
                    version=registration.version,
                    lb=_to_proto_lb(registration.endpoints, registration.balance_type),
                    health_check=_to_proto_hc(registration.health_check),
                    middleware_config=_to_proto_mw(registration.middleware),
                    tags=registration.tags or {},
                    protocol=registration.protocol,
                    tls_enabled=registration.tls_enabled,
                    protobuf_descriptor=registration.descriptor_data,
                    status=_pb.SERVICE_STATUS_HEALTHY,
                )
                req = _pb.RegisterServiceRequest(service=instance)
                resp: _pb.RegisterServiceResponse = await self._call(  # type: ignore[assignment]
                    self._s.RegisterService(req, metadata=self._meta(), timeout=self._timeout)
                )
                if not resp.success:
                    raise DiscoveryError(f"Re-registration rejected by gateway: {resp.message}")
                log.info(
                    "keepalive: re-registration successful for %s (lease=%s)",
                    key,
                    resp.lease_id,
                )
            except DiscoveryError as exc:
                log.error("keepalive: re-registration failed for %s: %s", key, exc)
                if on_error is not None:
                    try:
                        on_error(exc)
                    except Exception:  # noqa: BLE001
                        log.exception("keepalive on_error callback raised for %s", key)

        async def _loop() -> None:
            while True:
                await asyncio.sleep(interval)
                try:
                    await self.heartbeat(
                        service_name=service_name,
                        instance_id=instance_id,
                    )
                    log.debug("keepalive sent for %s", key)
                except NotFoundError as exc:
                    # Gateway lost the registration -- attempt self-healing re-registration.
                    log.warning(
                        "keepalive NOT_FOUND for %s: service is no longer registered on the "
                        "gateway (gateway restart?)",
                        key,
                    )
                    if registration is not None:
                        await _try_reregister()
                    else:
                        log.warning(
                            "keepalive: no RegistrationConfig supplied for %s; "
                            "cannot auto-recover -- re-register via the admin UI",
                            key,
                        )
                        if on_error is not None:
                            try:
                                on_error(exc)
                            except Exception:  # noqa: BLE001
                                log.exception("keepalive on_error callback raised for %s", key)
                except DiscoveryError as exc:
                    log.warning("keepalive failed for %s: %s", key, exc)
                    if on_error is not None:
                        try:
                            on_error(exc)
                        except Exception:  # noqa: BLE001
                            log.exception("keepalive on_error callback raised for %s", key)

        task = asyncio.create_task(_loop(), name=f"keepalive:{key}")
        self._keepalive_tasks[key] = task
        log.info("keepalive started for %s (interval=%ds, auto_recovery=%s)", key, interval, registration is not None)

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
    # Query (read-only, available to all authenticated callers)
    # ------------------------------------------------------------------

    async def list_services(
        self,
        *,
        name_prefix: str = "",
        tag_filters: dict[str, str] | None = None,
    ) -> list[dict]:
        """
        List services registered on the gateway (read-only).

        Parameters
        ----------
        name_prefix:
            Filter by service name prefix.  Empty string returns all services.
        tag_filters:
            Key/value tag pairs that must all match.

        Returns
        -------
        list[dict]
            Each entry contains ``service_name``, ``instance_id``, ``version``,
            ``status``, ``protocol``, and ``endpoints``.
        """
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

        with SyncDiscoveryClient("127.0.0.1:3012", app_secret="ak_xxx") as c:
            c.upload_descriptor_from_file(
                service_name="stew.api.v1.MyService",
                pb_path="./my_service.pb",
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

    def list_services(self, **kwargs) -> list[dict]:  # type: ignore[no-untyped-def]
        return self._run(self._client.list_services(**kwargs))


# ---------------------------------------------------------------------------
# One-stop client with automatic retry on gateway unavailability
# ---------------------------------------------------------------------------


class GatewayClient:
    """
    One-stop client: upload descriptor + start keepalive with automatic retry.

    Simplified entry point for business services.  On :meth:`start`, it:

    1. Connects to the gateway.
    2. Uploads the ``.pb`` descriptor (idempotent; ``ConflictError`` is treated
       as success).
    3. Queries registered instances and starts keepalive heartbeats for each.

    If the gateway is unreachable (``UNAVAILABLE``) at any step, a background
    task retries with exponential backoff until the full sequence succeeds.
    The calling service does **not** need to handle gateway downtime at startup.

    Parameters
    ----------
    gateway_addr:
        Host:port of the Stew gateway gRPC endpoint, e.g. ``127.0.0.1:3012``.
    app_secret:
        APP Secret issued by the admin UI.  Falls back to ``api_key``, then
        the ``APP_SECRET`` / ``SERVICE_API_KEY`` environment variables.
    api_key:
        Alias for ``app_secret`` (kept for backward compatibility).
    service_name:
        Fully-qualified protobuf service name, e.g. ``stew.api.v1.OrderService``.
    pb_path:
        Filesystem path to the compiled ``.pb`` descriptor file.
    version:
        Optional descriptor version string.  Auto-generated when empty.
    description:
        Human-readable note stored with the uploaded version.
    keepalive_interval:
        Heartbeat interval in seconds (must be < gateway TTL; default 30 s).
    retry_base_delay:
        Initial delay between registration retries in seconds.
    retry_max_delay:
        Maximum delay cap for exponential backoff.
    use_tls:
        Connect over TLS.
    timeout:
        Per-RPC deadline in seconds.
    on_registered:
        Optional zero-argument callback invoked once after the first
        successful registration.

    Example::

        async with GatewayClient(
            "127.0.0.1:3012",
            app_secret="ak_xxx",
            service_name="stew.api.v1.OrderService",
            pb_path="./order_service.pb",
        ) as gw:
            await gw.registered.wait()  # optional: block until first success
            await your_app.serve()
    """

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
        retry_base_delay: float = 5.0,
        retry_max_delay: float = 300.0,
        use_tls: bool = False,
        timeout: float = 10.0,
        on_registered: Callable[[], None] | None = None,
    ) -> None:
        # Disable inner retry logic; GatewayClient owns all retry scheduling.
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
        self._retry_base_delay = retry_base_delay
        self._retry_max_delay = retry_max_delay
        self._on_registered = on_registered
        self._registered: asyncio.Event = asyncio.Event()
        self._retry_task: asyncio.Task[None] | None = None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    @property
    def registered(self) -> asyncio.Event:
        """Event that is set once the descriptor has been uploaded successfully."""
        return self._registered

    async def start(self) -> None:
        """
        Connect to the gateway and attempt registration.

        If the gateway is unreachable a background task polls with exponential
        backoff until it becomes available.  This method always returns promptly
        and never raises due to gateway unavailability.
        """
        await self._client.connect()
        try:
            success = await self._register_once()
        except Exception as exc:  # noqa: BLE001
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
        """Cancel background tasks and close the gateway connection."""
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

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _upload_once(self) -> bool:
        """
        Attempt one descriptor upload.

        Returns True on success (including idempotent ConflictError).
        Returns False when the gateway is UNAVAILABLE; raises on other errors.
        """
        active_version: str | None = None
        try:
            active_version = await self._client.get_active_version(self._service_name)
        except DiscoveryError:
            pass  # fail-open: version check is advisory only

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
            for w in result["compatibility_warnings"]:
                log.warning(
                    "descriptor compatibility warning [%s]: %s",
                    self._service_name,
                    w,
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
            if exc.code == grpc.StatusCode.UNAVAILABLE:
                log.warning(
                    "gateway unreachable during descriptor upload [%s]: %s",
                    self._service_name,
                    exc,
                )
                return False
            # Non-retryable error (e.g. PERMISSION_DENIED, INVALID_ARGUMENT).
            log.warning(
                "descriptor upload non-retryable failure for %s: %s",
                self._service_name,
                exc,
            )
            return True  # avoid infinite retries for non-transient errors

    async def _start_keepalive_once(self) -> bool:
        """
        Query registered instances and start keepalive for each.

        Returns False on UNAVAILABLE; True on success or when no instances exist.
        """
        try:
            instances = await self._client.get_instances(
                self._service_name, healthy_only=False
            )
        except DiscoveryError as exc:
            if exc.code == grpc.StatusCode.UNAVAILABLE:
                log.warning(
                    "gateway unreachable during instance query [%s]: %s",
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

        for inst in instances:
            instance_id: str = inst["instance_id"]
            try:
                await self._client.start_keepalive(
                    service_name=self._service_name,
                    instance_id=instance_id,
                    interval=self._keepalive_interval,
                )
                log.info(
                    "keepalive started: service=%s instance_id=%s",
                    self._service_name,
                    instance_id,
                )
            except RuntimeError:
                pass  # keepalive already running for this instance; idempotent

        return True

    async def _register_once(self) -> bool:
        """
        Run one full registration cycle: upload descriptor + start keepalive.

        Returns True on success, False when the gateway is unreachable.
        """
        uploaded = await self._upload_once()
        if not uploaded:
            return False
        return await self._start_keepalive_once()

    def _fire_on_registered(self) -> None:
        self._registered.set()
        if self._on_registered is not None:
            try:
                self._on_registered()
            except Exception:  # noqa: BLE001
                log.exception("on_registered callback raised for %s", self._service_name)

    async def _retry_loop(self) -> None:
        """Background task: retry registration with exponential backoff until success."""
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
            except Exception as exc:  # noqa: BLE001
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

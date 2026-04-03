from __future__ import annotations

import hashlib
from typing import Sequence

import grpc

from stew.api.v1 import service_discovery_pb2 as _pb

from .errors import ConflictError, DiscoveryError, NotFoundError
from .types import BalanceType, Endpoint, EndpointBinding, HealthCheckConfig, MiddlewareConfig


def make_metadata(api_key: str) -> list[tuple[str, str]]:
    if api_key:
        return [("x-api-key", api_key)]
    return []


def to_proto_lb(
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


def to_proto_hc(cfg: HealthCheckConfig | None) -> _pb.HealthCheckConfig | None:
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


def to_proto_mw(cfg: MiddlewareConfig | None) -> _pb.ServiceMiddlewareConfig | None:
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


def as_discovery_error(exc: Exception) -> DiscoveryError:
    if isinstance(exc, DiscoveryError):
        return exc
    return DiscoveryError(f"Unexpected client error: {exc}")


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def endpoint_matches_binding(
    binding: EndpointBinding,
    *,
    service_name: str,
    endpoint: Endpoint,
    protocol: str,
    tls_enabled: bool,
) -> bool:
    return (
        binding.service_name == service_name
        and binding.address == endpoint.address
        and binding.port == endpoint.port
        and binding.weight == endpoint.weight
        and binding.protocol == protocol
        and binding.tls_enabled == tls_enabled
    )


def wrap_rpc_error(exc: grpc.RpcError) -> DiscoveryError:
    code: grpc.StatusCode = exc.code()  # type: ignore[attr-defined]
    detail: str = exc.details() or ""  # type: ignore[attr-defined]
    if code == grpc.StatusCode.NOT_FOUND:
        return NotFoundError(detail, code=code)
    if code == grpc.StatusCode.FAILED_PRECONDITION:
        return ConflictError(detail, code=code)
    return DiscoveryError(f"[{code.name}] {detail}", code=code)


__all__ = [
    "as_discovery_error",
    "endpoint_matches_binding",
    "hash_bytes",
    "make_metadata",
    "to_proto_hc",
    "to_proto_lb",
    "to_proto_mw",
    "wrap_rpc_error",
]
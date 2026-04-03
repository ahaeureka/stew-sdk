from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Sequence

from stew.api.v1 import service_discovery_pb2 as _pb

CorsConfig = _pb.ServiceCorsConfig
RiskRuleConfig = _pb.ServiceRiskRuleConfig
RiskConfig = _pb.ServiceRiskConfig
TurnstileConfig = _pb.ServiceTurnstileConfig


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
    weight: int = 0


@dataclass
class EndpointBinding:
    """Local binding between an endpoint_id and one concrete endpoint config."""

    endpoint_id: str
    service_name: str
    address: str
    port: int
    weight: int = 0
    protocol: str = "grpc"
    tls_enabled: bool = False


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
    created_at: str


@dataclass
class RegistrationConfig:
    """
    Descriptor refresh payload used during keepalive recovery.

    Pass an instance to :meth:`DiscoveryClient.start_keepalive` to enable
    self-healing: when keepalive encounters gateway errors, network failures,
    or missing runtime descriptor state, the background recovery loop replays
    the local ``.pb`` descriptor upload and resumes normal heartbeats once the
    descriptor refresh plus heartbeat both succeed.

    The admin frontend remains the source of truth for instance configuration.
    Local recovery only refreshes the protobuf descriptor and does not push
    endpoint, middleware, tag, protocol, or TLS settings back to the gateway.
    """

    endpoints: Sequence[Endpoint] = field(default_factory=tuple)
    balance_type: BalanceType = BalanceType.ROUND_ROBIN
    version: str = ""
    health_check: HealthCheckConfig | None = None
    middleware: MiddlewareConfig | None = None
    tags: dict[str, str] | None = None
    protocol: str = "grpc"
    tls_enabled: bool = False
    descriptor_data: bytes = b""
    descriptor_path: str = ""


__all__ = [
    "BalanceType",
    "CorsConfig",
    "DescriptorVersion",
    "Endpoint",
    "EndpointBinding",
    "HealthCheckConfig",
    "MiddlewareConfig",
    "RegistrationConfig",
    "RiskConfig",
    "RiskRuleConfig",
    "TurnstileConfig",
]
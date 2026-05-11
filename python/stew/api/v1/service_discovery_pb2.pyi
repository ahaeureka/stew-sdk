import datetime

from google.protobuf import any_pb2 as _any_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
import billing_common_pb2 as _billing_common_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from stew.api.v1 import web_pb2 as _web_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BalanceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BALANCE_TYPE_UNKNOWN: _ClassVar[BalanceType]
    BALANCE_TYPE_ROUND_ROBIN: _ClassVar[BalanceType]
    BALANCE_TYPE_WEIGHTED_ROUND_ROBIN: _ClassVar[BalanceType]
    BALANCE_TYPE_CONSISTENT_HASH: _ClassVar[BalanceType]
    BALANCE_TYPE_LEAST_CONNECTIONS: _ClassVar[BalanceType]
    BALANCE_TYPE_SED: _ClassVar[BalanceType]
    BALANCE_TYPE_WEIGHTED_LEAST_CONNECTIONS: _ClassVar[BalanceType]
    BALANCE_TYPE_NEVER_QUEUE: _ClassVar[BalanceType]

class ServiceStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SERVICE_STATUS_UNKNOWN: _ClassVar[ServiceStatus]
    SERVICE_STATUS_HEALTHY: _ClassVar[ServiceStatus]
    SERVICE_STATUS_UNHEALTHY: _ClassVar[ServiceStatus]
    SERVICE_STATUS_MAINTENANCE: _ClassVar[ServiceStatus]
    SERVICE_STATUS_DRAINING: _ClassVar[ServiceStatus]
BALANCE_TYPE_UNKNOWN: BalanceType
BALANCE_TYPE_ROUND_ROBIN: BalanceType
BALANCE_TYPE_WEIGHTED_ROUND_ROBIN: BalanceType
BALANCE_TYPE_CONSISTENT_HASH: BalanceType
BALANCE_TYPE_LEAST_CONNECTIONS: BalanceType
BALANCE_TYPE_SED: BalanceType
BALANCE_TYPE_WEIGHTED_LEAST_CONNECTIONS: BalanceType
BALANCE_TYPE_NEVER_QUEUE: BalanceType
SERVICE_STATUS_UNKNOWN: ServiceStatus
SERVICE_STATUS_HEALTHY: ServiceStatus
SERVICE_STATUS_UNHEALTHY: ServiceStatus
SERVICE_STATUS_MAINTENANCE: ServiceStatus
SERVICE_STATUS_DRAINING: ServiceStatus

class Endpoint(_message.Message):
    __slots__ = ("address", "port", "weight")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    address: str
    port: int
    weight: int
    def __init__(self, address: _Optional[str] = ..., port: _Optional[int] = ..., weight: _Optional[int] = ...) -> None: ...

class LoadBalancer(_message.Message):
    __slots__ = ("type", "endpoints")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    type: BalanceType
    endpoints: _containers.RepeatedCompositeFieldContainer[Endpoint]
    def __init__(self, type: _Optional[_Union[BalanceType, str]] = ..., endpoints: _Optional[_Iterable[_Union[Endpoint, _Mapping]]] = ...) -> None: ...

class HealthCheckConfig(_message.Message):
    __slots__ = ("grpc_method", "http_path", "interval_seconds", "timeout_seconds", "healthy_threshold", "unhealthy_threshold", "enabled")
    GRPC_METHOD_FIELD_NUMBER: _ClassVar[int]
    HTTP_PATH_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    HEALTHY_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    UNHEALTHY_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    grpc_method: str
    http_path: str
    interval_seconds: int
    timeout_seconds: int
    healthy_threshold: int
    unhealthy_threshold: int
    enabled: bool
    def __init__(self, grpc_method: _Optional[str] = ..., http_path: _Optional[str] = ..., interval_seconds: _Optional[int] = ..., timeout_seconds: _Optional[int] = ..., healthy_threshold: _Optional[int] = ..., unhealthy_threshold: _Optional[int] = ..., enabled: bool = ...) -> None: ...

class ServiceCorsConfig(_message.Message):
    __slots__ = ("enabled", "allow_origins", "allow_methods", "allow_headers", "expose_headers", "allow_credentials", "max_age_secs")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ALLOW_ORIGINS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_METHODS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_HEADERS_FIELD_NUMBER: _ClassVar[int]
    EXPOSE_HEADERS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    MAX_AGE_SECS_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    allow_origins: _containers.RepeatedScalarFieldContainer[str]
    allow_methods: _containers.RepeatedScalarFieldContainer[str]
    allow_headers: _containers.RepeatedScalarFieldContainer[str]
    expose_headers: _containers.RepeatedScalarFieldContainer[str]
    allow_credentials: bool
    max_age_secs: int
    def __init__(self, enabled: bool = ..., allow_origins: _Optional[_Iterable[str]] = ..., allow_methods: _Optional[_Iterable[str]] = ..., allow_headers: _Optional[_Iterable[str]] = ..., expose_headers: _Optional[_Iterable[str]] = ..., allow_credentials: bool = ..., max_age_secs: _Optional[int] = ...) -> None: ...

class ServiceRiskRuleConfig(_message.Message):
    __slots__ = ("name", "enabled", "path_prefixes", "countries", "proxy", "tor", "datacenter", "min_bot_score", "max_bot_score", "action")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    PATH_PREFIXES_FIELD_NUMBER: _ClassVar[int]
    COUNTRIES_FIELD_NUMBER: _ClassVar[int]
    PROXY_FIELD_NUMBER: _ClassVar[int]
    TOR_FIELD_NUMBER: _ClassVar[int]
    DATACENTER_FIELD_NUMBER: _ClassVar[int]
    MIN_BOT_SCORE_FIELD_NUMBER: _ClassVar[int]
    MAX_BOT_SCORE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    enabled: bool
    path_prefixes: _containers.RepeatedScalarFieldContainer[str]
    countries: _containers.RepeatedScalarFieldContainer[str]
    proxy: bool
    tor: bool
    datacenter: bool
    min_bot_score: int
    max_bot_score: int
    action: str
    def __init__(self, name: _Optional[str] = ..., enabled: bool = ..., path_prefixes: _Optional[_Iterable[str]] = ..., countries: _Optional[_Iterable[str]] = ..., proxy: bool = ..., tor: bool = ..., datacenter: bool = ..., min_bot_score: _Optional[int] = ..., max_bot_score: _Optional[int] = ..., action: _Optional[str] = ...) -> None: ...

class ServiceRiskConfig(_message.Message):
    __slots__ = ("enabled", "mode", "default_action", "challenge_paths", "block_paths", "observe_only_paths", "high_risk_countries", "challenge_proxy_traffic", "block_datacenter_traffic", "allow_tor_exit_nodes", "bot_score_threshold", "proxy_score_threshold", "action_overrides")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ACTION_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_PATHS_FIELD_NUMBER: _ClassVar[int]
    BLOCK_PATHS_FIELD_NUMBER: _ClassVar[int]
    OBSERVE_ONLY_PATHS_FIELD_NUMBER: _ClassVar[int]
    HIGH_RISK_COUNTRIES_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_PROXY_TRAFFIC_FIELD_NUMBER: _ClassVar[int]
    BLOCK_DATACENTER_TRAFFIC_FIELD_NUMBER: _ClassVar[int]
    ALLOW_TOR_EXIT_NODES_FIELD_NUMBER: _ClassVar[int]
    BOT_SCORE_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    PROXY_SCORE_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    ACTION_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    mode: str
    default_action: str
    challenge_paths: _containers.RepeatedScalarFieldContainer[str]
    block_paths: _containers.RepeatedScalarFieldContainer[str]
    observe_only_paths: _containers.RepeatedScalarFieldContainer[str]
    high_risk_countries: _containers.RepeatedScalarFieldContainer[str]
    challenge_proxy_traffic: bool
    block_datacenter_traffic: bool
    allow_tor_exit_nodes: bool
    bot_score_threshold: int
    proxy_score_threshold: int
    action_overrides: _containers.RepeatedCompositeFieldContainer[ServiceRiskRuleConfig]
    def __init__(self, enabled: bool = ..., mode: _Optional[str] = ..., default_action: _Optional[str] = ..., challenge_paths: _Optional[_Iterable[str]] = ..., block_paths: _Optional[_Iterable[str]] = ..., observe_only_paths: _Optional[_Iterable[str]] = ..., high_risk_countries: _Optional[_Iterable[str]] = ..., challenge_proxy_traffic: bool = ..., block_datacenter_traffic: bool = ..., allow_tor_exit_nodes: bool = ..., bot_score_threshold: _Optional[int] = ..., proxy_score_threshold: _Optional[int] = ..., action_overrides: _Optional[_Iterable[_Union[ServiceRiskRuleConfig, _Mapping]]] = ...) -> None: ...

class ServiceTurnstileConfig(_message.Message):
    __slots__ = ("enabled", "required_paths", "skip_paths", "expected_action", "expected_hostname", "enforce_on_risk_challenge")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_PATHS_FIELD_NUMBER: _ClassVar[int]
    SKIP_PATHS_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_ACTION_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    ENFORCE_ON_RISK_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    required_paths: _containers.RepeatedScalarFieldContainer[str]
    skip_paths: _containers.RepeatedScalarFieldContainer[str]
    expected_action: str
    expected_hostname: str
    enforce_on_risk_challenge: bool
    def __init__(self, enabled: bool = ..., required_paths: _Optional[_Iterable[str]] = ..., skip_paths: _Optional[_Iterable[str]] = ..., expected_action: _Optional[str] = ..., expected_hostname: _Optional[str] = ..., enforce_on_risk_challenge: bool = ...) -> None: ...

class AiBodyFieldMap(_message.Message):
    __slots__ = ("messages_path", "role_field", "content_field", "user_role_value", "prompt_path", "model_path", "max_tokens_path")
    MESSAGES_PATH_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_FIELD_NUMBER: _ClassVar[int]
    USER_ROLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    PROMPT_PATH_FIELD_NUMBER: _ClassVar[int]
    MODEL_PATH_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_PATH_FIELD_NUMBER: _ClassVar[int]
    messages_path: str
    role_field: str
    content_field: str
    user_role_value: str
    prompt_path: str
    model_path: str
    max_tokens_path: str
    def __init__(self, messages_path: _Optional[str] = ..., role_field: _Optional[str] = ..., content_field: _Optional[str] = ..., user_role_value: _Optional[str] = ..., prompt_path: _Optional[str] = ..., model_path: _Optional[str] = ..., max_tokens_path: _Optional[str] = ...) -> None: ...

class ServiceAiGuardConfig(_message.Message):
    __slots__ = ("enabled", "mode", "include_paths", "request_body_max_bytes", "max_input_tokens", "max_output_tokens", "max_context_tokens", "history_policy", "daily_token_quota", "daily_request_quota", "minute_request_quota", "allow_free_chat", "allowed_topics", "deny_keywords", "enable_audit", "classifier_type", "llm_endpoint", "llm_model", "llm_system_prompt", "llm_timeout_ms", "llm_confidence_threshold", "body_map", "quota_window_secs", "business_description", "valid_intent_examples", "invalid_intent_examples", "endpoint_overrides")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PATHS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_BODY_MAX_BYTES_FIELD_NUMBER: _ClassVar[int]
    MAX_INPUT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    MAX_OUTPUT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    MAX_CONTEXT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    HISTORY_POLICY_FIELD_NUMBER: _ClassVar[int]
    DAILY_TOKEN_QUOTA_FIELD_NUMBER: _ClassVar[int]
    DAILY_REQUEST_QUOTA_FIELD_NUMBER: _ClassVar[int]
    MINUTE_REQUEST_QUOTA_FIELD_NUMBER: _ClassVar[int]
    ALLOW_FREE_CHAT_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_TOPICS_FIELD_NUMBER: _ClassVar[int]
    DENY_KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    ENABLE_AUDIT_FIELD_NUMBER: _ClassVar[int]
    CLASSIFIER_TYPE_FIELD_NUMBER: _ClassVar[int]
    LLM_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    LLM_MODEL_FIELD_NUMBER: _ClassVar[int]
    LLM_SYSTEM_PROMPT_FIELD_NUMBER: _ClassVar[int]
    LLM_TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    LLM_CONFIDENCE_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    BODY_MAP_FIELD_NUMBER: _ClassVar[int]
    QUOTA_WINDOW_SECS_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VALID_INTENT_EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    INVALID_INTENT_EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    mode: str
    include_paths: _containers.RepeatedScalarFieldContainer[str]
    request_body_max_bytes: int
    max_input_tokens: int
    max_output_tokens: int
    max_context_tokens: int
    history_policy: str
    daily_token_quota: int
    daily_request_quota: int
    minute_request_quota: int
    allow_free_chat: bool
    allowed_topics: _containers.RepeatedScalarFieldContainer[str]
    deny_keywords: _containers.RepeatedScalarFieldContainer[str]
    enable_audit: bool
    classifier_type: str
    llm_endpoint: str
    llm_model: str
    llm_system_prompt: str
    llm_timeout_ms: int
    llm_confidence_threshold: float
    body_map: AiBodyFieldMap
    quota_window_secs: int
    business_description: str
    valid_intent_examples: _containers.RepeatedScalarFieldContainer[str]
    invalid_intent_examples: _containers.RepeatedScalarFieldContainer[str]
    endpoint_overrides: _containers.RepeatedCompositeFieldContainer[AiGuardEndpointConfig]
    def __init__(self, enabled: bool = ..., mode: _Optional[str] = ..., include_paths: _Optional[_Iterable[str]] = ..., request_body_max_bytes: _Optional[int] = ..., max_input_tokens: _Optional[int] = ..., max_output_tokens: _Optional[int] = ..., max_context_tokens: _Optional[int] = ..., history_policy: _Optional[str] = ..., daily_token_quota: _Optional[int] = ..., daily_request_quota: _Optional[int] = ..., minute_request_quota: _Optional[int] = ..., allow_free_chat: bool = ..., allowed_topics: _Optional[_Iterable[str]] = ..., deny_keywords: _Optional[_Iterable[str]] = ..., enable_audit: bool = ..., classifier_type: _Optional[str] = ..., llm_endpoint: _Optional[str] = ..., llm_model: _Optional[str] = ..., llm_system_prompt: _Optional[str] = ..., llm_timeout_ms: _Optional[int] = ..., llm_confidence_threshold: _Optional[float] = ..., body_map: _Optional[_Union[AiBodyFieldMap, _Mapping]] = ..., quota_window_secs: _Optional[int] = ..., business_description: _Optional[str] = ..., valid_intent_examples: _Optional[_Iterable[str]] = ..., invalid_intent_examples: _Optional[_Iterable[str]] = ..., endpoint_overrides: _Optional[_Iterable[_Union[AiGuardEndpointConfig, _Mapping]]] = ...) -> None: ...

class AiGuardEndpointConfig(_message.Message):
    __slots__ = ("endpoint_id", "exact_paths", "prefix_paths", "pattern_paths", "disabled", "mode", "request_body_max_bytes", "max_input_tokens", "max_output_tokens", "max_context_tokens", "history_policy", "daily_token_quota", "daily_request_quota", "minute_request_quota", "quota_window_secs", "allow_free_chat", "allowed_topics", "deny_keywords", "enable_audit", "classifier_type", "llm_endpoint", "llm_model", "llm_system_prompt", "business_description", "valid_intent_examples", "invalid_intent_examples", "llm_timeout_ms", "llm_confidence_threshold", "body_map")
    ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    EXACT_PATHS_FIELD_NUMBER: _ClassVar[int]
    PREFIX_PATHS_FIELD_NUMBER: _ClassVar[int]
    PATTERN_PATHS_FIELD_NUMBER: _ClassVar[int]
    DISABLED_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_BODY_MAX_BYTES_FIELD_NUMBER: _ClassVar[int]
    MAX_INPUT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    MAX_OUTPUT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    MAX_CONTEXT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    HISTORY_POLICY_FIELD_NUMBER: _ClassVar[int]
    DAILY_TOKEN_QUOTA_FIELD_NUMBER: _ClassVar[int]
    DAILY_REQUEST_QUOTA_FIELD_NUMBER: _ClassVar[int]
    MINUTE_REQUEST_QUOTA_FIELD_NUMBER: _ClassVar[int]
    QUOTA_WINDOW_SECS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_FREE_CHAT_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_TOPICS_FIELD_NUMBER: _ClassVar[int]
    DENY_KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    ENABLE_AUDIT_FIELD_NUMBER: _ClassVar[int]
    CLASSIFIER_TYPE_FIELD_NUMBER: _ClassVar[int]
    LLM_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    LLM_MODEL_FIELD_NUMBER: _ClassVar[int]
    LLM_SYSTEM_PROMPT_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VALID_INTENT_EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    INVALID_INTENT_EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    LLM_TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    LLM_CONFIDENCE_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    BODY_MAP_FIELD_NUMBER: _ClassVar[int]
    endpoint_id: str
    exact_paths: _containers.RepeatedScalarFieldContainer[str]
    prefix_paths: _containers.RepeatedScalarFieldContainer[str]
    pattern_paths: _containers.RepeatedScalarFieldContainer[str]
    disabled: bool
    mode: str
    request_body_max_bytes: int
    max_input_tokens: int
    max_output_tokens: int
    max_context_tokens: int
    history_policy: str
    daily_token_quota: int
    daily_request_quota: int
    minute_request_quota: int
    quota_window_secs: int
    allow_free_chat: bool
    allowed_topics: _containers.RepeatedScalarFieldContainer[str]
    deny_keywords: _containers.RepeatedScalarFieldContainer[str]
    enable_audit: bool
    classifier_type: str
    llm_endpoint: str
    llm_model: str
    llm_system_prompt: str
    business_description: str
    valid_intent_examples: _containers.RepeatedScalarFieldContainer[str]
    invalid_intent_examples: _containers.RepeatedScalarFieldContainer[str]
    llm_timeout_ms: int
    llm_confidence_threshold: float
    body_map: AiBodyFieldMap
    def __init__(self, endpoint_id: _Optional[str] = ..., exact_paths: _Optional[_Iterable[str]] = ..., prefix_paths: _Optional[_Iterable[str]] = ..., pattern_paths: _Optional[_Iterable[str]] = ..., disabled: bool = ..., mode: _Optional[str] = ..., request_body_max_bytes: _Optional[int] = ..., max_input_tokens: _Optional[int] = ..., max_output_tokens: _Optional[int] = ..., max_context_tokens: _Optional[int] = ..., history_policy: _Optional[str] = ..., daily_token_quota: _Optional[int] = ..., daily_request_quota: _Optional[int] = ..., minute_request_quota: _Optional[int] = ..., quota_window_secs: _Optional[int] = ..., allow_free_chat: bool = ..., allowed_topics: _Optional[_Iterable[str]] = ..., deny_keywords: _Optional[_Iterable[str]] = ..., enable_audit: bool = ..., classifier_type: _Optional[str] = ..., llm_endpoint: _Optional[str] = ..., llm_model: _Optional[str] = ..., llm_system_prompt: _Optional[str] = ..., business_description: _Optional[str] = ..., valid_intent_examples: _Optional[_Iterable[str]] = ..., invalid_intent_examples: _Optional[_Iterable[str]] = ..., llm_timeout_ms: _Optional[int] = ..., llm_confidence_threshold: _Optional[float] = ..., body_map: _Optional[_Union[AiBodyFieldMap, _Mapping]] = ...) -> None: ...

class ServiceSubscriptionConfig(_message.Message):
    __slots__ = ("enabled", "business_id", "default_plan_id", "auto_create_subscription", "inject_features", "inject_quotas", "feature_gate_mode", "require_active_subscription", "endpoint_features")
    class EndpointFeaturesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    AUTO_CREATE_SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    INJECT_FEATURES_FIELD_NUMBER: _ClassVar[int]
    INJECT_QUOTAS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_GATE_MODE_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_ACTIVE_SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FEATURES_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    business_id: str
    default_plan_id: str
    auto_create_subscription: bool
    inject_features: bool
    inject_quotas: bool
    feature_gate_mode: str
    require_active_subscription: bool
    endpoint_features: _containers.ScalarMap[str, str]
    def __init__(self, enabled: bool = ..., business_id: _Optional[str] = ..., default_plan_id: _Optional[str] = ..., auto_create_subscription: bool = ..., inject_features: bool = ..., inject_quotas: bool = ..., feature_gate_mode: _Optional[str] = ..., require_active_subscription: bool = ..., endpoint_features: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ServiceRbacPolicyRule(_message.Message):
    __slots__ = ("pattern", "methods", "roles", "permissions", "groups")
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    METHODS_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    pattern: str
    methods: _containers.RepeatedScalarFieldContainer[str]
    roles: _containers.RepeatedScalarFieldContainer[str]
    permissions: _containers.RepeatedScalarFieldContainer[str]
    groups: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, pattern: _Optional[str] = ..., methods: _Optional[_Iterable[str]] = ..., roles: _Optional[_Iterable[str]] = ..., permissions: _Optional[_Iterable[str]] = ..., groups: _Optional[_Iterable[str]] = ...) -> None: ...

class ServiceRbacConfig(_message.Message):
    __slots__ = ("enabled", "default_action", "admin_bypass", "roles_claim_path", "permissions_claim_path", "groups_claim_path", "rules")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ACTION_FIELD_NUMBER: _ClassVar[int]
    ADMIN_BYPASS_FIELD_NUMBER: _ClassVar[int]
    ROLES_CLAIM_PATH_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_CLAIM_PATH_FIELD_NUMBER: _ClassVar[int]
    GROUPS_CLAIM_PATH_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    default_action: str
    admin_bypass: bool
    roles_claim_path: str
    permissions_claim_path: str
    groups_claim_path: str
    rules: _containers.RepeatedCompositeFieldContainer[ServiceRbacPolicyRule]
    def __init__(self, enabled: bool = ..., default_action: _Optional[str] = ..., admin_bypass: bool = ..., roles_claim_path: _Optional[str] = ..., permissions_claim_path: _Optional[str] = ..., groups_claim_path: _Optional[str] = ..., rules: _Optional[_Iterable[_Union[ServiceRbacPolicyRule, _Mapping]]] = ...) -> None: ...

class ServiceMiddlewareConfig(_message.Message):
    __slots__ = ("rate_limit_enabled", "rate_limit_rpm", "rate_limit_user_rpm", "cors_enabled", "cors", "risk_enabled", "risk", "turnstile_enabled", "turnstile", "ai_guard_enabled", "ai_guard", "billing_enabled", "billing", "subscription_enabled", "subscription", "rbac_enabled", "rbac")
    RATE_LIMIT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    RATE_LIMIT_RPM_FIELD_NUMBER: _ClassVar[int]
    RATE_LIMIT_USER_RPM_FIELD_NUMBER: _ClassVar[int]
    CORS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CORS_FIELD_NUMBER: _ClassVar[int]
    RISK_ENABLED_FIELD_NUMBER: _ClassVar[int]
    RISK_FIELD_NUMBER: _ClassVar[int]
    TURNSTILE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TURNSTILE_FIELD_NUMBER: _ClassVar[int]
    AI_GUARD_ENABLED_FIELD_NUMBER: _ClassVar[int]
    AI_GUARD_FIELD_NUMBER: _ClassVar[int]
    BILLING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    BILLING_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RBAC_ENABLED_FIELD_NUMBER: _ClassVar[int]
    RBAC_FIELD_NUMBER: _ClassVar[int]
    rate_limit_enabled: bool
    rate_limit_rpm: int
    rate_limit_user_rpm: int
    cors_enabled: bool
    cors: ServiceCorsConfig
    risk_enabled: bool
    risk: ServiceRiskConfig
    turnstile_enabled: bool
    turnstile: ServiceTurnstileConfig
    ai_guard_enabled: bool
    ai_guard: ServiceAiGuardConfig
    billing_enabled: bool
    billing: _billing_common_pb2.ServiceBillingConfig
    subscription_enabled: bool
    subscription: ServiceSubscriptionConfig
    rbac_enabled: bool
    rbac: ServiceRbacConfig
    def __init__(self, rate_limit_enabled: bool = ..., rate_limit_rpm: _Optional[int] = ..., rate_limit_user_rpm: _Optional[int] = ..., cors_enabled: bool = ..., cors: _Optional[_Union[ServiceCorsConfig, _Mapping]] = ..., risk_enabled: bool = ..., risk: _Optional[_Union[ServiceRiskConfig, _Mapping]] = ..., turnstile_enabled: bool = ..., turnstile: _Optional[_Union[ServiceTurnstileConfig, _Mapping]] = ..., ai_guard_enabled: bool = ..., ai_guard: _Optional[_Union[ServiceAiGuardConfig, _Mapping]] = ..., billing_enabled: bool = ..., billing: _Optional[_Union[_billing_common_pb2.ServiceBillingConfig, _Mapping]] = ..., subscription_enabled: bool = ..., subscription: _Optional[_Union[ServiceSubscriptionConfig, _Mapping]] = ..., rbac_enabled: bool = ..., rbac: _Optional[_Union[ServiceRbacConfig, _Mapping]] = ...) -> None: ...

class ServiceInstance(_message.Message):
    __slots__ = ("service_name", "instance_id", "lb", "version", "metadata", "health_endpoint", "health_check_config", "registered_at", "status", "weight", "tags", "protocol", "tls_enabled", "protobuf_descriptor", "middleware_config", "business_id")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _any_pb2.Any
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    LB_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    HEALTH_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CHECK_CONFIG_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    TLS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PROTOBUF_DESCRIPTOR_FIELD_NUMBER: _ClassVar[int]
    MIDDLEWARE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    instance_id: str
    lb: LoadBalancer
    version: str
    metadata: _containers.MessageMap[str, _any_pb2.Any]
    health_endpoint: str
    health_check_config: HealthCheckConfig
    registered_at: _timestamp_pb2.Timestamp
    status: ServiceStatus
    weight: int
    tags: _containers.ScalarMap[str, str]
    protocol: str
    tls_enabled: bool
    protobuf_descriptor: bytes
    middleware_config: ServiceMiddlewareConfig
    business_id: str
    def __init__(self, service_name: _Optional[str] = ..., instance_id: _Optional[str] = ..., lb: _Optional[_Union[LoadBalancer, _Mapping]] = ..., version: _Optional[str] = ..., metadata: _Optional[_Mapping[str, _any_pb2.Any]] = ..., health_endpoint: _Optional[str] = ..., health_check_config: _Optional[_Union[HealthCheckConfig, _Mapping]] = ..., registered_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[ServiceStatus, str]] = ..., weight: _Optional[int] = ..., tags: _Optional[_Mapping[str, str]] = ..., protocol: _Optional[str] = ..., tls_enabled: bool = ..., protobuf_descriptor: _Optional[bytes] = ..., middleware_config: _Optional[_Union[ServiceMiddlewareConfig, _Mapping]] = ..., business_id: _Optional[str] = ...) -> None: ...

class InitServiceRequest(_message.Message):
    __slots__ = ("service_name", "description", "protocol")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    description: str
    protocol: str
    def __init__(self, service_name: _Optional[str] = ..., description: _Optional[str] = ..., protocol: _Optional[str] = ...) -> None: ...

class InitServiceResponse(_message.Message):
    __slots__ = ("success", "message", "app_id", "app_secret", "service_name", "business_id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SECRET_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    app_id: str
    app_secret: str
    service_name: str
    business_id: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., app_id: _Optional[str] = ..., app_secret: _Optional[str] = ..., service_name: _Optional[str] = ..., business_id: _Optional[str] = ...) -> None: ...

class RegisterServiceRequest(_message.Message):
    __slots__ = ("service", "ttl")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    service: ServiceInstance
    ttl: int
    def __init__(self, service: _Optional[_Union[ServiceInstance, _Mapping]] = ..., ttl: _Optional[int] = ...) -> None: ...

class RegisterServiceResponse(_message.Message):
    __slots__ = ("success", "message", "lease_id", "instance_id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LEASE_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    lease_id: str
    instance_id: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., lease_id: _Optional[str] = ..., instance_id: _Optional[str] = ...) -> None: ...

class RegisterServiceEndpointRequest(_message.Message):
    __slots__ = ("service_name", "endpoint_id", "endpoint", "version", "protocol", "tls_enabled", "protobuf_descriptor")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    TLS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PROTOBUF_DESCRIPTOR_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    endpoint_id: str
    endpoint: Endpoint
    version: str
    protocol: str
    tls_enabled: bool
    protobuf_descriptor: bytes
    def __init__(self, service_name: _Optional[str] = ..., endpoint_id: _Optional[str] = ..., endpoint: _Optional[_Union[Endpoint, _Mapping]] = ..., version: _Optional[str] = ..., protocol: _Optional[str] = ..., tls_enabled: bool = ..., protobuf_descriptor: _Optional[bytes] = ...) -> None: ...

class RegisterServiceEndpointResponse(_message.Message):
    __slots__ = ("success", "message", "endpoint_id", "lease_id", "registered_service")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    LEASE_ID_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_SERVICE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    endpoint_id: str
    lease_id: str
    registered_service: ServiceInstance
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., endpoint_id: _Optional[str] = ..., lease_id: _Optional[str] = ..., registered_service: _Optional[_Union[ServiceInstance, _Mapping]] = ...) -> None: ...

class DeregisterServiceEndpointRequest(_message.Message):
    __slots__ = ("service_name", "endpoint_id")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    endpoint_id: str
    def __init__(self, service_name: _Optional[str] = ..., endpoint_id: _Optional[str] = ...) -> None: ...

class DeregisterServiceEndpointResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class DeregisterServiceRequest(_message.Message):
    __slots__ = ("service_name", "instance_id")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    instance_id: str
    def __init__(self, service_name: _Optional[str] = ..., instance_id: _Optional[str] = ...) -> None: ...

class DeregisterServiceResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class DeleteServiceRecordRequest(_message.Message):
    __slots__ = ("service_name", "instance_id")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    instance_id: str
    def __init__(self, service_name: _Optional[str] = ..., instance_id: _Optional[str] = ...) -> None: ...

class DeleteServiceRecordResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class UpdateServiceInstanceRequest(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: ServiceInstance
    def __init__(self, service: _Optional[_Union[ServiceInstance, _Mapping]] = ...) -> None: ...

class UpdateServiceInstanceResponse(_message.Message):
    __slots__ = ("success", "message", "updated_service")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_SERVICE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    updated_service: ServiceInstance
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., updated_service: _Optional[_Union[ServiceInstance, _Mapping]] = ...) -> None: ...

class GetServiceInstancesRequest(_message.Message):
    __slots__ = ("service_name", "tag_filters", "healthy_only")
    class TagFiltersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    TAG_FILTERS_FIELD_NUMBER: _ClassVar[int]
    HEALTHY_ONLY_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    tag_filters: _containers.ScalarMap[str, str]
    healthy_only: bool
    def __init__(self, service_name: _Optional[str] = ..., tag_filters: _Optional[_Mapping[str, str]] = ..., healthy_only: bool = ...) -> None: ...

class GetServiceInstancesResponse(_message.Message):
    __slots__ = ("instances", "total_count")
    INSTANCES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    instances: _containers.RepeatedCompositeFieldContainer[ServiceInstance]
    total_count: int
    def __init__(self, instances: _Optional[_Iterable[_Union[ServiceInstance, _Mapping]]] = ..., total_count: _Optional[int] = ...) -> None: ...

class ListServicesRequest(_message.Message):
    __slots__ = ("name_prefix", "tag_filters")
    class TagFiltersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_PREFIX_FIELD_NUMBER: _ClassVar[int]
    TAG_FILTERS_FIELD_NUMBER: _ClassVar[int]
    name_prefix: str
    tag_filters: _containers.ScalarMap[str, str]
    def __init__(self, name_prefix: _Optional[str] = ..., tag_filters: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ListServicesResponse(_message.Message):
    __slots__ = ("services", "total_count")
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    services: _containers.RepeatedCompositeFieldContainer[ServiceInstance]
    total_count: int
    def __init__(self, services: _Optional[_Iterable[_Union[ServiceInstance, _Mapping]]] = ..., total_count: _Optional[int] = ...) -> None: ...

class ServiceSummary(_message.Message):
    __slots__ = ("service_name", "instance_count", "healthy_count", "versions")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    HEALTHY_COUNT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    instance_count: int
    healthy_count: int
    versions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, service_name: _Optional[str] = ..., instance_count: _Optional[int] = ..., healthy_count: _Optional[int] = ..., versions: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateServiceHealthRequest(_message.Message):
    __slots__ = ("service_name", "instance_id", "status", "health_message")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HEALTH_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    instance_id: str
    status: ServiceStatus
    health_message: str
    def __init__(self, service_name: _Optional[str] = ..., instance_id: _Optional[str] = ..., status: _Optional[_Union[ServiceStatus, str]] = ..., health_message: _Optional[str] = ...) -> None: ...

class UpdateServiceHealthResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class ServiceHealthCheckRequest(_message.Message):
    __slots__ = ("service_name", "instance_id")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    instance_id: str
    def __init__(self, service_name: _Optional[str] = ..., instance_id: _Optional[str] = ...) -> None: ...

class ServiceHealthCheckResponse(_message.Message):
    __slots__ = ("instance_healths",)
    INSTANCE_HEALTHS_FIELD_NUMBER: _ClassVar[int]
    instance_healths: _containers.RepeatedCompositeFieldContainer[ServiceInstanceHealth]
    def __init__(self, instance_healths: _Optional[_Iterable[_Union[ServiceInstanceHealth, _Mapping]]] = ...) -> None: ...

class ServiceInstanceHealth(_message.Message):
    __slots__ = ("instance", "status", "message", "last_check")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LAST_CHECK_FIELD_NUMBER: _ClassVar[int]
    instance: ServiceInstance
    status: ServiceStatus
    message: str
    last_check: _timestamp_pb2.Timestamp
    def __init__(self, instance: _Optional[_Union[ServiceInstance, _Mapping]] = ..., status: _Optional[_Union[ServiceStatus, str]] = ..., message: _Optional[str] = ..., last_check: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UploadServiceConfigRequest(_message.Message):
    __slots__ = ("service_name", "config_version", "config_data", "description")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
    CONFIG_DATA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    config_version: str
    config_data: _struct_pb2.Struct
    description: str
    def __init__(self, service_name: _Optional[str] = ..., config_version: _Optional[str] = ..., config_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., description: _Optional[str] = ...) -> None: ...

class UploadServiceConfigResponse(_message.Message):
    __slots__ = ("success", "message", "config_key")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_KEY_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    config_key: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., config_key: _Optional[str] = ...) -> None: ...

class GetServiceConfigRequest(_message.Message):
    __slots__ = ("service_name", "config_version")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    config_version: str
    def __init__(self, service_name: _Optional[str] = ..., config_version: _Optional[str] = ...) -> None: ...

class GetServiceConfigResponse(_message.Message):
    __slots__ = ("config_data", "config_version", "updated_at", "description")
    CONFIG_DATA_FIELD_NUMBER: _ClassVar[int]
    CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    config_data: _struct_pb2.Struct
    config_version: str
    updated_at: _timestamp_pb2.Timestamp
    description: str
    def __init__(self, config_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., config_version: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., description: _Optional[str] = ...) -> None: ...

class GetServiceRoutesRequest(_message.Message):
    __slots__ = ("service_name", "descriptor_version")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    descriptor_version: str
    def __init__(self, service_name: _Optional[str] = ..., descriptor_version: _Optional[str] = ...) -> None: ...

class ServiceRoute(_message.Message):
    __slots__ = ("http_method", "path", "service_name", "method_name", "source")
    HTTP_METHOD_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    METHOD_NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    http_method: str
    path: str
    service_name: str
    method_name: str
    source: str
    def __init__(self, http_method: _Optional[str] = ..., path: _Optional[str] = ..., service_name: _Optional[str] = ..., method_name: _Optional[str] = ..., source: _Optional[str] = ...) -> None: ...

class ServiceRouteDiagnostics(_message.Message):
    __slots__ = ("has_http_routes", "missing_http_extension", "services_without_http", "rest_route_count", "grpc_fallback_count")
    HAS_HTTP_ROUTES_FIELD_NUMBER: _ClassVar[int]
    MISSING_HTTP_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    SERVICES_WITHOUT_HTTP_FIELD_NUMBER: _ClassVar[int]
    REST_ROUTE_COUNT_FIELD_NUMBER: _ClassVar[int]
    GRPC_FALLBACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    has_http_routes: bool
    missing_http_extension: bool
    services_without_http: _containers.RepeatedScalarFieldContainer[str]
    rest_route_count: int
    grpc_fallback_count: int
    def __init__(self, has_http_routes: bool = ..., missing_http_extension: bool = ..., services_without_http: _Optional[_Iterable[str]] = ..., rest_route_count: _Optional[int] = ..., grpc_fallback_count: _Optional[int] = ...) -> None: ...

class GetServiceRoutesResponse(_message.Message):
    __slots__ = ("routes", "diagnostics", "descriptor_version")
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    routes: _containers.RepeatedCompositeFieldContainer[ServiceRoute]
    diagnostics: ServiceRouteDiagnostics
    descriptor_version: str
    def __init__(self, routes: _Optional[_Iterable[_Union[ServiceRoute, _Mapping]]] = ..., diagnostics: _Optional[_Union[ServiceRouteDiagnostics, _Mapping]] = ..., descriptor_version: _Optional[str] = ...) -> None: ...

class UploadProtobufDescriptorRequest(_message.Message):
    __slots__ = ("service_name", "descriptor_version", "descriptor_data", "description", "signature", "force", "previous_version")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_DATA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_VERSION_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    descriptor_version: str
    descriptor_data: bytes
    description: str
    signature: str
    force: bool
    previous_version: str
    def __init__(self, service_name: _Optional[str] = ..., descriptor_version: _Optional[str] = ..., descriptor_data: _Optional[bytes] = ..., description: _Optional[str] = ..., signature: _Optional[str] = ..., force: bool = ..., previous_version: _Optional[str] = ...) -> None: ...

class UploadProtobufDescriptorResponse(_message.Message):
    __slots__ = ("success", "message", "descriptor_key", "discovered_services", "compatibility_warnings", "applied_version", "descriptor_hash")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_KEY_FIELD_NUMBER: _ClassVar[int]
    DISCOVERED_SERVICES_FIELD_NUMBER: _ClassVar[int]
    COMPATIBILITY_WARNINGS_FIELD_NUMBER: _ClassVar[int]
    APPLIED_VERSION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_HASH_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    descriptor_key: str
    discovered_services: _containers.RepeatedScalarFieldContainer[str]
    compatibility_warnings: _containers.RepeatedScalarFieldContainer[str]
    applied_version: str
    descriptor_hash: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., descriptor_key: _Optional[str] = ..., discovered_services: _Optional[_Iterable[str]] = ..., compatibility_warnings: _Optional[_Iterable[str]] = ..., applied_version: _Optional[str] = ..., descriptor_hash: _Optional[str] = ...) -> None: ...

class GetProtobufDescriptorRequest(_message.Message):
    __slots__ = ("service_name", "descriptor_version")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    descriptor_version: str
    def __init__(self, service_name: _Optional[str] = ..., descriptor_version: _Optional[str] = ...) -> None: ...

class GetProtobufDescriptorResponse(_message.Message):
    __slots__ = ("descriptor_data", "descriptor_version", "updated_at", "description", "services")
    DESCRIPTOR_DATA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    descriptor_data: bytes
    descriptor_version: str
    updated_at: _timestamp_pb2.Timestamp
    description: str
    services: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, descriptor_data: _Optional[bytes] = ..., descriptor_version: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., description: _Optional[str] = ..., services: _Optional[_Iterable[str]] = ...) -> None: ...

class ListProtobufDescriptorsRequest(_message.Message):
    __slots__ = ("service_name_prefix",)
    SERVICE_NAME_PREFIX_FIELD_NUMBER: _ClassVar[int]
    service_name_prefix: str
    def __init__(self, service_name_prefix: _Optional[str] = ...) -> None: ...

class ListProtobufDescriptorsResponse(_message.Message):
    __slots__ = ("descriptors",)
    DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    descriptors: _containers.RepeatedCompositeFieldContainer[ProtobufDescriptorInfo]
    def __init__(self, descriptors: _Optional[_Iterable[_Union[ProtobufDescriptorInfo, _Mapping]]] = ...) -> None: ...

class ProtobufDescriptorInfo(_message.Message):
    __slots__ = ("service_name", "descriptor_version", "updated_at", "description", "services", "size_bytes", "descriptor_hash", "is_active")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_HASH_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    descriptor_version: str
    updated_at: _timestamp_pb2.Timestamp
    description: str
    services: _containers.RepeatedScalarFieldContainer[str]
    size_bytes: int
    descriptor_hash: str
    is_active: bool
    def __init__(self, service_name: _Optional[str] = ..., descriptor_version: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., description: _Optional[str] = ..., services: _Optional[_Iterable[str]] = ..., size_bytes: _Optional[int] = ..., descriptor_hash: _Optional[str] = ..., is_active: bool = ...) -> None: ...

class DescriptorVersionInfo(_message.Message):
    __slots__ = ("version", "descriptor_hash", "created_at", "description", "services", "size_bytes", "is_active")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_HASH_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    version: str
    descriptor_hash: str
    created_at: _timestamp_pb2.Timestamp
    description: str
    services: _containers.RepeatedScalarFieldContainer[str]
    size_bytes: int
    is_active: bool
    def __init__(self, version: _Optional[str] = ..., descriptor_hash: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., description: _Optional[str] = ..., services: _Optional[_Iterable[str]] = ..., size_bytes: _Optional[int] = ..., is_active: bool = ...) -> None: ...

class RollbackDescriptorRequest(_message.Message):
    __slots__ = ("service_name", "target_version")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_VERSION_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    target_version: str
    def __init__(self, service_name: _Optional[str] = ..., target_version: _Optional[str] = ...) -> None: ...

class RollbackDescriptorResponse(_message.Message):
    __slots__ = ("success", "message", "active_version", "discovered_services")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_VERSION_FIELD_NUMBER: _ClassVar[int]
    DISCOVERED_SERVICES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    active_version: str
    discovered_services: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., active_version: _Optional[str] = ..., discovered_services: _Optional[_Iterable[str]] = ...) -> None: ...

class ListDescriptorVersionsRequest(_message.Message):
    __slots__ = ("service_name",)
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    def __init__(self, service_name: _Optional[str] = ...) -> None: ...

class ListDescriptorVersionsResponse(_message.Message):
    __slots__ = ("versions", "active_version")
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_VERSION_FIELD_NUMBER: _ClassVar[int]
    versions: _containers.RepeatedCompositeFieldContainer[DescriptorVersionInfo]
    active_version: str
    def __init__(self, versions: _Optional[_Iterable[_Union[DescriptorVersionInfo, _Mapping]]] = ..., active_version: _Optional[str] = ...) -> None: ...

from google.api import annotations_pb2 as _annotations_pb2
from google.api import http_pb2 as _http_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

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

class EntitlementPlan(_message.Message):
    __slots__ = ("id", "business_id", "name", "description", "is_active", "sort_order", "features", "quotas", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    QUOTAS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    business_id: str
    name: str
    description: str
    is_active: bool
    sort_order: int
    features: _containers.RepeatedCompositeFieldContainer[PlanFeature]
    quotas: _containers.RepeatedCompositeFieldContainer[PlanQuota]
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., business_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_active: bool = ..., sort_order: _Optional[int] = ..., features: _Optional[_Iterable[_Union[PlanFeature, _Mapping]]] = ..., quotas: _Optional[_Iterable[_Union[PlanQuota, _Mapping]]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PlanFeature(_message.Message):
    __slots__ = ("feature_key", "enabled", "config")
    FEATURE_KEY_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    feature_key: str
    enabled: bool
    config: _struct_pb2.Struct
    def __init__(self, feature_key: _Optional[str] = ..., enabled: bool = ..., config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class PlanQuota(_message.Message):
    __slots__ = ("quota_key", "quota_limit", "quota_unit", "reset_period")
    QUOTA_KEY_FIELD_NUMBER: _ClassVar[int]
    QUOTA_LIMIT_FIELD_NUMBER: _ClassVar[int]
    QUOTA_UNIT_FIELD_NUMBER: _ClassVar[int]
    RESET_PERIOD_FIELD_NUMBER: _ClassVar[int]
    quota_key: str
    quota_limit: int
    quota_unit: str
    reset_period: str
    def __init__(self, quota_key: _Optional[str] = ..., quota_limit: _Optional[int] = ..., quota_unit: _Optional[str] = ..., reset_period: _Optional[str] = ...) -> None: ...

class Subscription(_message.Message):
    __slots__ = ("id", "business_id", "subject_id", "subject_type", "plan_id", "status", "billing_cycle", "current_period_start", "current_period_end", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BILLING_CYCLE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    business_id: str
    subject_id: str
    subject_type: int
    plan_id: str
    status: str
    billing_cycle: str
    current_period_start: int
    current_period_end: int
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[int] = ..., plan_id: _Optional[str] = ..., status: _Optional[str] = ..., billing_cycle: _Optional[str] = ..., current_period_start: _Optional[int] = ..., current_period_end: _Optional[int] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class QuotaUsage(_message.Message):
    __slots__ = ("business_id", "subject_id", "quota_key", "period_start", "period_end", "used")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    QUOTA_KEY_FIELD_NUMBER: _ClassVar[int]
    PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    quota_key: str
    period_start: int
    period_end: int
    used: int
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., quota_key: _Optional[str] = ..., period_start: _Optional[int] = ..., period_end: _Optional[int] = ..., used: _Optional[int] = ...) -> None: ...

class CreatePlanRequest(_message.Message):
    __slots__ = ("business_id", "name", "description", "is_active", "sort_order", "features", "quotas", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    QUOTAS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    name: str
    description: str
    is_active: bool
    sort_order: int
    features: _containers.RepeatedCompositeFieldContainer[PlanFeature]
    quotas: _containers.RepeatedCompositeFieldContainer[PlanQuota]
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, business_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_active: bool = ..., sort_order: _Optional[int] = ..., features: _Optional[_Iterable[_Union[PlanFeature, _Mapping]]] = ..., quotas: _Optional[_Iterable[_Union[PlanQuota, _Mapping]]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class GetPlanRequest(_message.Message):
    __slots__ = ("business_id", "plan_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    plan_id: str
    def __init__(self, business_id: _Optional[str] = ..., plan_id: _Optional[str] = ...) -> None: ...

class ListPlansRequest(_message.Message):
    __slots__ = ("business_id", "active_only")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ONLY_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    active_only: bool
    def __init__(self, business_id: _Optional[str] = ..., active_only: bool = ...) -> None: ...

class ListPlansResponse(_message.Message):
    __slots__ = ("plans",)
    PLANS_FIELD_NUMBER: _ClassVar[int]
    plans: _containers.RepeatedCompositeFieldContainer[EntitlementPlan]
    def __init__(self, plans: _Optional[_Iterable[_Union[EntitlementPlan, _Mapping]]] = ...) -> None: ...

class UpdatePlanRequest(_message.Message):
    __slots__ = ("business_id", "plan_id", "name", "description", "is_active", "sort_order", "features", "quotas", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    QUOTAS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    plan_id: str
    name: str
    description: str
    is_active: bool
    sort_order: int
    features: _containers.RepeatedCompositeFieldContainer[PlanFeature]
    quotas: _containers.RepeatedCompositeFieldContainer[PlanQuota]
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, business_id: _Optional[str] = ..., plan_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_active: bool = ..., sort_order: _Optional[int] = ..., features: _Optional[_Iterable[_Union[PlanFeature, _Mapping]]] = ..., quotas: _Optional[_Iterable[_Union[PlanQuota, _Mapping]]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CreateSubscriptionRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "subject_type", "plan_id", "billing_cycle", "current_period_start", "current_period_end", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    BILLING_CYCLE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    subject_type: int
    plan_id: str
    billing_cycle: str
    current_period_start: int
    current_period_end: int
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[int] = ..., plan_id: _Optional[str] = ..., billing_cycle: _Optional[str] = ..., current_period_start: _Optional[int] = ..., current_period_end: _Optional[int] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class GetSubscriptionRequest(_message.Message):
    __slots__ = ("business_id", "subscription_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subscription_id: str
    def __init__(self, business_id: _Optional[str] = ..., subscription_id: _Optional[str] = ...) -> None: ...

class GetSubscriptionBySubjectRequest(_message.Message):
    __slots__ = ("business_id", "subject_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ...) -> None: ...

class UpdateSubscriptionRequest(_message.Message):
    __slots__ = ("business_id", "subscription_id", "plan_id", "status", "billing_cycle", "current_period_start", "current_period_end", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BILLING_CYCLE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subscription_id: str
    plan_id: str
    status: str
    billing_cycle: str
    current_period_start: int
    current_period_end: int
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, business_id: _Optional[str] = ..., subscription_id: _Optional[str] = ..., plan_id: _Optional[str] = ..., status: _Optional[str] = ..., billing_cycle: _Optional[str] = ..., current_period_start: _Optional[int] = ..., current_period_end: _Optional[int] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CancelSubscriptionRequest(_message.Message):
    __slots__ = ("business_id", "subscription_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subscription_id: str
    def __init__(self, business_id: _Optional[str] = ..., subscription_id: _Optional[str] = ...) -> None: ...

class GetQuotaUsageRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "quota_key")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    QUOTA_KEY_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    quota_key: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., quota_key: _Optional[str] = ...) -> None: ...

class IncrementQuotaRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "quota_key", "delta")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    QUOTA_KEY_FIELD_NUMBER: _ClassVar[int]
    DELTA_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    quota_key: str
    delta: int
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., quota_key: _Optional[str] = ..., delta: _Optional[int] = ...) -> None: ...

class CheckQuotaRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "quota_key")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    QUOTA_KEY_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    quota_key: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., quota_key: _Optional[str] = ...) -> None: ...

class CheckQuotaResponse(_message.Message):
    __slots__ = ("used", "limit")
    USED_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    used: int
    limit: int
    def __init__(self, used: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class ResolvedEntitlementResponse(_message.Message):
    __slots__ = ("subscription", "plan", "quota_usages")
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    QUOTA_USAGES_FIELD_NUMBER: _ClassVar[int]
    subscription: Subscription
    plan: EntitlementPlan
    quota_usages: _containers.RepeatedCompositeFieldContainer[QuotaUsage]
    def __init__(self, subscription: _Optional[_Union[Subscription, _Mapping]] = ..., plan: _Optional[_Union[EntitlementPlan, _Mapping]] = ..., quota_usages: _Optional[_Iterable[_Union[QuotaUsage, _Mapping]]] = ...) -> None: ...

class GetMyEntitlementRequest(_message.Message):
    __slots__ = ("business_id", "subject_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ...) -> None: ...

class CheckFeatureRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "feature_key")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_KEY_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    feature_key: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., feature_key: _Optional[str] = ...) -> None: ...

class CheckFeatureResponse(_message.Message):
    __slots__ = ("enabled", "feature_key", "plan_id", "config")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    FEATURE_KEY_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    feature_key: str
    plan_id: str
    config: _struct_pb2.Struct
    def __init__(self, enabled: bool = ..., feature_key: _Optional[str] = ..., plan_id: _Optional[str] = ..., config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

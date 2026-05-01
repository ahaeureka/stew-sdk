import datetime

from google.api import annotations_pb2 as _annotations_pb2
from google.api import http_pb2 as _http_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntitlementPlan(_message.Message):
    __slots__ = ("id", "business_id", "name", "description", "is_active", "sort_order", "features", "quotas", "metadata", "created_at", "updated_at", "deleted_at", "localized_name", "localized_description")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class LocalizedNameEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class LocalizedDescriptionEntry(_message.Message):
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
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    LOCALIZED_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCALIZED_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    business_id: str
    name: str
    description: str
    is_active: bool
    sort_order: int
    features: _containers.RepeatedCompositeFieldContainer[PlanFeature]
    quotas: _containers.RepeatedCompositeFieldContainer[PlanQuota]
    metadata: _containers.ScalarMap[str, str]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    localized_name: _containers.ScalarMap[str, str]
    localized_description: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., business_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_active: bool = ..., sort_order: _Optional[int] = ..., features: _Optional[_Iterable[_Union[PlanFeature, _Mapping]]] = ..., quotas: _Optional[_Iterable[_Union[PlanQuota, _Mapping]]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., localized_name: _Optional[_Mapping[str, str]] = ..., localized_description: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PlanFeature(_message.Message):
    __slots__ = ("feature_key", "enabled", "config", "feature_display_name", "created_at", "updated_at", "deleted_at", "localized_display_name")
    class LocalizedDisplayNameEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FEATURE_KEY_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    FEATURE_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    LOCALIZED_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    feature_key: str
    enabled: bool
    config: _struct_pb2.Struct
    feature_display_name: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    localized_display_name: _containers.ScalarMap[str, str]
    def __init__(self, feature_key: _Optional[str] = ..., enabled: bool = ..., config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., feature_display_name: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., localized_display_name: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PlanQuota(_message.Message):
    __slots__ = ("quota_key", "quota_limit", "quota_unit", "reset_period", "quota_display_name", "created_at", "updated_at", "deleted_at", "localized_display_name")
    class LocalizedDisplayNameEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    QUOTA_KEY_FIELD_NUMBER: _ClassVar[int]
    QUOTA_LIMIT_FIELD_NUMBER: _ClassVar[int]
    QUOTA_UNIT_FIELD_NUMBER: _ClassVar[int]
    RESET_PERIOD_FIELD_NUMBER: _ClassVar[int]
    QUOTA_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    LOCALIZED_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    quota_key: str
    quota_limit: int
    quota_unit: str
    reset_period: str
    quota_display_name: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    localized_display_name: _containers.ScalarMap[str, str]
    def __init__(self, quota_key: _Optional[str] = ..., quota_limit: _Optional[int] = ..., quota_unit: _Optional[str] = ..., reset_period: _Optional[str] = ..., quota_display_name: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., localized_display_name: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Subscription(_message.Message):
    __slots__ = ("id", "business_id", "subject_id", "subject_type", "plan_id", "status", "billing_cycle", "current_period_start", "current_period_end", "metadata", "created_at", "updated_at", "deleted_at")
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
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
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
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[int] = ..., plan_id: _Optional[str] = ..., status: _Optional[str] = ..., billing_cycle: _Optional[str] = ..., current_period_start: _Optional[int] = ..., current_period_end: _Optional[int] = ..., metadata: _Optional[_Mapping[str, str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class QuotaUsage(_message.Message):
    __slots__ = ("business_id", "subject_id", "quota_key", "period_start", "period_end", "used", "quota_display_name", "created_at", "updated_at", "deleted_at", "localized_display_name")
    class LocalizedDisplayNameEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    QUOTA_KEY_FIELD_NUMBER: _ClassVar[int]
    PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    QUOTA_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    LOCALIZED_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    quota_key: str
    period_start: int
    period_end: int
    used: int
    quota_display_name: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    localized_display_name: _containers.ScalarMap[str, str]
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., quota_key: _Optional[str] = ..., period_start: _Optional[int] = ..., period_end: _Optional[int] = ..., used: _Optional[int] = ..., quota_display_name: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., localized_display_name: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CreatePlanRequest(_message.Message):
    __slots__ = ("business_id", "name", "description", "is_active", "sort_order", "features", "quotas", "metadata", "localized_name", "localized_description")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class LocalizedNameEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class LocalizedDescriptionEntry(_message.Message):
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
    LOCALIZED_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCALIZED_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    name: str
    description: str
    is_active: bool
    sort_order: int
    features: _containers.RepeatedCompositeFieldContainer[PlanFeature]
    quotas: _containers.RepeatedCompositeFieldContainer[PlanQuota]
    metadata: _containers.ScalarMap[str, str]
    localized_name: _containers.ScalarMap[str, str]
    localized_description: _containers.ScalarMap[str, str]
    def __init__(self, business_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_active: bool = ..., sort_order: _Optional[int] = ..., features: _Optional[_Iterable[_Union[PlanFeature, _Mapping]]] = ..., quotas: _Optional[_Iterable[_Union[PlanQuota, _Mapping]]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., localized_name: _Optional[_Mapping[str, str]] = ..., localized_description: _Optional[_Mapping[str, str]] = ...) -> None: ...

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
    __slots__ = ("business_id", "plan_id", "name", "description", "is_active", "sort_order", "features", "quotas", "metadata", "localized_name", "localized_description")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class LocalizedNameEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class LocalizedDescriptionEntry(_message.Message):
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
    LOCALIZED_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCALIZED_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    plan_id: str
    name: str
    description: str
    is_active: bool
    sort_order: int
    features: _containers.RepeatedCompositeFieldContainer[PlanFeature]
    quotas: _containers.RepeatedCompositeFieldContainer[PlanQuota]
    metadata: _containers.ScalarMap[str, str]
    localized_name: _containers.ScalarMap[str, str]
    localized_description: _containers.ScalarMap[str, str]
    def __init__(self, business_id: _Optional[str] = ..., plan_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_active: bool = ..., sort_order: _Optional[int] = ..., features: _Optional[_Iterable[_Union[PlanFeature, _Mapping]]] = ..., quotas: _Optional[_Iterable[_Union[PlanQuota, _Mapping]]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., localized_name: _Optional[_Mapping[str, str]] = ..., localized_description: _Optional[_Mapping[str, str]] = ...) -> None: ...

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

class DeleteSubscriptionRequest(_message.Message):
    __slots__ = ("business_id", "subscription_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subscription_id: str
    def __init__(self, business_id: _Optional[str] = ..., subscription_id: _Optional[str] = ...) -> None: ...

class ListSubscriptionsRequest(_message.Message):
    __slots__ = ("business_id", "status", "plan_id", "page_size", "page_token")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    status: str
    plan_id: str
    page_size: int
    page_token: str
    def __init__(self, business_id: _Optional[str] = ..., status: _Optional[str] = ..., plan_id: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListSubscriptionsResponse(_message.Message):
    __slots__ = ("subscriptions", "next_page_token")
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    subscriptions: _containers.RepeatedCompositeFieldContainer[Subscription]
    next_page_token: str
    def __init__(self, subscriptions: _Optional[_Iterable[_Union[Subscription, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class RenewSubscriptionsRequest(_message.Message):
    __slots__ = ("subscription_ids", "horizon_seconds")
    SUBSCRIPTION_IDS_FIELD_NUMBER: _ClassVar[int]
    HORIZON_SECONDS_FIELD_NUMBER: _ClassVar[int]
    subscription_ids: _containers.RepeatedScalarFieldContainer[str]
    horizon_seconds: int
    def __init__(self, subscription_ids: _Optional[_Iterable[str]] = ..., horizon_seconds: _Optional[int] = ...) -> None: ...

class RenewSubscriptionResult(_message.Message):
    __slots__ = ("subscription_id", "succeeded", "error_message", "subscription")
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    subscription_id: str
    succeeded: bool
    error_message: str
    subscription: Subscription
    def __init__(self, subscription_id: _Optional[str] = ..., succeeded: bool = ..., error_message: _Optional[str] = ..., subscription: _Optional[_Union[Subscription, _Mapping]] = ...) -> None: ...

class RenewSubscriptionsResponse(_message.Message):
    __slots__ = ("results", "succeeded_count", "failed_count")
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_COUNT_FIELD_NUMBER: _ClassVar[int]
    FAILED_COUNT_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[RenewSubscriptionResult]
    succeeded_count: int
    failed_count: int
    def __init__(self, results: _Optional[_Iterable[_Union[RenewSubscriptionResult, _Mapping]]] = ..., succeeded_count: _Optional[int] = ..., failed_count: _Optional[int] = ...) -> None: ...

class DeletePlanRequest(_message.Message):
    __slots__ = ("business_id", "plan_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    plan_id: str
    def __init__(self, business_id: _Optional[str] = ..., plan_id: _Optional[str] = ...) -> None: ...

class UpsertPlanFeatureRequest(_message.Message):
    __slots__ = ("business_id", "plan_id", "feature")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    plan_id: str
    feature: PlanFeature
    def __init__(self, business_id: _Optional[str] = ..., plan_id: _Optional[str] = ..., feature: _Optional[_Union[PlanFeature, _Mapping]] = ...) -> None: ...

class DeletePlanFeatureRequest(_message.Message):
    __slots__ = ("business_id", "plan_id", "feature_key")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_KEY_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    plan_id: str
    feature_key: str
    def __init__(self, business_id: _Optional[str] = ..., plan_id: _Optional[str] = ..., feature_key: _Optional[str] = ...) -> None: ...

class UpsertPlanQuotaRequest(_message.Message):
    __slots__ = ("business_id", "plan_id", "quota")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    QUOTA_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    plan_id: str
    quota: PlanQuota
    def __init__(self, business_id: _Optional[str] = ..., plan_id: _Optional[str] = ..., quota: _Optional[_Union[PlanQuota, _Mapping]] = ...) -> None: ...

class DeletePlanQuotaRequest(_message.Message):
    __slots__ = ("business_id", "plan_id", "quota_key")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    QUOTA_KEY_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    plan_id: str
    quota_key: str
    def __init__(self, business_id: _Optional[str] = ..., plan_id: _Optional[str] = ..., quota_key: _Optional[str] = ...) -> None: ...

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

class PlanChangeRecord(_message.Message):
    __slots__ = ("id", "business_id", "subscription_id", "subject_id", "previous_plan_id", "new_plan_id", "change_type", "change_mode", "status", "effective_at", "executed_at", "metadata", "created_at", "updated_at", "deleted_at")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHANGE_MODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_AT_FIELD_NUMBER: _ClassVar[int]
    EXECUTED_AT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    business_id: str
    subscription_id: str
    subject_id: str
    previous_plan_id: str
    new_plan_id: str
    change_type: str
    change_mode: str
    status: str
    effective_at: int
    executed_at: int
    metadata: _containers.ScalarMap[str, str]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., business_id: _Optional[str] = ..., subscription_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., previous_plan_id: _Optional[str] = ..., new_plan_id: _Optional[str] = ..., change_type: _Optional[str] = ..., change_mode: _Optional[str] = ..., status: _Optional[str] = ..., effective_at: _Optional[int] = ..., executed_at: _Optional[int] = ..., metadata: _Optional[_Mapping[str, str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ChangePlanRequest(_message.Message):
    __slots__ = ("business_id", "subscription_id", "subject_id", "new_plan_id", "change_mode", "reset_quota", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    CHANGE_MODE_FIELD_NUMBER: _ClassVar[int]
    RESET_QUOTA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subscription_id: str
    subject_id: str
    new_plan_id: str
    change_mode: str
    reset_quota: bool
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, business_id: _Optional[str] = ..., subscription_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., new_plan_id: _Optional[str] = ..., change_mode: _Optional[str] = ..., reset_quota: bool = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ChangePlanResponse(_message.Message):
    __slots__ = ("subscription", "change_record")
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CHANGE_RECORD_FIELD_NUMBER: _ClassVar[int]
    subscription: Subscription
    change_record: PlanChangeRecord
    def __init__(self, subscription: _Optional[_Union[Subscription, _Mapping]] = ..., change_record: _Optional[_Union[PlanChangeRecord, _Mapping]] = ...) -> None: ...

class ListPlanChangesRequest(_message.Message):
    __slots__ = ("business_id", "subscription_id", "subject_id", "page_size", "page_token")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subscription_id: str
    subject_id: str
    page_size: int
    page_token: str
    def __init__(self, business_id: _Optional[str] = ..., subscription_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListPlanChangesResponse(_message.Message):
    __slots__ = ("changes", "next_page_token")
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    changes: _containers.RepeatedCompositeFieldContainer[PlanChangeRecord]
    next_page_token: str
    def __init__(self, changes: _Optional[_Iterable[_Union[PlanChangeRecord, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class CancelPlanChangeRequest(_message.Message):
    __slots__ = ("business_id", "change_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    CHANGE_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    change_id: str
    def __init__(self, business_id: _Optional[str] = ..., change_id: _Optional[str] = ...) -> None: ...

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
    __slots__ = ("enabled", "feature_key", "plan_id", "config", "feature_display_name", "localized_display_name")
    class LocalizedDisplayNameEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    FEATURE_KEY_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    FEATURE_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCALIZED_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    feature_key: str
    plan_id: str
    config: _struct_pb2.Struct
    feature_display_name: str
    localized_display_name: _containers.ScalarMap[str, str]
    def __init__(self, enabled: bool = ..., feature_key: _Optional[str] = ..., plan_id: _Optional[str] = ..., config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., feature_display_name: _Optional[str] = ..., localized_display_name: _Optional[_Mapping[str, str]] = ...) -> None: ...

import datetime

from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BillingSubjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_SUBJECT_TYPE_UNSPECIFIED: _ClassVar[BillingSubjectType]
    BILLING_SUBJECT_TYPE_USER: _ClassVar[BillingSubjectType]
    BILLING_SUBJECT_TYPE_API_KEY: _ClassVar[BillingSubjectType]
    BILLING_SUBJECT_TYPE_ORG: _ClassVar[BillingSubjectType]
    BILLING_SUBJECT_TYPE_PROJECT: _ClassVar[BillingSubjectType]

class BillingPreauthMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_PREAUTH_MODE_UNSPECIFIED: _ClassVar[BillingPreauthMode]
    BILLING_PREAUTH_MODE_REQUIRED: _ClassVar[BillingPreauthMode]
    BILLING_PREAUTH_MODE_BEST_EFFORT: _ClassVar[BillingPreauthMode]
    BILLING_PREAUTH_MODE_DISABLED: _ClassVar[BillingPreauthMode]

class BillingMissingReportAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_MISSING_REPORT_ACTION_UNSPECIFIED: _ClassVar[BillingMissingReportAction]
    BILLING_MISSING_REPORT_ACTION_RELEASE: _ClassVar[BillingMissingReportAction]
    BILLING_MISSING_REPORT_ACTION_MARK_PENDING: _ClassVar[BillingMissingReportAction]
    BILLING_MISSING_REPORT_ACTION_CAPTURE_ESTIMATE: _ClassVar[BillingMissingReportAction]

class BillingReportTransport(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_REPORT_TRANSPORT_UNSPECIFIED: _ClassVar[BillingReportTransport]
    BILLING_REPORT_TRANSPORT_HEADER: _ClassVar[BillingReportTransport]
    BILLING_REPORT_TRANSPORT_TRAILER: _ClassVar[BillingReportTransport]
    BILLING_REPORT_TRANSPORT_BOTH: _ClassVar[BillingReportTransport]

class BillingFinalStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_FINAL_STATUS_UNSPECIFIED: _ClassVar[BillingFinalStatus]
    BILLING_FINAL_STATUS_SUCCESS: _ClassVar[BillingFinalStatus]
    BILLING_FINAL_STATUS_FAILED: _ClassVar[BillingFinalStatus]
    BILLING_FINAL_STATUS_COMPENSATED: _ClassVar[BillingFinalStatus]

class BillingUsageSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_USAGE_SOURCE_UNSPECIFIED: _ClassVar[BillingUsageSource]
    BILLING_USAGE_SOURCE_ESTIMATED: _ClassVar[BillingUsageSource]
    BILLING_USAGE_SOURCE_ACTUAL: _ClassVar[BillingUsageSource]

class BillingTransactionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_TRANSACTION_TYPE_UNSPECIFIED: _ClassVar[BillingTransactionType]
    BILLING_TRANSACTION_TYPE_AUTHORIZE: _ClassVar[BillingTransactionType]
    BILLING_TRANSACTION_TYPE_CAPTURE: _ClassVar[BillingTransactionType]
    BILLING_TRANSACTION_TYPE_RELEASE: _ClassVar[BillingTransactionType]
    BILLING_TRANSACTION_TYPE_REFUND: _ClassVar[BillingTransactionType]
    BILLING_TRANSACTION_TYPE_EXPIRE: _ClassVar[BillingTransactionType]
    BILLING_TRANSACTION_TYPE_GRANT: _ClassVar[BillingTransactionType]
    BILLING_TRANSACTION_TYPE_COMPENSATION: _ClassVar[BillingTransactionType]
BILLING_SUBJECT_TYPE_UNSPECIFIED: BillingSubjectType
BILLING_SUBJECT_TYPE_USER: BillingSubjectType
BILLING_SUBJECT_TYPE_API_KEY: BillingSubjectType
BILLING_SUBJECT_TYPE_ORG: BillingSubjectType
BILLING_SUBJECT_TYPE_PROJECT: BillingSubjectType
BILLING_PREAUTH_MODE_UNSPECIFIED: BillingPreauthMode
BILLING_PREAUTH_MODE_REQUIRED: BillingPreauthMode
BILLING_PREAUTH_MODE_BEST_EFFORT: BillingPreauthMode
BILLING_PREAUTH_MODE_DISABLED: BillingPreauthMode
BILLING_MISSING_REPORT_ACTION_UNSPECIFIED: BillingMissingReportAction
BILLING_MISSING_REPORT_ACTION_RELEASE: BillingMissingReportAction
BILLING_MISSING_REPORT_ACTION_MARK_PENDING: BillingMissingReportAction
BILLING_MISSING_REPORT_ACTION_CAPTURE_ESTIMATE: BillingMissingReportAction
BILLING_REPORT_TRANSPORT_UNSPECIFIED: BillingReportTransport
BILLING_REPORT_TRANSPORT_HEADER: BillingReportTransport
BILLING_REPORT_TRANSPORT_TRAILER: BillingReportTransport
BILLING_REPORT_TRANSPORT_BOTH: BillingReportTransport
BILLING_FINAL_STATUS_UNSPECIFIED: BillingFinalStatus
BILLING_FINAL_STATUS_SUCCESS: BillingFinalStatus
BILLING_FINAL_STATUS_FAILED: BillingFinalStatus
BILLING_FINAL_STATUS_COMPENSATED: BillingFinalStatus
BILLING_USAGE_SOURCE_UNSPECIFIED: BillingUsageSource
BILLING_USAGE_SOURCE_ESTIMATED: BillingUsageSource
BILLING_USAGE_SOURCE_ACTUAL: BillingUsageSource
BILLING_TRANSACTION_TYPE_UNSPECIFIED: BillingTransactionType
BILLING_TRANSACTION_TYPE_AUTHORIZE: BillingTransactionType
BILLING_TRANSACTION_TYPE_CAPTURE: BillingTransactionType
BILLING_TRANSACTION_TYPE_RELEASE: BillingTransactionType
BILLING_TRANSACTION_TYPE_REFUND: BillingTransactionType
BILLING_TRANSACTION_TYPE_EXPIRE: BillingTransactionType
BILLING_TRANSACTION_TYPE_GRANT: BillingTransactionType
BILLING_TRANSACTION_TYPE_COMPENSATION: BillingTransactionType

class ServiceBillingConfig(_message.Message):
    __slots__ = ("enabled", "business_id", "policy_id", "subject_mode", "preauth_mode", "allow_anonymous_subject", "missing_report_action", "release_timeout_seconds", "report_transport", "report_header_prefix", "factor_schema_version", "max_reservation_ttl_seconds", "idempotency_window_seconds", "capture_requires_report", "reconcile_scan_interval_seconds", "max_report_size_bytes", "strict_policy_snapshot")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_MODE_FIELD_NUMBER: _ClassVar[int]
    PREAUTH_MODE_FIELD_NUMBER: _ClassVar[int]
    ALLOW_ANONYMOUS_SUBJECT_FIELD_NUMBER: _ClassVar[int]
    MISSING_REPORT_ACTION_FIELD_NUMBER: _ClassVar[int]
    RELEASE_TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    REPORT_TRANSPORT_FIELD_NUMBER: _ClassVar[int]
    REPORT_HEADER_PREFIX_FIELD_NUMBER: _ClassVar[int]
    FACTOR_SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    MAX_RESERVATION_TTL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_WINDOW_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_REQUIRES_REPORT_FIELD_NUMBER: _ClassVar[int]
    RECONCILE_SCAN_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    MAX_REPORT_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    STRICT_POLICY_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    business_id: str
    policy_id: str
    subject_mode: BillingSubjectType
    preauth_mode: BillingPreauthMode
    allow_anonymous_subject: bool
    missing_report_action: BillingMissingReportAction
    release_timeout_seconds: int
    report_transport: BillingReportTransport
    report_header_prefix: str
    factor_schema_version: str
    max_reservation_ttl_seconds: int
    idempotency_window_seconds: int
    capture_requires_report: bool
    reconcile_scan_interval_seconds: int
    max_report_size_bytes: int
    strict_policy_snapshot: bool
    def __init__(self, enabled: bool = ..., business_id: _Optional[str] = ..., policy_id: _Optional[str] = ..., subject_mode: _Optional[_Union[BillingSubjectType, str]] = ..., preauth_mode: _Optional[_Union[BillingPreauthMode, str]] = ..., allow_anonymous_subject: bool = ..., missing_report_action: _Optional[_Union[BillingMissingReportAction, str]] = ..., release_timeout_seconds: _Optional[int] = ..., report_transport: _Optional[_Union[BillingReportTransport, str]] = ..., report_header_prefix: _Optional[str] = ..., factor_schema_version: _Optional[str] = ..., max_reservation_ttl_seconds: _Optional[int] = ..., idempotency_window_seconds: _Optional[int] = ..., capture_requires_report: bool = ..., reconcile_scan_interval_seconds: _Optional[int] = ..., max_report_size_bytes: _Optional[int] = ..., strict_policy_snapshot: bool = ...) -> None: ...

class AuthorizationContext(_message.Message):
    __slots__ = ("business_id", "user_id", "authorization_id", "request_id", "policy_id", "subject_id", "subject_type", "factor_schema_version")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FACTOR_SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    user_id: str
    authorization_id: str
    request_id: str
    policy_id: str
    subject_id: str
    subject_type: BillingSubjectType
    factor_schema_version: str
    def __init__(self, business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., policy_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., factor_schema_version: _Optional[str] = ...) -> None: ...

class BillingUsageTotals(_message.Message):
    __slots__ = ("prompt_tokens", "completion_tokens", "embedding_tokens", "ocr_pages", "asr_minutes", "infra_units")
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_TOKENS_FIELD_NUMBER: _ClassVar[int]
    OCR_PAGES_FIELD_NUMBER: _ClassVar[int]
    ASR_MINUTES_FIELD_NUMBER: _ClassVar[int]
    INFRA_UNITS_FIELD_NUMBER: _ClassVar[int]
    prompt_tokens: int
    completion_tokens: int
    embedding_tokens: int
    ocr_pages: int
    asr_minutes: int
    infra_units: int
    def __init__(self, prompt_tokens: _Optional[int] = ..., completion_tokens: _Optional[int] = ..., embedding_tokens: _Optional[int] = ..., ocr_pages: _Optional[int] = ..., asr_minutes: _Optional[int] = ..., infra_units: _Optional[int] = ...) -> None: ...

class BillingCostBreakdown(_message.Message):
    __slots__ = ("chat_in_micros", "chat_out_micros", "embed_micros", "media_micros", "infra_micros")
    CHAT_IN_MICROS_FIELD_NUMBER: _ClassVar[int]
    CHAT_OUT_MICROS_FIELD_NUMBER: _ClassVar[int]
    EMBED_MICROS_FIELD_NUMBER: _ClassVar[int]
    MEDIA_MICROS_FIELD_NUMBER: _ClassVar[int]
    INFRA_MICROS_FIELD_NUMBER: _ClassVar[int]
    chat_in_micros: int
    chat_out_micros: int
    embed_micros: int
    media_micros: int
    infra_micros: int
    def __init__(self, chat_in_micros: _Optional[int] = ..., chat_out_micros: _Optional[int] = ..., embed_micros: _Optional[int] = ..., media_micros: _Optional[int] = ..., infra_micros: _Optional[int] = ...) -> None: ...

class BillingReport(_message.Message):
    __slots__ = ("business_id", "authorization_id", "request_id", "user_id", "usage_source", "final_status", "raw_usage_totals", "cost_breakdown", "business_factors", "billed_points_candidate", "refund_reason", "dedupe_key")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USAGE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    FINAL_STATUS_FIELD_NUMBER: _ClassVar[int]
    RAW_USAGE_TOTALS_FIELD_NUMBER: _ClassVar[int]
    COST_BREAKDOWN_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_FACTORS_FIELD_NUMBER: _ClassVar[int]
    BILLED_POINTS_CANDIDATE_FIELD_NUMBER: _ClassVar[int]
    REFUND_REASON_FIELD_NUMBER: _ClassVar[int]
    DEDUPE_KEY_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    authorization_id: str
    request_id: str
    user_id: str
    usage_source: BillingUsageSource
    final_status: BillingFinalStatus
    raw_usage_totals: BillingUsageTotals
    cost_breakdown: BillingCostBreakdown
    business_factors: _struct_pb2.Struct
    billed_points_candidate: int
    refund_reason: str
    dedupe_key: str
    def __init__(self, business_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., user_id: _Optional[str] = ..., usage_source: _Optional[_Union[BillingUsageSource, str]] = ..., final_status: _Optional[_Union[BillingFinalStatus, str]] = ..., raw_usage_totals: _Optional[_Union[BillingUsageTotals, _Mapping]] = ..., cost_breakdown: _Optional[_Union[BillingCostBreakdown, _Mapping]] = ..., business_factors: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., billed_points_candidate: _Optional[int] = ..., refund_reason: _Optional[str] = ..., dedupe_key: _Optional[str] = ...) -> None: ...

class EstimateChargeRequest(_message.Message):
    __slots__ = ("context", "request_factors")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FACTORS_FIELD_NUMBER: _ClassVar[int]
    context: AuthorizationContext
    request_factors: _struct_pb2.Struct
    def __init__(self, context: _Optional[_Union[AuthorizationContext, _Mapping]] = ..., request_factors: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class EstimateChargeResponse(_message.Message):
    __slots__ = ("success", "estimated_points", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_POINTS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    estimated_points: int
    message: str
    def __init__(self, success: bool = ..., estimated_points: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class AuthorizeRequest(_message.Message):
    __slots__ = ("context", "estimated_points")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_POINTS_FIELD_NUMBER: _ClassVar[int]
    context: AuthorizationContext
    estimated_points: int
    def __init__(self, context: _Optional[_Union[AuthorizationContext, _Mapping]] = ..., estimated_points: _Optional[int] = ...) -> None: ...

class BillingAuthorizationResponse(_message.Message):
    __slots__ = ("success", "authorization_id", "held_points", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    HELD_POINTS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    authorization_id: str
    held_points: int
    message: str
    def __init__(self, success: bool = ..., authorization_id: _Optional[str] = ..., held_points: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class FinalizeRequest(_message.Message):
    __slots__ = ("context", "report")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    REPORT_FIELD_NUMBER: _ClassVar[int]
    context: AuthorizationContext
    report: BillingReport
    def __init__(self, context: _Optional[_Union[AuthorizationContext, _Mapping]] = ..., report: _Optional[_Union[BillingReport, _Mapping]] = ...) -> None: ...

class SettlementDecision(_message.Message):
    __slots__ = ("success", "transaction_type", "points", "face_value_minor", "recognized_revenue_minor", "budget_consumed_minor", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    FACE_VALUE_MINOR_FIELD_NUMBER: _ClassVar[int]
    RECOGNIZED_REVENUE_MINOR_FIELD_NUMBER: _ClassVar[int]
    BUDGET_CONSUMED_MINOR_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    transaction_type: BillingTransactionType
    points: int
    face_value_minor: int
    recognized_revenue_minor: int
    budget_consumed_minor: int
    message: str
    def __init__(self, success: bool = ..., transaction_type: _Optional[_Union[BillingTransactionType, str]] = ..., points: _Optional[int] = ..., face_value_minor: _Optional[int] = ..., recognized_revenue_minor: _Optional[int] = ..., budget_consumed_minor: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class ReleaseRequest(_message.Message):
    __slots__ = ("authorization_id", "request_id", "reason")
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    authorization_id: str
    request_id: str
    reason: str
    def __init__(self, authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class RefundRequest(_message.Message):
    __slots__ = ("authorization_id", "request_id", "reason")
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    authorization_id: str
    request_id: str
    reason: str
    def __init__(self, authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class QueryBalanceRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "subject_type", "user_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    subject_type: BillingSubjectType
    user_id: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., user_id: _Optional[str] = ...) -> None: ...

class BalanceSnapshot(_message.Message):
    __slots__ = ("business_id", "subject_id", "subject_type", "user_id", "available_balance", "held_balance", "total_granted", "total_consumed", "updated_at")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_BALANCE_FIELD_NUMBER: _ClassVar[int]
    HELD_BALANCE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_GRANTED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CONSUMED_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    subject_type: BillingSubjectType
    user_id: str
    available_balance: int
    held_balance: int
    total_granted: int
    total_consumed: int
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., user_id: _Optional[str] = ..., available_balance: _Optional[int] = ..., held_balance: _Optional[int] = ..., total_granted: _Optional[int] = ..., total_consumed: _Optional[int] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreditGrant(_message.Message):
    __slots__ = ("grant_id", "business_id", "user_id", "subject_id", "subject_type", "credit_type", "amount", "consumed", "expires_at", "status")
    GRANT_ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CREDIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CONSUMED_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    grant_id: str
    business_id: str
    user_id: str
    subject_id: str
    subject_type: BillingSubjectType
    credit_type: str
    amount: int
    consumed: int
    expires_at: _timestamp_pb2.Timestamp
    status: str
    def __init__(self, grant_id: _Optional[str] = ..., business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., credit_type: _Optional[str] = ..., amount: _Optional[int] = ..., consumed: _Optional[int] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[str] = ...) -> None: ...

class GrantCreditsRequest(_message.Message):
    __slots__ = ("business_id", "user_id", "subject_id", "subject_type", "credit_type", "amount")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CREDIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    user_id: str
    subject_id: str
    subject_type: BillingSubjectType
    credit_type: str
    amount: int
    def __init__(self, business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., credit_type: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...

class ListGrantsRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "subject_type", "user_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    subject_type: BillingSubjectType
    user_id: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., user_id: _Optional[str] = ...) -> None: ...

class ListGrantsResponse(_message.Message):
    __slots__ = ("grants",)
    GRANTS_FIELD_NUMBER: _ClassVar[int]
    grants: _containers.RepeatedCompositeFieldContainer[CreditGrant]
    def __init__(self, grants: _Optional[_Iterable[_Union[CreditGrant, _Mapping]]] = ...) -> None: ...

class BillingTransaction(_message.Message):
    __slots__ = ("transaction_id", "business_id", "user_id", "authorization_id", "request_id", "subject_id", "subject_type", "transaction_type", "points", "face_value_minor", "recognized_revenue_minor", "budget_consumed_minor", "created_at")
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    FACE_VALUE_MINOR_FIELD_NUMBER: _ClassVar[int]
    RECOGNIZED_REVENUE_MINOR_FIELD_NUMBER: _ClassVar[int]
    BUDGET_CONSUMED_MINOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    transaction_id: str
    business_id: str
    user_id: str
    authorization_id: str
    request_id: str
    subject_id: str
    subject_type: BillingSubjectType
    transaction_type: BillingTransactionType
    points: int
    face_value_minor: int
    recognized_revenue_minor: int
    budget_consumed_minor: int
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, transaction_id: _Optional[str] = ..., business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., transaction_type: _Optional[_Union[BillingTransactionType, str]] = ..., points: _Optional[int] = ..., face_value_minor: _Optional[int] = ..., recognized_revenue_minor: _Optional[int] = ..., budget_consumed_minor: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class QueryTransactionsRequest(_message.Message):
    __slots__ = ("business_id", "request_id", "authorization_id", "subject_id", "subject_type", "user_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    request_id: str
    authorization_id: str
    subject_id: str
    subject_type: BillingSubjectType
    user_id: str
    def __init__(self, business_id: _Optional[str] = ..., request_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., user_id: _Optional[str] = ...) -> None: ...

class QueryTransactionsResponse(_message.Message):
    __slots__ = ("transactions",)
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    transactions: _containers.RepeatedCompositeFieldContainer[BillingTransaction]
    def __init__(self, transactions: _Optional[_Iterable[_Union[BillingTransaction, _Mapping]]] = ...) -> None: ...

class UsageCostSnapshot(_message.Message):
    __slots__ = ("business_id", "user_id", "request_id", "usage_snapshot", "cost_snapshot", "business_factors", "policy_id", "created_at")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    USAGE_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    COST_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_FACTORS_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    user_id: str
    request_id: str
    usage_snapshot: _struct_pb2.Struct
    cost_snapshot: _struct_pb2.Struct
    business_factors: _struct_pb2.Struct
    policy_id: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., request_id: _Optional[str] = ..., usage_snapshot: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., cost_snapshot: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., business_factors: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., policy_id: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class QuerySnapshotRequest(_message.Message):
    __slots__ = ("request_id",)
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    def __init__(self, request_id: _Optional[str] = ...) -> None: ...

class ManualReconcileRequest(_message.Message):
    __slots__ = ("request_id", "authorization_id", "reason")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    authorization_id: str
    reason: str
    def __init__(self, request_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class ManualReconcileResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

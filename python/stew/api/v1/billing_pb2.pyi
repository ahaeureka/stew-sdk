import datetime

from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from stew.api.v1 import options_pb2 as _options_pb2
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
    BILLING_REPORT_TRANSPORT_OUT_OF_BAND: _ClassVar[BillingReportTransport]

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

class BillingReservationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_RESERVATION_STATUS_UNSPECIFIED: _ClassVar[BillingReservationStatus]
    BILLING_RESERVATION_STATUS_AUTHORIZED: _ClassVar[BillingReservationStatus]
    BILLING_RESERVATION_STATUS_AWAITING_REPORT: _ClassVar[BillingReservationStatus]
    BILLING_RESERVATION_STATUS_PENDING_RECONCILE: _ClassVar[BillingReservationStatus]
    BILLING_RESERVATION_STATUS_CAPTURED: _ClassVar[BillingReservationStatus]
    BILLING_RESERVATION_STATUS_RELEASED: _ClassVar[BillingReservationStatus]
    BILLING_RESERVATION_STATUS_REFUNDED: _ClassVar[BillingReservationStatus]
    BILLING_RESERVATION_STATUS_EXPIRED: _ClassVar[BillingReservationStatus]

class BillingPolicyArtifactType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_POLICY_ARTIFACT_TYPE_UNSPECIFIED: _ClassVar[BillingPolicyArtifactType]
    BILLING_POLICY_ARTIFACT_TYPE_PROVIDER_RATE_CARD: _ClassVar[BillingPolicyArtifactType]
    BILLING_POLICY_ARTIFACT_TYPE_POINT_POLICY: _ClassVar[BillingPolicyArtifactType]
    BILLING_POLICY_ARTIFACT_TYPE_MONEY_POLICY: _ClassVar[BillingPolicyArtifactType]
    BILLING_POLICY_ARTIFACT_TYPE_ESTIMATOR: _ClassVar[BillingPolicyArtifactType]
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
BILLING_REPORT_TRANSPORT_OUT_OF_BAND: BillingReportTransport
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
BILLING_RESERVATION_STATUS_UNSPECIFIED: BillingReservationStatus
BILLING_RESERVATION_STATUS_AUTHORIZED: BillingReservationStatus
BILLING_RESERVATION_STATUS_AWAITING_REPORT: BillingReservationStatus
BILLING_RESERVATION_STATUS_PENDING_RECONCILE: BillingReservationStatus
BILLING_RESERVATION_STATUS_CAPTURED: BillingReservationStatus
BILLING_RESERVATION_STATUS_RELEASED: BillingReservationStatus
BILLING_RESERVATION_STATUS_REFUNDED: BillingReservationStatus
BILLING_RESERVATION_STATUS_EXPIRED: BillingReservationStatus
BILLING_POLICY_ARTIFACT_TYPE_UNSPECIFIED: BillingPolicyArtifactType
BILLING_POLICY_ARTIFACT_TYPE_PROVIDER_RATE_CARD: BillingPolicyArtifactType
BILLING_POLICY_ARTIFACT_TYPE_POINT_POLICY: BillingPolicyArtifactType
BILLING_POLICY_ARTIFACT_TYPE_MONEY_POLICY: BillingPolicyArtifactType
BILLING_POLICY_ARTIFACT_TYPE_ESTIMATOR: BillingPolicyArtifactType

class ServiceBillingConfig(_message.Message):
    __slots__ = ("enabled", "business_id", "policy_id", "subject_mode", "preauth_mode", "allow_anonymous_subject", "missing_report_action", "release_timeout_seconds", "report_transport", "report_header_prefix", "factor_schema_version", "max_reservation_ttl_seconds", "idempotency_window_seconds", "capture_requires_report", "reconcile_scan_interval_seconds", "max_report_size_bytes", "strict_policy_snapshot", "policy_id_by_plan", "out_of_band_report_timeout_seconds")
    class PolicyIdByPlanEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
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
    POLICY_ID_BY_PLAN_FIELD_NUMBER: _ClassVar[int]
    OUT_OF_BAND_REPORT_TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
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
    policy_id_by_plan: _containers.ScalarMap[str, str]
    out_of_band_report_timeout_seconds: int
    def __init__(self, enabled: bool = ..., business_id: _Optional[str] = ..., policy_id: _Optional[str] = ..., subject_mode: _Optional[_Union[BillingSubjectType, str]] = ..., preauth_mode: _Optional[_Union[BillingPreauthMode, str]] = ..., allow_anonymous_subject: bool = ..., missing_report_action: _Optional[_Union[BillingMissingReportAction, str]] = ..., release_timeout_seconds: _Optional[int] = ..., report_transport: _Optional[_Union[BillingReportTransport, str]] = ..., report_header_prefix: _Optional[str] = ..., factor_schema_version: _Optional[str] = ..., max_reservation_ttl_seconds: _Optional[int] = ..., idempotency_window_seconds: _Optional[int] = ..., capture_requires_report: bool = ..., reconcile_scan_interval_seconds: _Optional[int] = ..., max_report_size_bytes: _Optional[int] = ..., strict_policy_snapshot: bool = ..., policy_id_by_plan: _Optional[_Mapping[str, str]] = ..., out_of_band_report_timeout_seconds: _Optional[int] = ...) -> None: ...

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
    __slots__ = ("chat_in_micros", "chat_out_micros", "embed_micros", "media_micros", "infra_micros", "total_cost_micros")
    CHAT_IN_MICROS_FIELD_NUMBER: _ClassVar[int]
    CHAT_OUT_MICROS_FIELD_NUMBER: _ClassVar[int]
    EMBED_MICROS_FIELD_NUMBER: _ClassVar[int]
    MEDIA_MICROS_FIELD_NUMBER: _ClassVar[int]
    INFRA_MICROS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COST_MICROS_FIELD_NUMBER: _ClassVar[int]
    chat_in_micros: int
    chat_out_micros: int
    embed_micros: int
    media_micros: int
    infra_micros: int
    total_cost_micros: int
    def __init__(self, chat_in_micros: _Optional[int] = ..., chat_out_micros: _Optional[int] = ..., embed_micros: _Optional[int] = ..., media_micros: _Optional[int] = ..., infra_micros: _Optional[int] = ..., total_cost_micros: _Optional[int] = ...) -> None: ...

class BillingReport(_message.Message):
    __slots__ = ("business_id", "authorization_id", "request_id", "user_id", "usage_source", "final_status", "raw_usage_totals", "cost_breakdown", "business_factors", "billed_points_candidate", "refund_reason", "dedupe_key", "provider_usage_facts", "execution_hints")
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
    PROVIDER_USAGE_FACTS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_HINTS_FIELD_NUMBER: _ClassVar[int]
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
    provider_usage_facts: _struct_pb2.Struct
    execution_hints: _struct_pb2.Struct
    def __init__(self, business_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., user_id: _Optional[str] = ..., usage_source: _Optional[_Union[BillingUsageSource, str]] = ..., final_status: _Optional[_Union[BillingFinalStatus, str]] = ..., raw_usage_totals: _Optional[_Union[BillingUsageTotals, _Mapping]] = ..., cost_breakdown: _Optional[_Union[BillingCostBreakdown, _Mapping]] = ..., business_factors: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., billed_points_candidate: _Optional[int] = ..., refund_reason: _Optional[str] = ..., dedupe_key: _Optional[str] = ..., provider_usage_facts: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., execution_hints: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

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

class SubmitBillingReportRequest(_message.Message):
    __slots__ = ("report", "delivery_request_id", "source_service", "labels")
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    REPORT_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_SERVICE_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    report: BillingReport
    delivery_request_id: str
    source_service: str
    labels: _containers.ScalarMap[str, str]
    def __init__(self, report: _Optional[_Union[BillingReport, _Mapping]] = ..., delivery_request_id: _Optional[str] = ..., source_service: _Optional[str] = ..., labels: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SubmitBillingReportResponse(_message.Message):
    __slots__ = ("business_id", "user_id", "subject_id", "subject_type", "authorization_id", "request_id", "decision", "deduped")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    DECISION_FIELD_NUMBER: _ClassVar[int]
    DEDUPED_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    user_id: str
    subject_id: str
    subject_type: BillingSubjectType
    authorization_id: str
    request_id: str
    decision: SettlementDecision
    deduped: bool
    def __init__(self, business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., decision: _Optional[_Union[SettlementDecision, _Mapping]] = ..., deduped: bool = ...) -> None: ...

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
    __slots__ = ("business_id", "subject_id", "authorization_id", "request_id", "reason")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    authorization_id: str
    request_id: str
    reason: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class RefundRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "authorization_id", "request_id", "reason")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    authorization_id: str
    request_id: str
    reason: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

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
    __slots__ = ("business_id", "subject_id", "subject_type", "user_id", "available_balance", "held_balance", "total_granted", "total_consumed", "updated_at", "breakdown", "created_at", "deleted_at")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_BALANCE_FIELD_NUMBER: _ClassVar[int]
    HELD_BALANCE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_GRANTED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CONSUMED_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    BREAKDOWN_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    subject_type: BillingSubjectType
    user_id: str
    available_balance: int
    held_balance: int
    total_granted: int
    total_consumed: int
    updated_at: _timestamp_pb2.Timestamp
    breakdown: _containers.RepeatedCompositeFieldContainer[CreditTypeBalance]
    created_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., user_id: _Optional[str] = ..., available_balance: _Optional[int] = ..., held_balance: _Optional[int] = ..., total_granted: _Optional[int] = ..., total_consumed: _Optional[int] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., breakdown: _Optional[_Iterable[_Union[CreditTypeBalance, _Mapping]]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreditTypeBalance(_message.Message):
    __slots__ = ("credit_type", "available_balance", "held_balance", "total_granted", "total_consumed", "credit_type_display_name")
    CREDIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_BALANCE_FIELD_NUMBER: _ClassVar[int]
    HELD_BALANCE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_GRANTED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CONSUMED_FIELD_NUMBER: _ClassVar[int]
    CREDIT_TYPE_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    credit_type: str
    available_balance: int
    held_balance: int
    total_granted: int
    total_consumed: int
    credit_type_display_name: str
    def __init__(self, credit_type: _Optional[str] = ..., available_balance: _Optional[int] = ..., held_balance: _Optional[int] = ..., total_granted: _Optional[int] = ..., total_consumed: _Optional[int] = ..., credit_type_display_name: _Optional[str] = ...) -> None: ...

class CreditGrant(_message.Message):
    __slots__ = ("grant_id", "business_id", "user_id", "subject_id", "subject_type", "credit_type", "amount", "consumed", "expires_at", "status", "credit_type_display_name", "created_at", "updated_at", "deleted_at")
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
    CREDIT_TYPE_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
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
    credit_type_display_name: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    def __init__(self, grant_id: _Optional[str] = ..., business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., credit_type: _Optional[str] = ..., amount: _Optional[int] = ..., consumed: _Optional[int] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[str] = ..., credit_type_display_name: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GrantCreditsRequest(_message.Message):
    __slots__ = ("business_id", "user_id", "subject_id", "subject_type", "credit_type", "amount", "expires_at_epoch_seconds", "idempotency_key", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CREDIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_EPOCH_SECONDS_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    user_id: str
    subject_id: str
    subject_type: BillingSubjectType
    credit_type: str
    amount: int
    expires_at_epoch_seconds: int
    idempotency_key: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., credit_type: _Optional[str] = ..., amount: _Optional[int] = ..., expires_at_epoch_seconds: _Optional[int] = ..., idempotency_key: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

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
    __slots__ = ("transaction_id", "business_id", "user_id", "authorization_id", "request_id", "subject_id", "subject_type", "transaction_type", "points", "face_value_minor", "recognized_revenue_minor", "budget_consumed_minor", "created_at", "updated_at", "deleted_at")
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
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
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
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    def __init__(self, transaction_id: _Optional[str] = ..., business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., transaction_type: _Optional[_Union[BillingTransactionType, str]] = ..., points: _Optional[int] = ..., face_value_minor: _Optional[int] = ..., recognized_revenue_minor: _Optional[int] = ..., budget_consumed_minor: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetBillingTransactionRequest(_message.Message):
    __slots__ = ("business_id", "request_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    request_id: str
    def __init__(self, business_id: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class QueryTransactionsRequest(_message.Message):
    __slots__ = ("business_id", "request_id", "authorization_id", "subject_id", "subject_type", "user_id", "start_time_epoch_seconds", "end_time_epoch_seconds", "page_size", "page_token", "transaction_type")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_EPOCH_SECONDS_FIELD_NUMBER: _ClassVar[int]
    END_TIME_EPOCH_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    request_id: str
    authorization_id: str
    subject_id: str
    subject_type: BillingSubjectType
    user_id: str
    start_time_epoch_seconds: int
    end_time_epoch_seconds: int
    page_size: int
    page_token: str
    transaction_type: BillingTransactionType
    def __init__(self, business_id: _Optional[str] = ..., request_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., user_id: _Optional[str] = ..., start_time_epoch_seconds: _Optional[int] = ..., end_time_epoch_seconds: _Optional[int] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., transaction_type: _Optional[_Union[BillingTransactionType, str]] = ...) -> None: ...

class QueryTransactionsResponse(_message.Message):
    __slots__ = ("transactions", "next_page_token")
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    transactions: _containers.RepeatedCompositeFieldContainer[BillingTransaction]
    next_page_token: str
    def __init__(self, transactions: _Optional[_Iterable[_Union[BillingTransaction, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class UsageCostSnapshot(_message.Message):
    __slots__ = ("business_id", "user_id", "request_id", "usage_snapshot", "cost_snapshot", "business_factors", "policy_id", "created_at", "updated_at", "deleted_at")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    USAGE_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    COST_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_FACTORS_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    user_id: str
    request_id: str
    usage_snapshot: _struct_pb2.Struct
    cost_snapshot: _struct_pb2.Struct
    business_factors: _struct_pb2.Struct
    policy_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    def __init__(self, business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., request_id: _Optional[str] = ..., usage_snapshot: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., cost_snapshot: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., business_factors: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., policy_id: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class QuerySnapshotRequest(_message.Message):
    __slots__ = ("business_id", "request_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    request_id: str
    def __init__(self, business_id: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class GetBillingReservationRequest(_message.Message):
    __slots__ = ("business_id", "authorization_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    authorization_id: str
    def __init__(self, business_id: _Optional[str] = ..., authorization_id: _Optional[str] = ...) -> None: ...

class QueryBillingReservationsRequest(_message.Message):
    __slots__ = ("business_id", "request_id", "authorization_id", "subject_id", "subject_type", "user_id", "start_time_epoch_seconds", "end_time_epoch_seconds", "page_size", "page_token", "status")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_EPOCH_SECONDS_FIELD_NUMBER: _ClassVar[int]
    END_TIME_EPOCH_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    request_id: str
    authorization_id: str
    subject_id: str
    subject_type: BillingSubjectType
    user_id: str
    start_time_epoch_seconds: int
    end_time_epoch_seconds: int
    page_size: int
    page_token: str
    status: BillingReservationStatus
    def __init__(self, business_id: _Optional[str] = ..., request_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., user_id: _Optional[str] = ..., start_time_epoch_seconds: _Optional[int] = ..., end_time_epoch_seconds: _Optional[int] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., status: _Optional[_Union[BillingReservationStatus, str]] = ...) -> None: ...

class BillingReservation(_message.Message):
    __slots__ = ("business_id", "user_id", "authorization_id", "request_id", "subject_id", "subject_type", "policy_id", "status", "held_points", "captured_points", "awaiting_report_timeout_action", "awaiting_report_deadline", "created_at")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HELD_POINTS_FIELD_NUMBER: _ClassVar[int]
    CAPTURED_POINTS_FIELD_NUMBER: _ClassVar[int]
    AWAITING_REPORT_TIMEOUT_ACTION_FIELD_NUMBER: _ClassVar[int]
    AWAITING_REPORT_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    user_id: str
    authorization_id: str
    request_id: str
    subject_id: str
    subject_type: BillingSubjectType
    policy_id: str
    status: BillingReservationStatus
    held_points: int
    captured_points: int
    awaiting_report_timeout_action: str
    awaiting_report_deadline: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., policy_id: _Optional[str] = ..., status: _Optional[_Union[BillingReservationStatus, str]] = ..., held_points: _Optional[int] = ..., captured_points: _Optional[int] = ..., awaiting_report_timeout_action: _Optional[str] = ..., awaiting_report_deadline: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class QueryBillingReservationsResponse(_message.Message):
    __slots__ = ("reservations", "next_page_token")
    RESERVATIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    reservations: _containers.RepeatedCompositeFieldContainer[BillingReservation]
    next_page_token: str
    def __init__(self, reservations: _Optional[_Iterable[_Union[BillingReservation, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class ManualReconcileRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "request_id", "authorization_id", "reason")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    request_id: str
    authorization_id: str
    reason: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., request_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class ManualReconcileResponse(_message.Message):
    __slots__ = ("success", "message", "reservation")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    reservation: BillingReservation
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., reservation: _Optional[_Union[BillingReservation, _Mapping]] = ...) -> None: ...

class BillingPolicyArtifact(_message.Message):
    __slots__ = ("artifact_id", "business_id", "artifact_type", "artifact_version", "content", "content_hash", "created_at", "updated_at", "deleted_at")
    ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_VERSION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_HASH_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    artifact_id: str
    business_id: str
    artifact_type: BillingPolicyArtifactType
    artifact_version: str
    content: _struct_pb2.Struct
    content_hash: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    def __init__(self, artifact_id: _Optional[str] = ..., business_id: _Optional[str] = ..., artifact_type: _Optional[_Union[BillingPolicyArtifactType, str]] = ..., artifact_version: _Optional[str] = ..., content: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., content_hash: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateBillingPolicyArtifactRequest(_message.Message):
    __slots__ = ("business_id", "artifact_type", "artifact_version", "content", "policy_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_VERSION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    artifact_type: BillingPolicyArtifactType
    artifact_version: str
    content: _struct_pb2.Struct
    policy_id: str
    def __init__(self, business_id: _Optional[str] = ..., artifact_type: _Optional[_Union[BillingPolicyArtifactType, str]] = ..., artifact_version: _Optional[str] = ..., content: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., policy_id: _Optional[str] = ...) -> None: ...

class GetBillingPolicyArtifactRequest(_message.Message):
    __slots__ = ("artifact_id",)
    ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    artifact_id: str
    def __init__(self, artifact_id: _Optional[str] = ...) -> None: ...

class ListBillingPolicyArtifactsRequest(_message.Message):
    __slots__ = ("business_id", "artifact_type", "policy_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    artifact_type: BillingPolicyArtifactType
    policy_id: str
    def __init__(self, business_id: _Optional[str] = ..., artifact_type: _Optional[_Union[BillingPolicyArtifactType, str]] = ..., policy_id: _Optional[str] = ...) -> None: ...

class ListBillingPolicyArtifactsResponse(_message.Message):
    __slots__ = ("artifacts",)
    ARTIFACTS_FIELD_NUMBER: _ClassVar[int]
    artifacts: _containers.RepeatedCompositeFieldContainer[BillingPolicyArtifact]
    def __init__(self, artifacts: _Optional[_Iterable[_Union[BillingPolicyArtifact, _Mapping]]] = ...) -> None: ...

class BillingPolicyBundle(_message.Message):
    __slots__ = ("policy_id", "business_id", "bundle_version", "factor_schema_version", "provider_rate_card_artifact_id", "point_policy_artifact_id", "money_policy_artifact_id", "estimator_artifact_id", "status", "published_at", "created_at", "updated_at", "deleted_at")
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_VERSION_FIELD_NUMBER: _ClassVar[int]
    FACTOR_SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_RATE_CARD_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_POLICY_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    MONEY_POLICY_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    ESTIMATOR_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    policy_id: str
    business_id: str
    bundle_version: int
    factor_schema_version: str
    provider_rate_card_artifact_id: str
    point_policy_artifact_id: str
    money_policy_artifact_id: str
    estimator_artifact_id: str
    status: str
    published_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    def __init__(self, policy_id: _Optional[str] = ..., business_id: _Optional[str] = ..., bundle_version: _Optional[int] = ..., factor_schema_version: _Optional[str] = ..., provider_rate_card_artifact_id: _Optional[str] = ..., point_policy_artifact_id: _Optional[str] = ..., money_policy_artifact_id: _Optional[str] = ..., estimator_artifact_id: _Optional[str] = ..., status: _Optional[str] = ..., published_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., deleted_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class PublishBillingPolicyBundleRequest(_message.Message):
    __slots__ = ("business_id", "policy_id", "factor_schema_version", "provider_rate_card_artifact_id", "point_policy_artifact_id", "money_policy_artifact_id", "estimator_artifact_id", "bundle_version")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    FACTOR_SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_RATE_CARD_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_POLICY_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    MONEY_POLICY_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    ESTIMATOR_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_VERSION_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    policy_id: str
    factor_schema_version: str
    provider_rate_card_artifact_id: str
    point_policy_artifact_id: str
    money_policy_artifact_id: str
    estimator_artifact_id: str
    bundle_version: int
    def __init__(self, business_id: _Optional[str] = ..., policy_id: _Optional[str] = ..., factor_schema_version: _Optional[str] = ..., provider_rate_card_artifact_id: _Optional[str] = ..., point_policy_artifact_id: _Optional[str] = ..., money_policy_artifact_id: _Optional[str] = ..., estimator_artifact_id: _Optional[str] = ..., bundle_version: _Optional[int] = ...) -> None: ...

class GetBillingPolicyBundleRequest(_message.Message):
    __slots__ = ("business_id", "policy_id", "bundle_version")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_VERSION_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    policy_id: str
    bundle_version: int
    def __init__(self, business_id: _Optional[str] = ..., policy_id: _Optional[str] = ..., bundle_version: _Optional[int] = ...) -> None: ...

class ListBillingPolicyBundlesRequest(_message.Message):
    __slots__ = ("business_id", "policy_id", "active_only")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ONLY_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    policy_id: str
    active_only: bool
    def __init__(self, business_id: _Optional[str] = ..., policy_id: _Optional[str] = ..., active_only: bool = ...) -> None: ...

class ListBillingPolicyBundlesResponse(_message.Message):
    __slots__ = ("bundles",)
    BUNDLES_FIELD_NUMBER: _ClassVar[int]
    bundles: _containers.RepeatedCompositeFieldContainer[BillingPolicyBundle]
    def __init__(self, bundles: _Optional[_Iterable[_Union[BillingPolicyBundle, _Mapping]]] = ...) -> None: ...

class BillingPointBreakdown(_message.Message):
    __slots__ = ("base_points", "factor_points", "final_points", "min_points", "point_policy_artifact_id", "point_policy_version")
    BASE_POINTS_FIELD_NUMBER: _ClassVar[int]
    FACTOR_POINTS_FIELD_NUMBER: _ClassVar[int]
    FINAL_POINTS_FIELD_NUMBER: _ClassVar[int]
    MIN_POINTS_FIELD_NUMBER: _ClassVar[int]
    POINT_POLICY_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_POLICY_VERSION_FIELD_NUMBER: _ClassVar[int]
    base_points: int
    factor_points: int
    final_points: int
    min_points: int
    point_policy_artifact_id: str
    point_policy_version: str
    def __init__(self, base_points: _Optional[int] = ..., factor_points: _Optional[int] = ..., final_points: _Optional[int] = ..., min_points: _Optional[int] = ..., point_policy_artifact_id: _Optional[str] = ..., point_policy_version: _Optional[str] = ...) -> None: ...

class BillingMoneySnapshot(_message.Message):
    __slots__ = ("face_value_minor", "recognized_revenue_minor", "budget_consumed_minor", "face_value_minor_per_point", "recognized_revenue_minor_per_point", "budget_minor_per_point", "money_policy_artifact_id", "money_policy_version")
    FACE_VALUE_MINOR_FIELD_NUMBER: _ClassVar[int]
    RECOGNIZED_REVENUE_MINOR_FIELD_NUMBER: _ClassVar[int]
    BUDGET_CONSUMED_MINOR_FIELD_NUMBER: _ClassVar[int]
    FACE_VALUE_MINOR_PER_POINT_FIELD_NUMBER: _ClassVar[int]
    RECOGNIZED_REVENUE_MINOR_PER_POINT_FIELD_NUMBER: _ClassVar[int]
    BUDGET_MINOR_PER_POINT_FIELD_NUMBER: _ClassVar[int]
    MONEY_POLICY_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    MONEY_POLICY_VERSION_FIELD_NUMBER: _ClassVar[int]
    face_value_minor: int
    recognized_revenue_minor: int
    budget_consumed_minor: int
    face_value_minor_per_point: int
    recognized_revenue_minor_per_point: int
    budget_minor_per_point: int
    money_policy_artifact_id: str
    money_policy_version: str
    def __init__(self, face_value_minor: _Optional[int] = ..., recognized_revenue_minor: _Optional[int] = ..., budget_consumed_minor: _Optional[int] = ..., face_value_minor_per_point: _Optional[int] = ..., recognized_revenue_minor_per_point: _Optional[int] = ..., budget_minor_per_point: _Optional[int] = ..., money_policy_artifact_id: _Optional[str] = ..., money_policy_version: _Optional[str] = ...) -> None: ...

class BillingSettlementSnapshot(_message.Message):
    __slots__ = ("business_id", "user_id", "authorization_id", "request_id", "subject_id", "subject_type", "usage_snapshot", "provider_usage_facts", "business_factors", "execution_hints", "raw_cost_snapshot", "point_breakdown", "money_snapshot", "policy_id", "policy_bundle_version", "factor_schema_version", "provider_rate_card_artifact_id", "point_policy_artifact_id", "money_policy_artifact_id", "estimator_artifact_id", "applied_points", "face_value_minor", "recognized_revenue_minor", "budget_consumed_minor", "created_at")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    USAGE_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_USAGE_FACTS_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_FACTORS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_HINTS_FIELD_NUMBER: _ClassVar[int]
    RAW_COST_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    POINT_BREAKDOWN_FIELD_NUMBER: _ClassVar[int]
    MONEY_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_BUNDLE_VERSION_FIELD_NUMBER: _ClassVar[int]
    FACTOR_SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_RATE_CARD_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_POLICY_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    MONEY_POLICY_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    ESTIMATOR_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    APPLIED_POINTS_FIELD_NUMBER: _ClassVar[int]
    FACE_VALUE_MINOR_FIELD_NUMBER: _ClassVar[int]
    RECOGNIZED_REVENUE_MINOR_FIELD_NUMBER: _ClassVar[int]
    BUDGET_CONSUMED_MINOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    user_id: str
    authorization_id: str
    request_id: str
    subject_id: str
    subject_type: BillingSubjectType
    usage_snapshot: BillingUsageTotals
    provider_usage_facts: _struct_pb2.Struct
    business_factors: _struct_pb2.Struct
    execution_hints: _struct_pb2.Struct
    raw_cost_snapshot: BillingCostBreakdown
    point_breakdown: BillingPointBreakdown
    money_snapshot: BillingMoneySnapshot
    policy_id: str
    policy_bundle_version: int
    factor_schema_version: str
    provider_rate_card_artifact_id: str
    point_policy_artifact_id: str
    money_policy_artifact_id: str
    estimator_artifact_id: str
    applied_points: int
    face_value_minor: int
    recognized_revenue_minor: int
    budget_consumed_minor: int
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[BillingSubjectType, str]] = ..., usage_snapshot: _Optional[_Union[BillingUsageTotals, _Mapping]] = ..., provider_usage_facts: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., business_factors: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., execution_hints: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., raw_cost_snapshot: _Optional[_Union[BillingCostBreakdown, _Mapping]] = ..., point_breakdown: _Optional[_Union[BillingPointBreakdown, _Mapping]] = ..., money_snapshot: _Optional[_Union[BillingMoneySnapshot, _Mapping]] = ..., policy_id: _Optional[str] = ..., policy_bundle_version: _Optional[int] = ..., factor_schema_version: _Optional[str] = ..., provider_rate_card_artifact_id: _Optional[str] = ..., point_policy_artifact_id: _Optional[str] = ..., money_policy_artifact_id: _Optional[str] = ..., estimator_artifact_id: _Optional[str] = ..., applied_points: _Optional[int] = ..., face_value_minor: _Optional[int] = ..., recognized_revenue_minor: _Optional[int] = ..., budget_consumed_minor: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

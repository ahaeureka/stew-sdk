import datetime

import billing_common_pb2 as _billing_common_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BillingSessionExecutionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_SESSION_EXECUTION_MODE_UNSPECIFIED: _ClassVar[BillingSessionExecutionMode]
    BILLING_SESSION_EXECUTION_MODE_ASYNC_TASK: _ClassVar[BillingSessionExecutionMode]
    BILLING_SESSION_EXECUTION_MODE_SYNC: _ClassVar[BillingSessionExecutionMode]

class BillingSessionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_SESSION_STATUS_UNSPECIFIED: _ClassVar[BillingSessionStatus]
    BILLING_SESSION_STATUS_CREATED: _ClassVar[BillingSessionStatus]
    BILLING_SESSION_STATUS_AUTHORIZED: _ClassVar[BillingSessionStatus]
    BILLING_SESSION_STATUS_RUNNING: _ClassVar[BillingSessionStatus]
    BILLING_SESSION_STATUS_AWAITING_FINAL_FACTS: _ClassVar[BillingSessionStatus]
    BILLING_SESSION_STATUS_CAPTURED: _ClassVar[BillingSessionStatus]
    BILLING_SESSION_STATUS_RELEASED: _ClassVar[BillingSessionStatus]
    BILLING_SESSION_STATUS_PENDING_RECONCILE: _ClassVar[BillingSessionStatus]
    BILLING_SESSION_STATUS_COMPENSATED: _ClassVar[BillingSessionStatus]
    BILLING_SESSION_STATUS_EXPIRED: _ClassVar[BillingSessionStatus]
BILLING_SESSION_EXECUTION_MODE_UNSPECIFIED: BillingSessionExecutionMode
BILLING_SESSION_EXECUTION_MODE_ASYNC_TASK: BillingSessionExecutionMode
BILLING_SESSION_EXECUTION_MODE_SYNC: BillingSessionExecutionMode
BILLING_SESSION_STATUS_UNSPECIFIED: BillingSessionStatus
BILLING_SESSION_STATUS_CREATED: BillingSessionStatus
BILLING_SESSION_STATUS_AUTHORIZED: BillingSessionStatus
BILLING_SESSION_STATUS_RUNNING: BillingSessionStatus
BILLING_SESSION_STATUS_AWAITING_FINAL_FACTS: BillingSessionStatus
BILLING_SESSION_STATUS_CAPTURED: BillingSessionStatus
BILLING_SESSION_STATUS_RELEASED: BillingSessionStatus
BILLING_SESSION_STATUS_PENDING_RECONCILE: BillingSessionStatus
BILLING_SESSION_STATUS_COMPENSATED: BillingSessionStatus
BILLING_SESSION_STATUS_EXPIRED: BillingSessionStatus

class BillingSession(_message.Message):
    __slots__ = ("billing_session_id", "business_id", "subject_id", "subject_type", "policy_id", "factor_schema_version", "authorization_id", "request_id", "task_id", "run_id", "status", "execution_token_issued", "awaiting_report_deadline", "timeout_action", "created_at", "updated_at")
    BILLING_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    FACTOR_SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_TOKEN_ISSUED_FIELD_NUMBER: _ClassVar[int]
    AWAITING_REPORT_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_ACTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    billing_session_id: str
    business_id: str
    subject_id: str
    subject_type: _billing_common_pb2.BillingSubjectType
    policy_id: str
    factor_schema_version: str
    authorization_id: str
    request_id: str
    task_id: str
    run_id: str
    status: BillingSessionStatus
    execution_token_issued: bool
    awaiting_report_deadline: _timestamp_pb2.Timestamp
    timeout_action: _billing_common_pb2.BillingMissingReportAction
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, billing_session_id: _Optional[str] = ..., business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[_billing_common_pb2.BillingSubjectType, str]] = ..., policy_id: _Optional[str] = ..., factor_schema_version: _Optional[str] = ..., authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., task_id: _Optional[str] = ..., run_id: _Optional[str] = ..., status: _Optional[_Union[BillingSessionStatus, str]] = ..., execution_token_issued: bool = ..., awaiting_report_deadline: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., timeout_action: _Optional[_Union[_billing_common_pb2.BillingMissingReportAction, str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class BillingSessionContext(_message.Message):
    __slots__ = ("billing_session_id", "authorization_id", "business_id", "request_id", "policy_id", "factor_schema_version", "subject_id", "subject_type", "execution_token", "token_version", "issued_at", "expires_at")
    BILLING_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    FACTOR_SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_VERSION_FIELD_NUMBER: _ClassVar[int]
    ISSUED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    billing_session_id: str
    authorization_id: str
    business_id: str
    request_id: str
    policy_id: str
    factor_schema_version: str
    subject_id: str
    subject_type: _billing_common_pb2.BillingSubjectType
    execution_token: str
    token_version: str
    issued_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, billing_session_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., business_id: _Optional[str] = ..., request_id: _Optional[str] = ..., policy_id: _Optional[str] = ..., factor_schema_version: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[_billing_common_pb2.BillingSubjectType, str]] = ..., execution_token: _Optional[str] = ..., token_version: _Optional[str] = ..., issued_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TaskFinalFacts(_message.Message):
    __slots__ = ("final_status", "dedupe_key", "delivery_request_id", "raw_usage_totals", "cost_breakdown", "business_factors", "provider_usage_facts", "execution_hints", "refund_reason")
    FINAL_STATUS_FIELD_NUMBER: _ClassVar[int]
    DEDUPE_KEY_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RAW_USAGE_TOTALS_FIELD_NUMBER: _ClassVar[int]
    COST_BREAKDOWN_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_FACTORS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_USAGE_FACTS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_HINTS_FIELD_NUMBER: _ClassVar[int]
    REFUND_REASON_FIELD_NUMBER: _ClassVar[int]
    final_status: _billing_common_pb2.BillingFinalStatus
    dedupe_key: str
    delivery_request_id: str
    raw_usage_totals: _struct_pb2.Struct
    cost_breakdown: _struct_pb2.Struct
    business_factors: _struct_pb2.Struct
    provider_usage_facts: _struct_pb2.Struct
    execution_hints: _struct_pb2.Struct
    refund_reason: str
    def __init__(self, final_status: _Optional[_Union[_billing_common_pb2.BillingFinalStatus, str]] = ..., dedupe_key: _Optional[str] = ..., delivery_request_id: _Optional[str] = ..., raw_usage_totals: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., cost_breakdown: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., business_factors: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., provider_usage_facts: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., execution_hints: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., refund_reason: _Optional[str] = ...) -> None: ...

class CreateBillingSessionRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "subject_type", "task_id", "run_id", "request_id", "plan_id_hint", "estimated_points", "request_factors", "execution_mode")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_HINT_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_POINTS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FACTORS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_MODE_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    subject_type: _billing_common_pb2.BillingSubjectType
    task_id: str
    run_id: str
    request_id: str
    plan_id_hint: str
    estimated_points: int
    request_factors: _struct_pb2.Struct
    execution_mode: BillingSessionExecutionMode
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[_billing_common_pb2.BillingSubjectType, str]] = ..., task_id: _Optional[str] = ..., run_id: _Optional[str] = ..., request_id: _Optional[str] = ..., plan_id_hint: _Optional[str] = ..., estimated_points: _Optional[int] = ..., request_factors: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., execution_mode: _Optional[_Union[BillingSessionExecutionMode, str]] = ...) -> None: ...

class CreateBillingSessionResponse(_message.Message):
    __slots__ = ("billing_session", "session_context", "reservation_status", "held_points", "message")
    BILLING_SESSION_FIELD_NUMBER: _ClassVar[int]
    SESSION_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    HELD_POINTS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    billing_session: BillingSession
    session_context: BillingSessionContext
    reservation_status: _billing_common_pb2.BillingReservationStatus
    held_points: int
    message: str
    def __init__(self, billing_session: _Optional[_Union[BillingSession, _Mapping]] = ..., session_context: _Optional[_Union[BillingSessionContext, _Mapping]] = ..., reservation_status: _Optional[_Union[_billing_common_pb2.BillingReservationStatus, str]] = ..., held_points: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class ActivateBillingSessionRequest(_message.Message):
    __slots__ = ("billing_session_id", "session_context", "run_id", "estimated_points_override", "activation_reason")
    BILLING_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_POINTS_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_REASON_FIELD_NUMBER: _ClassVar[int]
    billing_session_id: str
    session_context: BillingSessionContext
    run_id: str
    estimated_points_override: int
    activation_reason: str
    def __init__(self, billing_session_id: _Optional[str] = ..., session_context: _Optional[_Union[BillingSessionContext, _Mapping]] = ..., run_id: _Optional[str] = ..., estimated_points_override: _Optional[int] = ..., activation_reason: _Optional[str] = ...) -> None: ...

class ActivateBillingSessionResponse(_message.Message):
    __slots__ = ("billing_session_id", "authorization_id", "reservation_status", "held_points", "effective_estimated_points", "override_applied", "session_status", "message")
    BILLING_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    HELD_POINTS_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_ESTIMATED_POINTS_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_APPLIED_FIELD_NUMBER: _ClassVar[int]
    SESSION_STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    billing_session_id: str
    authorization_id: str
    reservation_status: _billing_common_pb2.BillingReservationStatus
    held_points: int
    effective_estimated_points: int
    override_applied: bool
    session_status: BillingSessionStatus
    message: str
    def __init__(self, billing_session_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., reservation_status: _Optional[_Union[_billing_common_pb2.BillingReservationStatus, str]] = ..., held_points: _Optional[int] = ..., effective_estimated_points: _Optional[int] = ..., override_applied: bool = ..., session_status: _Optional[_Union[BillingSessionStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class CompleteBillingSessionRequest(_message.Message):
    __slots__ = ("billing_session_id", "session_context", "task_final_facts")
    BILLING_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    TASK_FINAL_FACTS_FIELD_NUMBER: _ClassVar[int]
    billing_session_id: str
    session_context: BillingSessionContext
    task_final_facts: TaskFinalFacts
    def __init__(self, billing_session_id: _Optional[str] = ..., session_context: _Optional[_Union[BillingSessionContext, _Mapping]] = ..., task_final_facts: _Optional[_Union[TaskFinalFacts, _Mapping]] = ...) -> None: ...

class CompleteBillingSessionResponse(_message.Message):
    __slots__ = ("billing_session_id", "authorization_id", "decision", "session_status", "reservation_status", "deduped", "outcome_ref")
    BILLING_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    DECISION_FIELD_NUMBER: _ClassVar[int]
    SESSION_STATUS_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    DEDUPED_FIELD_NUMBER: _ClassVar[int]
    OUTCOME_REF_FIELD_NUMBER: _ClassVar[int]
    billing_session_id: str
    authorization_id: str
    decision: str
    session_status: BillingSessionStatus
    reservation_status: _billing_common_pb2.BillingReservationStatus
    deduped: bool
    outcome_ref: str
    def __init__(self, billing_session_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., decision: _Optional[str] = ..., session_status: _Optional[_Union[BillingSessionStatus, str]] = ..., reservation_status: _Optional[_Union[_billing_common_pb2.BillingReservationStatus, str]] = ..., deduped: bool = ..., outcome_ref: _Optional[str] = ...) -> None: ...

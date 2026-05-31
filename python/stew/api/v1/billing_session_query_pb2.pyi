import datetime

import billing_common_pb2 as _billing_common_pb2
import billing_session_pb2 as _billing_session_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BillingDiagnosticsStage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_DIAGNOSTICS_STAGE_UNSPECIFIED: _ClassVar[BillingDiagnosticsStage]
    BILLING_DIAGNOSTICS_STAGE_CREATED: _ClassVar[BillingDiagnosticsStage]
    BILLING_DIAGNOSTICS_STAGE_WAITING_ACTIVATION: _ClassVar[BillingDiagnosticsStage]
    BILLING_DIAGNOSTICS_STAGE_RUNNING: _ClassVar[BillingDiagnosticsStage]
    BILLING_DIAGNOSTICS_STAGE_AWAITING_FINAL_FACTS: _ClassVar[BillingDiagnosticsStage]
    BILLING_DIAGNOSTICS_STAGE_CAPTURED: _ClassVar[BillingDiagnosticsStage]
    BILLING_DIAGNOSTICS_STAGE_RELEASED: _ClassVar[BillingDiagnosticsStage]
    BILLING_DIAGNOSTICS_STAGE_PENDING_RECONCILE: _ClassVar[BillingDiagnosticsStage]
    BILLING_DIAGNOSTICS_STAGE_COMPENSATED: _ClassVar[BillingDiagnosticsStage]
    BILLING_DIAGNOSTICS_STAGE_EXPIRED: _ClassVar[BillingDiagnosticsStage]

class BillingBlockingReasonCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_BLOCKING_REASON_CODE_UNSPECIFIED: _ClassVar[BillingBlockingReasonCode]
    BILLING_BLOCKING_REASON_CODE_NONE: _ClassVar[BillingBlockingReasonCode]
    BILLING_BLOCKING_REASON_CODE_WAITING_FOR_ACTIVATION: _ClassVar[BillingBlockingReasonCode]
    BILLING_BLOCKING_REASON_CODE_WAITING_FOR_FINAL_FACTS: _ClassVar[BillingBlockingReasonCode]
    BILLING_BLOCKING_REASON_CODE_INSUFFICIENT_BALANCE: _ClassVar[BillingBlockingReasonCode]
    BILLING_BLOCKING_REASON_CODE_INVALID_EXECUTION_TOKEN: _ClassVar[BillingBlockingReasonCode]
    BILLING_BLOCKING_REASON_CODE_ESTIMATED_POINTS_OVERRIDE_EXCEEDED: _ClassVar[BillingBlockingReasonCode]
    BILLING_BLOCKING_REASON_CODE_POLICY_RECHECK_FAILED: _ClassVar[BillingBlockingReasonCode]
    BILLING_BLOCKING_REASON_CODE_TIMEOUT_PENDING: _ClassVar[BillingBlockingReasonCode]
    BILLING_BLOCKING_REASON_CODE_LATE_FACTS_PENDING_RECONCILE: _ClassVar[BillingBlockingReasonCode]
    BILLING_BLOCKING_REASON_CODE_SESSION_ALREADY_TERMINAL: _ClassVar[BillingBlockingReasonCode]

class BillingActionRequired(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_ACTION_REQUIRED_UNSPECIFIED: _ClassVar[BillingActionRequired]
    BILLING_ACTION_REQUIRED_NONE: _ClassVar[BillingActionRequired]
    BILLING_ACTION_REQUIRED_ACTIVATE_SESSION: _ClassVar[BillingActionRequired]
    BILLING_ACTION_REQUIRED_SUBMIT_FINAL_FACTS: _ClassVar[BillingActionRequired]
    BILLING_ACTION_REQUIRED_RETRY_COMPLETE: _ClassVar[BillingActionRequired]
    BILLING_ACTION_REQUIRED_RECREATE_SESSION: _ClassVar[BillingActionRequired]
    BILLING_ACTION_REQUIRED_WAIT_PLATFORM_RECONCILE: _ClassVar[BillingActionRequired]
    BILLING_ACTION_REQUIRED_CHECK_CALLER_IDENTITY: _ClassVar[BillingActionRequired]
    BILLING_ACTION_REQUIRED_CHECK_BALANCE: _ClassVar[BillingActionRequired]

class BillingActionOwner(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_ACTION_OWNER_UNSPECIFIED: _ClassVar[BillingActionOwner]
    BILLING_ACTION_OWNER_BUSINESS: _ClassVar[BillingActionOwner]
    BILLING_ACTION_OWNER_PLATFORM: _ClassVar[BillingActionOwner]
    BILLING_ACTION_OWNER_SDK: _ClassVar[BillingActionOwner]
    BILLING_ACTION_OWNER_NONE: _ClassVar[BillingActionOwner]
BILLING_DIAGNOSTICS_STAGE_UNSPECIFIED: BillingDiagnosticsStage
BILLING_DIAGNOSTICS_STAGE_CREATED: BillingDiagnosticsStage
BILLING_DIAGNOSTICS_STAGE_WAITING_ACTIVATION: BillingDiagnosticsStage
BILLING_DIAGNOSTICS_STAGE_RUNNING: BillingDiagnosticsStage
BILLING_DIAGNOSTICS_STAGE_AWAITING_FINAL_FACTS: BillingDiagnosticsStage
BILLING_DIAGNOSTICS_STAGE_CAPTURED: BillingDiagnosticsStage
BILLING_DIAGNOSTICS_STAGE_RELEASED: BillingDiagnosticsStage
BILLING_DIAGNOSTICS_STAGE_PENDING_RECONCILE: BillingDiagnosticsStage
BILLING_DIAGNOSTICS_STAGE_COMPENSATED: BillingDiagnosticsStage
BILLING_DIAGNOSTICS_STAGE_EXPIRED: BillingDiagnosticsStage
BILLING_BLOCKING_REASON_CODE_UNSPECIFIED: BillingBlockingReasonCode
BILLING_BLOCKING_REASON_CODE_NONE: BillingBlockingReasonCode
BILLING_BLOCKING_REASON_CODE_WAITING_FOR_ACTIVATION: BillingBlockingReasonCode
BILLING_BLOCKING_REASON_CODE_WAITING_FOR_FINAL_FACTS: BillingBlockingReasonCode
BILLING_BLOCKING_REASON_CODE_INSUFFICIENT_BALANCE: BillingBlockingReasonCode
BILLING_BLOCKING_REASON_CODE_INVALID_EXECUTION_TOKEN: BillingBlockingReasonCode
BILLING_BLOCKING_REASON_CODE_ESTIMATED_POINTS_OVERRIDE_EXCEEDED: BillingBlockingReasonCode
BILLING_BLOCKING_REASON_CODE_POLICY_RECHECK_FAILED: BillingBlockingReasonCode
BILLING_BLOCKING_REASON_CODE_TIMEOUT_PENDING: BillingBlockingReasonCode
BILLING_BLOCKING_REASON_CODE_LATE_FACTS_PENDING_RECONCILE: BillingBlockingReasonCode
BILLING_BLOCKING_REASON_CODE_SESSION_ALREADY_TERMINAL: BillingBlockingReasonCode
BILLING_ACTION_REQUIRED_UNSPECIFIED: BillingActionRequired
BILLING_ACTION_REQUIRED_NONE: BillingActionRequired
BILLING_ACTION_REQUIRED_ACTIVATE_SESSION: BillingActionRequired
BILLING_ACTION_REQUIRED_SUBMIT_FINAL_FACTS: BillingActionRequired
BILLING_ACTION_REQUIRED_RETRY_COMPLETE: BillingActionRequired
BILLING_ACTION_REQUIRED_RECREATE_SESSION: BillingActionRequired
BILLING_ACTION_REQUIRED_WAIT_PLATFORM_RECONCILE: BillingActionRequired
BILLING_ACTION_REQUIRED_CHECK_CALLER_IDENTITY: BillingActionRequired
BILLING_ACTION_REQUIRED_CHECK_BALANCE: BillingActionRequired
BILLING_ACTION_OWNER_UNSPECIFIED: BillingActionOwner
BILLING_ACTION_OWNER_BUSINESS: BillingActionOwner
BILLING_ACTION_OWNER_PLATFORM: BillingActionOwner
BILLING_ACTION_OWNER_SDK: BillingActionOwner
BILLING_ACTION_OWNER_NONE: BillingActionOwner

class BillingDiagnostics(_message.Message):
    __slots__ = ("current_stage", "blocking_reason_code", "action_required", "action_owner", "last_transition_at", "awaiting_report_deadline", "timeout_action", "latest_error_code", "reconcile_required")
    CURRENT_STAGE_FIELD_NUMBER: _ClassVar[int]
    BLOCKING_REASON_CODE_FIELD_NUMBER: _ClassVar[int]
    ACTION_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    ACTION_OWNER_FIELD_NUMBER: _ClassVar[int]
    LAST_TRANSITION_AT_FIELD_NUMBER: _ClassVar[int]
    AWAITING_REPORT_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_ACTION_FIELD_NUMBER: _ClassVar[int]
    LATEST_ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    RECONCILE_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    current_stage: BillingDiagnosticsStage
    blocking_reason_code: BillingBlockingReasonCode
    action_required: BillingActionRequired
    action_owner: BillingActionOwner
    last_transition_at: _timestamp_pb2.Timestamp
    awaiting_report_deadline: _timestamp_pb2.Timestamp
    timeout_action: _billing_common_pb2.BillingMissingReportAction
    latest_error_code: str
    reconcile_required: bool
    def __init__(self, current_stage: _Optional[_Union[BillingDiagnosticsStage, str]] = ..., blocking_reason_code: _Optional[_Union[BillingBlockingReasonCode, str]] = ..., action_required: _Optional[_Union[BillingActionRequired, str]] = ..., action_owner: _Optional[_Union[BillingActionOwner, str]] = ..., last_transition_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., awaiting_report_deadline: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., timeout_action: _Optional[_Union[_billing_common_pb2.BillingMissingReportAction, str]] = ..., latest_error_code: _Optional[str] = ..., reconcile_required: bool = ...) -> None: ...

class ReservationSummary(_message.Message):
    __slots__ = ("authorization_id", "status", "held_points", "captured_points", "released_points", "created_at", "updated_at")
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HELD_POINTS_FIELD_NUMBER: _ClassVar[int]
    CAPTURED_POINTS_FIELD_NUMBER: _ClassVar[int]
    RELEASED_POINTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    authorization_id: str
    status: _billing_common_pb2.BillingReservationStatus
    held_points: int
    captured_points: int
    released_points: int
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, authorization_id: _Optional[str] = ..., status: _Optional[_Union[_billing_common_pb2.BillingReservationStatus, str]] = ..., held_points: _Optional[int] = ..., captured_points: _Optional[int] = ..., released_points: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class BillingSessionOutcome(_message.Message):
    __slots__ = ("billing_session", "reservation_summary", "latest_decision", "latest_transaction", "snapshot_summary", "diagnostics")
    BILLING_SESSION_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    LATEST_DECISION_FIELD_NUMBER: _ClassVar[int]
    LATEST_TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    billing_session: _billing_session_pb2.BillingSession
    reservation_summary: ReservationSummary
    latest_decision: str
    latest_transaction: _struct_pb2.Struct
    snapshot_summary: _struct_pb2.Struct
    diagnostics: BillingDiagnostics
    def __init__(self, billing_session: _Optional[_Union[_billing_session_pb2.BillingSession, _Mapping]] = ..., reservation_summary: _Optional[_Union[ReservationSummary, _Mapping]] = ..., latest_decision: _Optional[str] = ..., latest_transaction: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., snapshot_summary: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., diagnostics: _Optional[_Union[BillingDiagnostics, _Mapping]] = ...) -> None: ...

class GetBillingSessionOutcomeRequest(_message.Message):
    __slots__ = ("billing_session_id", "authorization_id", "request_id", "task_id", "run_id")
    BILLING_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    billing_session_id: str
    authorization_id: str
    request_id: str
    task_id: str
    run_id: str
    def __init__(self, billing_session_id: _Optional[str] = ..., authorization_id: _Optional[str] = ..., request_id: _Optional[str] = ..., task_id: _Optional[str] = ..., run_id: _Optional[str] = ...) -> None: ...

class GetBillingSessionOutcomeResponse(_message.Message):
    __slots__ = ("outcome",)
    OUTCOME_FIELD_NUMBER: _ClassVar[int]
    outcome: BillingSessionOutcome
    def __init__(self, outcome: _Optional[_Union[BillingSessionOutcome, _Mapping]] = ...) -> None: ...

class QueryBillingSessionsRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "subject_type", "status_filter", "created_after", "created_before", "page_size", "page_token")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FILTER_FIELD_NUMBER: _ClassVar[int]
    CREATED_AFTER_FIELD_NUMBER: _ClassVar[int]
    CREATED_BEFORE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    subject_type: _billing_common_pb2.BillingSubjectType
    status_filter: _containers.RepeatedScalarFieldContainer[_billing_session_pb2.BillingSessionStatus]
    created_after: _timestamp_pb2.Timestamp
    created_before: _timestamp_pb2.Timestamp
    page_size: int
    page_token: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[_billing_common_pb2.BillingSubjectType, str]] = ..., status_filter: _Optional[_Iterable[_Union[_billing_session_pb2.BillingSessionStatus, str]]] = ..., created_after: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., created_before: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class QueryBillingSessionsResponse(_message.Message):
    __slots__ = ("outcomes", "next_page_token", "total_count")
    OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    outcomes: _containers.RepeatedCompositeFieldContainer[BillingSessionOutcome]
    next_page_token: str
    total_count: int
    def __init__(self, outcomes: _Optional[_Iterable[_Union[BillingSessionOutcome, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_count: _Optional[int] = ...) -> None: ...

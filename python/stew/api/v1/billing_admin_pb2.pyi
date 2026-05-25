import billing_common_pb2 as _billing_common_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RevokeBillingGrantsRequest(_message.Message):
    __slots__ = ("business_id", "user_id", "subject_id", "subject_type", "grant_ids", "credit_types", "dry_run")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    GRANT_IDS_FIELD_NUMBER: _ClassVar[int]
    CREDIT_TYPES_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    user_id: str
    subject_id: str
    subject_type: _billing_common_pb2.BillingSubjectType
    grant_ids: _containers.RepeatedScalarFieldContainer[str]
    credit_types: _containers.RepeatedScalarFieldContainer[str]
    dry_run: bool
    def __init__(self, business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[_billing_common_pb2.BillingSubjectType, str]] = ..., grant_ids: _Optional[_Iterable[str]] = ..., credit_types: _Optional[_Iterable[str]] = ..., dry_run: bool = ...) -> None: ...

class RevokeBillingGrantsResponse(_message.Message):
    __slots__ = ("dry_run", "business_id", "user_id", "subject_id", "subject_type", "matched_grant_ids", "matched_grants", "matched_points", "revoked_points", "balance_before", "balance_after", "warnings")
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    MATCHED_GRANT_IDS_FIELD_NUMBER: _ClassVar[int]
    MATCHED_GRANTS_FIELD_NUMBER: _ClassVar[int]
    MATCHED_POINTS_FIELD_NUMBER: _ClassVar[int]
    REVOKED_POINTS_FIELD_NUMBER: _ClassVar[int]
    BALANCE_BEFORE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_AFTER_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    dry_run: bool
    business_id: str
    user_id: str
    subject_id: str
    subject_type: _billing_common_pb2.BillingSubjectType
    matched_grant_ids: _containers.RepeatedScalarFieldContainer[str]
    matched_grants: _containers.RepeatedCompositeFieldContainer[_billing_common_pb2.CreditGrant]
    matched_points: int
    revoked_points: int
    balance_before: _billing_common_pb2.BalanceSnapshot
    balance_after: _billing_common_pb2.BalanceSnapshot
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, dry_run: bool = ..., business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[_billing_common_pb2.BillingSubjectType, str]] = ..., matched_grant_ids: _Optional[_Iterable[str]] = ..., matched_grants: _Optional[_Iterable[_Union[_billing_common_pb2.CreditGrant, _Mapping]]] = ..., matched_points: _Optional[int] = ..., revoked_points: _Optional[int] = ..., balance_before: _Optional[_Union[_billing_common_pb2.BalanceSnapshot, _Mapping]] = ..., balance_after: _Optional[_Union[_billing_common_pb2.BalanceSnapshot, _Mapping]] = ..., warnings: _Optional[_Iterable[str]] = ...) -> None: ...

class BillingBalanceAdjustmentTarget(_message.Message):
    __slots__ = ("available_balance", "held_balance", "total_granted")
    AVAILABLE_BALANCE_FIELD_NUMBER: _ClassVar[int]
    HELD_BALANCE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_GRANTED_FIELD_NUMBER: _ClassVar[int]
    available_balance: int
    held_balance: int
    total_granted: int
    def __init__(self, available_balance: _Optional[int] = ..., held_balance: _Optional[int] = ..., total_granted: _Optional[int] = ...) -> None: ...

class AdjustBillingBalanceRequest(_message.Message):
    __slots__ = ("business_id", "user_id", "subject_id", "subject_type", "target_available_balance", "target_held_balance", "target_total_granted", "dry_run", "force")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TARGET_AVAILABLE_BALANCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_HELD_BALANCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_TOTAL_GRANTED_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    user_id: str
    subject_id: str
    subject_type: _billing_common_pb2.BillingSubjectType
    target_available_balance: int
    target_held_balance: int
    target_total_granted: int
    dry_run: bool
    force: bool
    def __init__(self, business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[_billing_common_pb2.BillingSubjectType, str]] = ..., target_available_balance: _Optional[int] = ..., target_held_balance: _Optional[int] = ..., target_total_granted: _Optional[int] = ..., dry_run: bool = ..., force: bool = ...) -> None: ...

class AdjustBillingBalanceResponse(_message.Message):
    __slots__ = ("dry_run", "force", "business_id", "user_id", "subject_id", "subject_type", "balance_before", "target_balance", "active_grant_count", "active_grants", "live_reservation_count", "live_reservations", "balance_after", "warnings")
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_BEFORE_FIELD_NUMBER: _ClassVar[int]
    TARGET_BALANCE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_GRANT_COUNT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_GRANTS_FIELD_NUMBER: _ClassVar[int]
    LIVE_RESERVATION_COUNT_FIELD_NUMBER: _ClassVar[int]
    LIVE_RESERVATIONS_FIELD_NUMBER: _ClassVar[int]
    BALANCE_AFTER_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    dry_run: bool
    force: bool
    business_id: str
    user_id: str
    subject_id: str
    subject_type: _billing_common_pb2.BillingSubjectType
    balance_before: _billing_common_pb2.BalanceSnapshot
    target_balance: BillingBalanceAdjustmentTarget
    active_grant_count: int
    active_grants: _containers.RepeatedCompositeFieldContainer[_billing_common_pb2.CreditGrant]
    live_reservation_count: int
    live_reservations: _containers.RepeatedCompositeFieldContainer[_billing_common_pb2.BillingReservation]
    balance_after: _billing_common_pb2.BalanceSnapshot
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, dry_run: bool = ..., force: bool = ..., business_id: _Optional[str] = ..., user_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[_billing_common_pb2.BillingSubjectType, str]] = ..., balance_before: _Optional[_Union[_billing_common_pb2.BalanceSnapshot, _Mapping]] = ..., target_balance: _Optional[_Union[BillingBalanceAdjustmentTarget, _Mapping]] = ..., active_grant_count: _Optional[int] = ..., active_grants: _Optional[_Iterable[_Union[_billing_common_pb2.CreditGrant, _Mapping]]] = ..., live_reservation_count: _Optional[int] = ..., live_reservations: _Optional[_Iterable[_Union[_billing_common_pb2.BillingReservation, _Mapping]]] = ..., balance_after: _Optional[_Union[_billing_common_pb2.BalanceSnapshot, _Mapping]] = ..., warnings: _Optional[_Iterable[str]] = ...) -> None: ...

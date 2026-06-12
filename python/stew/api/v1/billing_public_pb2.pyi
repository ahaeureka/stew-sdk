import billing_common_pb2 as _billing_common_pb2
import entitlement_pb2 as _entitlement_pb2
from google.api import annotations_pb2 as _annotations_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetAccountStatusRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "subject_type", "user_id", "include_entitlement")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ENTITLEMENT_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    subject_type: _billing_common_pb2.BillingSubjectType
    user_id: str
    include_entitlement: bool
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., subject_type: _Optional[_Union[_billing_common_pb2.BillingSubjectType, str]] = ..., user_id: _Optional[str] = ..., include_entitlement: bool = ...) -> None: ...

class AccountStatusResponse(_message.Message):
    __slots__ = ("balance", "effective_available_balance", "entitlement")
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_AVAILABLE_BALANCE_FIELD_NUMBER: _ClassVar[int]
    ENTITLEMENT_FIELD_NUMBER: _ClassVar[int]
    balance: _billing_common_pb2.BalanceSnapshot
    effective_available_balance: int
    entitlement: _entitlement_pb2.ResolvedEntitlementResponse
    def __init__(self, balance: _Optional[_Union[_billing_common_pb2.BalanceSnapshot, _Mapping]] = ..., effective_available_balance: _Optional[int] = ..., entitlement: _Optional[_Union[_entitlement_pb2.ResolvedEntitlementResponse, _Mapping]] = ...) -> None: ...

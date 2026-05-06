from google.api import annotations_pb2 as _annotations_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BusinessMembershipRecord(_message.Message):
    __slots__ = ("business_id", "business_name", "business_status", "external_source_type", "external_source_ref", "local_user_id", "membership_status", "role_codes", "source_type", "source_subject", "source_version", "created_at", "updated_at", "synced_at")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_NAME_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_STATUS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_SOURCE_REF_FIELD_NUMBER: _ClassVar[int]
    LOCAL_USER_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ROLE_CODES_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_SUBJECT_FIELD_NUMBER: _ClassVar[int]
    SOURCE_VERSION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SYNCED_AT_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    business_name: str
    business_status: str
    external_source_type: str
    external_source_ref: str
    local_user_id: int
    membership_status: str
    role_codes: _containers.RepeatedScalarFieldContainer[str]
    source_type: str
    source_subject: str
    source_version: str
    created_at: str
    updated_at: str
    synced_at: str
    def __init__(self, business_id: _Optional[str] = ..., business_name: _Optional[str] = ..., business_status: _Optional[str] = ..., external_source_type: _Optional[str] = ..., external_source_ref: _Optional[str] = ..., local_user_id: _Optional[int] = ..., membership_status: _Optional[str] = ..., role_codes: _Optional[_Iterable[str]] = ..., source_type: _Optional[str] = ..., source_subject: _Optional[str] = ..., source_version: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., synced_at: _Optional[str] = ...) -> None: ...

class ListBusinessMembershipsRequest(_message.Message):
    __slots__ = ("business_id", "local_user_id", "membership_status", "page_size", "page_offset")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    LOCAL_USER_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_STATUS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    local_user_id: int
    membership_status: str
    page_size: int
    page_offset: int
    def __init__(self, business_id: _Optional[str] = ..., local_user_id: _Optional[int] = ..., membership_status: _Optional[str] = ..., page_size: _Optional[int] = ..., page_offset: _Optional[int] = ...) -> None: ...

class ListBusinessMembershipsResponse(_message.Message):
    __slots__ = ("items", "total_size")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[BusinessMembershipRecord]
    total_size: int
    def __init__(self, items: _Optional[_Iterable[_Union[BusinessMembershipRecord, _Mapping]]] = ..., total_size: _Optional[int] = ...) -> None: ...

class GetBusinessMembershipRequest(_message.Message):
    __slots__ = ("business_id", "local_user_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    LOCAL_USER_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    local_user_id: int
    def __init__(self, business_id: _Optional[str] = ..., local_user_id: _Optional[int] = ...) -> None: ...

class UpsertBusinessMembershipRequest(_message.Message):
    __slots__ = ("business_id", "local_user_id", "business_name", "business_status", "external_source_type", "external_source_ref", "membership_status", "role_codes", "source_type", "source_subject", "source_version")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    LOCAL_USER_ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_NAME_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_STATUS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_SOURCE_REF_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ROLE_CODES_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_SUBJECT_FIELD_NUMBER: _ClassVar[int]
    SOURCE_VERSION_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    local_user_id: int
    business_name: str
    business_status: str
    external_source_type: str
    external_source_ref: str
    membership_status: str
    role_codes: _containers.RepeatedScalarFieldContainer[str]
    source_type: str
    source_subject: str
    source_version: str
    def __init__(self, business_id: _Optional[str] = ..., local_user_id: _Optional[int] = ..., business_name: _Optional[str] = ..., business_status: _Optional[str] = ..., external_source_type: _Optional[str] = ..., external_source_ref: _Optional[str] = ..., membership_status: _Optional[str] = ..., role_codes: _Optional[_Iterable[str]] = ..., source_type: _Optional[str] = ..., source_subject: _Optional[str] = ..., source_version: _Optional[str] = ...) -> None: ...

class DeleteBusinessMembershipRequest(_message.Message):
    __slots__ = ("business_id", "local_user_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    LOCAL_USER_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    local_user_id: int
    def __init__(self, business_id: _Optional[str] = ..., local_user_id: _Optional[int] = ...) -> None: ...

class DeleteBusinessMembershipResponse(_message.Message):
    __slots__ = ("deleted",)
    DELETED_FIELD_NUMBER: _ClassVar[int]
    deleted: bool
    def __init__(self, deleted: bool = ...) -> None: ...

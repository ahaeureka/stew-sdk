import datetime

from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from stew.api.v1 import web_pb2 as _web_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiKey(_message.Message):
    __slots__ = ("id", "name", "key", "user_id", "description", "scopes", "created_at", "expires_at", "last_used_at", "is_active", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_AT_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    key: str
    user_id: str
    description: str
    scopes: _containers.RepeatedScalarFieldContainer[str]
    created_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    last_used_at: _timestamp_pb2.Timestamp
    is_active: bool
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., key: _Optional[str] = ..., user_id: _Optional[str] = ..., description: _Optional[str] = ..., scopes: _Optional[_Iterable[str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., last_used_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., is_active: bool = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CreateApiKeyRequest(_message.Message):
    __slots__ = ("name", "user_id", "scopes", "expires_at", "metadata", "description")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    user_id: str
    scopes: _containers.RepeatedScalarFieldContainer[str]
    expires_at: _timestamp_pb2.Timestamp
    metadata: _containers.ScalarMap[str, str]
    description: str
    def __init__(self, name: _Optional[str] = ..., user_id: _Optional[str] = ..., scopes: _Optional[_Iterable[str]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., description: _Optional[str] = ...) -> None: ...

class CreateApiKeyResponse(_message.Message):
    __slots__ = ("api_key", "raw_key")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    RAW_KEY_FIELD_NUMBER: _ClassVar[int]
    api_key: ApiKey
    raw_key: str
    def __init__(self, api_key: _Optional[_Union[ApiKey, _Mapping]] = ..., raw_key: _Optional[str] = ...) -> None: ...

class ListApiKeysRequest(_message.Message):
    __slots__ = ("user_id", "page", "limit", "include_inactive")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_INACTIVE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    page: int
    limit: int
    include_inactive: bool
    def __init__(self, user_id: _Optional[str] = ..., page: _Optional[int] = ..., limit: _Optional[int] = ..., include_inactive: bool = ...) -> None: ...

class ListApiKeysResponse(_message.Message):
    __slots__ = ("api_keys", "total", "page", "limit")
    API_KEYS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    api_keys: _containers.RepeatedCompositeFieldContainer[ApiKey]
    total: int
    page: int
    limit: int
    def __init__(self, api_keys: _Optional[_Iterable[_Union[ApiKey, _Mapping]]] = ..., total: _Optional[int] = ..., page: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class GetApiKeyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UpdateApiKeyRequest(_message.Message):
    __slots__ = ("id", "name", "scopes", "expires_at", "is_active", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    scopes: _containers.RepeatedScalarFieldContainer[str]
    expires_at: _timestamp_pb2.Timestamp
    is_active: bool
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., scopes: _Optional[_Iterable[str]] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., is_active: bool = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class DeleteApiKeyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ValidateApiKeyRequest(_message.Message):
    __slots__ = ("api_key", "required_scopes")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_SCOPES_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    required_scopes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, api_key: _Optional[str] = ..., required_scopes: _Optional[_Iterable[str]] = ...) -> None: ...

class ValidateApiKeyResponse(_message.Message):
    __slots__ = ("is_valid", "api_key", "error_message")
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    is_valid: bool
    api_key: ApiKey
    error_message: str
    def __init__(self, is_valid: bool = ..., api_key: _Optional[_Union[ApiKey, _Mapping]] = ..., error_message: _Optional[str] = ...) -> None: ...

class RotateApiKeyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RotateApiKeyResponse(_message.Message):
    __slots__ = ("api_key", "raw_key")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    RAW_KEY_FIELD_NUMBER: _ClassVar[int]
    api_key: ApiKey
    raw_key: str
    def __init__(self, api_key: _Optional[_Union[ApiKey, _Mapping]] = ..., raw_key: _Optional[str] = ...) -> None: ...

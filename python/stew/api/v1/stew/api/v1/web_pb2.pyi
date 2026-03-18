from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[Code]
    OK: _ClassVar[Code]
    PARAMS_ERROR: _ClassVar[Code]
    AUTH_ERROR: _ClassVar[Code]
    PREMISSION_DENIED: _ClassVar[Code]
    NOT_FOUND: _ClassVar[Code]
    TOKEN_NOT_FOUND: _ClassVar[Code]
    RESOURCE_EXHAUSTED: _ClassVar[Code]
    INTERNAL_ERROR: _ClassVar[Code]
    NOT_IMPLEMENTED: _ClassVar[Code]
    TIMEOUT_ERROR: _ClassVar[Code]
    METADATA_MISSING: _ClassVar[Code]
    CONFLICT: _ClassVar[Code]
UNKNOWN: Code
OK: Code
PARAMS_ERROR: Code
AUTH_ERROR: Code
PREMISSION_DENIED: Code
NOT_FOUND: Code
TOKEN_NOT_FOUND: Code
RESOURCE_EXHAUSTED: Code
INTERNAL_ERROR: Code
NOT_IMPLEMENTED: Code
TIMEOUT_ERROR: Code
METADATA_MISSING: Code
CONFLICT: Code
DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
description: _descriptor.FieldDescriptor
HTTP_CODE_FIELD_NUMBER: _ClassVar[int]
http_code: _descriptor.FieldDescriptor

class APIResponse(_message.Message):
    __slots__ = ("message", "code", "response_type", "data")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    message: str
    code: float
    response_type: str
    data: bytes
    def __init__(self, message: _Optional[str] = ..., code: _Optional[float] = ..., response_type: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class HttpResponse(_message.Message):
    __slots__ = ("message", "code", "data")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    message: str
    code: int
    data: _struct_pb2.Struct
    def __init__(self, message: _Optional[str] = ..., code: _Optional[int] = ..., data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class EventStreamResponse(_message.Message):
    __slots__ = ("event", "data", "id", "retry")
    EVENT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RETRY_FIELD_NUMBER: _ClassVar[int]
    event: str
    data: str
    id: int
    retry: int
    def __init__(self, event: _Optional[str] = ..., data: _Optional[str] = ..., id: _Optional[int] = ..., retry: _Optional[int] = ...) -> None: ...

class RedirectResponse(_message.Message):
    __slots__ = ("url", "code")
    URL_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    url: str
    code: int
    def __init__(self, url: _Optional[str] = ..., code: _Optional[int] = ...) -> None: ...

class Errors(_message.Message):
    __slots__ = ("code", "message", "action", "file", "line", "fn", "stack", "to_client_message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    FN_FIELD_NUMBER: _ClassVar[int]
    STACK_FIELD_NUMBER: _ClassVar[int]
    TO_CLIENT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    action: str
    file: str
    line: int
    fn: str
    stack: str
    to_client_message: str
    def __init__(self, code: _Optional[int] = ..., message: _Optional[str] = ..., action: _Optional[str] = ..., file: _Optional[str] = ..., line: _Optional[int] = ..., fn: _Optional[str] = ..., stack: _Optional[str] = ..., to_client_message: _Optional[str] = ...) -> None: ...

class Headers(_message.Message):
    __slots__ = ("Uid", "authentication", "filename", "token")
    UID_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    Uid: str
    authentication: str
    filename: str
    token: str
    def __init__(self, Uid: _Optional[str] = ..., authentication: _Optional[str] = ..., filename: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class EventStream(_message.Message):
    __slots__ = ("event", "data", "id", "retry")
    EVENT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RETRY_FIELD_NUMBER: _ClassVar[int]
    event: str
    data: str
    id: int
    retry: int
    def __init__(self, event: _Optional[str] = ..., data: _Optional[str] = ..., id: _Optional[int] = ..., retry: _Optional[int] = ...) -> None: ...

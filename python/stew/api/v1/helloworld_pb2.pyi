from google.api import annotations_pb2 as _annotations_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from stew.api.v1 import web_pb2 as _web_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class HelloRequest(_message.Message):
    __slots__ = ("msg", "name")
    MSG_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    msg: str
    name: str
    def __init__(self, msg: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class HelloReply(_message.Message):
    __slots__ = ("message", "name")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    message: str
    name: str
    def __init__(self, message: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

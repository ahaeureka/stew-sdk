from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor
AUTH_REQIURED_FIELD_NUMBER: _ClassVar[int]
auth_reqiured: _descriptor.FieldDescriptor
UN_UPDATABLE_FIELD_NUMBER: _ClassVar[int]
un_updatable: _descriptor.FieldDescriptor
VALIDATE_FIELD_NUMBER: _ClassVar[int]
validate: _descriptor.FieldDescriptor
MSG_FIELD_NUMBER: _ClassVar[int]
msg: _descriptor.FieldDescriptor
GO_MOD_PKG_FIELD_NUMBER: _ClassVar[int]
go_mod_pkg: _descriptor.FieldDescriptor
HTTP_RESPONSE_FIELD_NUMBER: _ClassVar[int]
http_response: _descriptor.FieldDescriptor
DONT_USE_HTTP_RESPONSE_FIELD_NUMBER: _ClassVar[int]
dont_use_http_response: _descriptor.FieldDescriptor
DONT_AUTH_REQIURED_FIELD_NUMBER: _ClassVar[int]
dont_auth_reqiured: _descriptor.FieldDescriptor
IS_REDIRECT_FIELD_NUMBER: _ClassVar[int]
is_redirect: _descriptor.FieldDescriptor
USE_AUTH_FIELD_NUMBER: _ClassVar[int]
use_auth: _descriptor.FieldDescriptor
AI_GUARD_FIELD_NUMBER: _ClassVar[int]
ai_guard: _descriptor.FieldDescriptor

class AiGuardFieldOptions(_message.Message):
    __slots__ = ("is_messages_array", "is_role_field", "is_content_field", "role_filter", "is_prompt", "is_model", "is_max_tokens")
    IS_MESSAGES_ARRAY_FIELD_NUMBER: _ClassVar[int]
    IS_ROLE_FIELD_FIELD_NUMBER: _ClassVar[int]
    IS_CONTENT_FIELD_FIELD_NUMBER: _ClassVar[int]
    ROLE_FILTER_FIELD_NUMBER: _ClassVar[int]
    IS_PROMPT_FIELD_NUMBER: _ClassVar[int]
    IS_MODEL_FIELD_NUMBER: _ClassVar[int]
    IS_MAX_TOKENS_FIELD_NUMBER: _ClassVar[int]
    is_messages_array: bool
    is_role_field: bool
    is_content_field: bool
    role_filter: str
    is_prompt: bool
    is_model: bool
    is_max_tokens: bool
    def __init__(self, is_messages_array: bool = ..., is_role_field: bool = ..., is_content_field: bool = ..., role_filter: _Optional[str] = ..., is_prompt: bool = ..., is_model: bool = ..., is_max_tokens: bool = ...) -> None: ...

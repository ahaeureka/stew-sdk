from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
import user_pb2 as _user_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from stew.api.v1 import web_pb2 as _web_pb2
from stew.api.v1 import context_pb2 as _context_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpenIDConnectCallbackRequest(_message.Message):
    __slots__ = ("code", "state", "nonce", "callback", "session_id")
    CODE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    CALLBACK_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    code: str
    state: str
    nonce: str
    callback: str
    session_id: str
    def __init__(self, code: _Optional[str] = ..., state: _Optional[str] = ..., nonce: _Optional[str] = ..., callback: _Optional[str] = ..., session_id: _Optional[str] = ...) -> None: ...

class LoginRequest(_message.Message):
    __slots__ = ("callback", "anonymous_id")
    CALLBACK_FIELD_NUMBER: _ClassVar[int]
    ANONYMOUS_ID_FIELD_NUMBER: _ClassVar[int]
    callback: str
    anonymous_id: str
    def __init__(self, callback: _Optional[str] = ..., anonymous_id: _Optional[str] = ...) -> None: ...

class LoginCallbackResponse(_message.Message):
    __slots__ = ("user", "token")
    USER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    user: _user_pb2.User
    token: str
    def __init__(self, user: _Optional[_Union[_user_pb2.User, _Mapping]] = ..., token: _Optional[str] = ...) -> None: ...

class LogoutRequest(_message.Message):
    __slots__ = ("callback", "token", "session_id")
    CALLBACK_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    callback: str
    token: str
    session_id: str
    def __init__(self, callback: _Optional[str] = ..., token: _Optional[str] = ..., session_id: _Optional[str] = ...) -> None: ...

class LogoutCallbackRequest(_message.Message):
    __slots__ = ("state", "callback")
    STATE_FIELD_NUMBER: _ClassVar[int]
    CALLBACK_FIELD_NUMBER: _ClassVar[int]
    state: str
    callback: str
    def __init__(self, state: _Optional[str] = ..., callback: _Optional[str] = ...) -> None: ...

class AuthServiceUris(_message.Message):
    __slots__ = ("login_url", "logout_url")
    LOGIN_URL_FIELD_NUMBER: _ClassVar[int]
    LOGOUT_URL_FIELD_NUMBER: _ClassVar[int]
    login_url: str
    logout_url: str
    def __init__(self, login_url: _Optional[str] = ..., logout_url: _Optional[str] = ...) -> None: ...

class GetCurrentUserRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CurrentUserResponse(_message.Message):
    __slots__ = ("user", "session_id", "expires_at")
    USER_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    user: _user_pb2.User
    session_id: str
    expires_at: int
    def __init__(self, user: _Optional[_Union[_user_pb2.User, _Mapping]] = ..., session_id: _Optional[str] = ..., expires_at: _Optional[int] = ...) -> None: ...

class ValidateSessionRequest(_message.Message):
    __slots__ = ("session_id",)
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class ValidateSessionResponse(_message.Message):
    __slots__ = ("valid", "user_id", "expires_at")
    VALID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    user_id: str
    expires_at: int
    def __init__(self, valid: bool = ..., user_id: _Optional[str] = ..., expires_at: _Optional[int] = ...) -> None: ...

class RefreshTokenRequest(_message.Message):
    __slots__ = ("session_id",)
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class RefreshTokenResponse(_message.Message):
    __slots__ = ("access_token", "expires_in")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    expires_in: int
    def __init__(self, access_token: _Optional[str] = ..., expires_in: _Optional[int] = ...) -> None: ...

class DeviceFingerprintRequest(_message.Message):
    __slots__ = ("fingerprint_hash", "signature", "public_key", "timestamp", "nonce", "anonymous_id", "components_count")
    FINGERPRINT_HASH_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    ANONYMOUS_ID_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_COUNT_FIELD_NUMBER: _ClassVar[int]
    fingerprint_hash: str
    signature: str
    public_key: str
    timestamp: int
    nonce: str
    anonymous_id: str
    components_count: int
    def __init__(self, fingerprint_hash: _Optional[str] = ..., signature: _Optional[str] = ..., public_key: _Optional[str] = ..., timestamp: _Optional[int] = ..., nonce: _Optional[str] = ..., anonymous_id: _Optional[str] = ..., components_count: _Optional[int] = ...) -> None: ...

class AnonymousSessionResponse(_message.Message):
    __slots__ = ("anonymous_id", "session_token", "expires_at", "is_suspicious")
    ANONYMOUS_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    IS_SUSPICIOUS_FIELD_NUMBER: _ClassVar[int]
    anonymous_id: str
    session_token: str
    expires_at: int
    is_suspicious: bool
    def __init__(self, anonymous_id: _Optional[str] = ..., session_token: _Optional[str] = ..., expires_at: _Optional[int] = ..., is_suspicious: bool = ...) -> None: ...

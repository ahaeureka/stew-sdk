from google.protobuf import timestamp_pb2 as _timestamp_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.api import annotations_pb2 as _annotations_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ADMIN: _ClassVar[Role]

class USER_STATUS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVE: _ClassVar[USER_STATUS]
    INACTIVE: _ClassVar[USER_STATUS]
    LOCKED: _ClassVar[USER_STATUS]
    DELETED: _ClassVar[USER_STATUS]

class UserSvrCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER_UNKNOWN: _ClassVar[UserSvrCode]
    USER_LOGIN_ERR: _ClassVar[UserSvrCode]
    USER_TOKEN_EXPIRE_ERR: _ClassVar[UserSvrCode]
    USER_DISABLED_ERR: _ClassVar[UserSvrCode]
    USER_TOKEN_INVALIDATE_ERR: _ClassVar[UserSvrCode]
    USER_TOKEN_NOT_ACTIVTE_ERR: _ClassVar[UserSvrCode]
    USER_AUTH_DECRYPT_ERR: _ClassVar[UserSvrCode]
    USER_ACCOUNT_ERR: _ClassVar[UserSvrCode]
    USER_PASSWORD_ERR: _ClassVar[UserSvrCode]
    USER_NOT_FOUND_ERR: _ClassVar[UserSvrCode]
    USER_AUTH_MISSING_ERR: _ClassVar[UserSvrCode]
    USER_IDENTITY_MISSING_ERR: _ClassVar[UserSvrCode]
    USER_APIKEY_NOT_MATCH_ERR: _ClassVar[UserSvrCode]
    USER_USERNAME_DUPLICATE_ERR: _ClassVar[UserSvrCode]
ADMIN: Role
ACTIVE: USER_STATUS
INACTIVE: USER_STATUS
LOCKED: USER_STATUS
DELETED: USER_STATUS
USER_UNKNOWN: UserSvrCode
USER_LOGIN_ERR: UserSvrCode
USER_TOKEN_EXPIRE_ERR: UserSvrCode
USER_DISABLED_ERR: UserSvrCode
USER_TOKEN_INVALIDATE_ERR: UserSvrCode
USER_TOKEN_NOT_ACTIVTE_ERR: UserSvrCode
USER_AUTH_DECRYPT_ERR: UserSvrCode
USER_ACCOUNT_ERR: UserSvrCode
USER_PASSWORD_ERR: UserSvrCode
USER_NOT_FOUND_ERR: UserSvrCode
USER_AUTH_MISSING_ERR: UserSvrCode
USER_IDENTITY_MISSING_ERR: UserSvrCode
USER_APIKEY_NOT_MATCH_ERR: UserSvrCode
USER_USERNAME_DUPLICATE_ERR: UserSvrCode

class Address(_message.Message):
    __slots__ = ("formatted", "street_address", "locality", "region", "postal_code", "country")
    FORMATTED_FIELD_NUMBER: _ClassVar[int]
    STREET_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    LOCALITY_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    formatted: str
    street_address: str
    locality: str
    region: str
    postal_code: str
    country: str
    def __init__(self, formatted: _Optional[str] = ..., street_address: _Optional[str] = ..., locality: _Optional[str] = ..., region: _Optional[str] = ..., postal_code: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("sub", "name", "given_name", "family_name", "middle_name", "nickname", "preferred_username", "profile", "picture", "website", "email", "email_verified", "gender", "birthdate", "zoneinfo", "locale", "phone_number", "phone_number_verified", "address", "updated_at", "id", "owner", "type", "password", "password_salt", "password_type", "display_name", "first_name", "last_name", "avatar", "avatar_type", "permanent_avatar", "properties")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _any_pb2.Any
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
    SUB_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    GIVEN_NAME_FIELD_NUMBER: _ClassVar[int]
    FAMILY_NAME_FIELD_NUMBER: _ClassVar[int]
    MIDDLE_NAME_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_USERNAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    PICTURE_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    BIRTHDATE_FIELD_NUMBER: _ClassVar[int]
    ZONEINFO_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_SALT_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    AVATAR_TYPE_FIELD_NUMBER: _ClassVar[int]
    PERMANENT_AVATAR_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    sub: str
    name: str
    given_name: str
    family_name: str
    middle_name: str
    nickname: str
    preferred_username: str
    profile: str
    picture: str
    website: str
    email: str
    email_verified: bool
    gender: str
    birthdate: str
    zoneinfo: str
    locale: str
    phone_number: str
    phone_number_verified: bool
    address: _containers.RepeatedCompositeFieldContainer[Address]
    updated_at: int
    id: str
    owner: str
    type: str
    password: str
    password_salt: str
    password_type: str
    display_name: str
    first_name: str
    last_name: str
    avatar: str
    avatar_type: str
    permanent_avatar: str
    properties: _containers.MessageMap[str, _any_pb2.Any]
    def __init__(self, sub: _Optional[str] = ..., name: _Optional[str] = ..., given_name: _Optional[str] = ..., family_name: _Optional[str] = ..., middle_name: _Optional[str] = ..., nickname: _Optional[str] = ..., preferred_username: _Optional[str] = ..., profile: _Optional[str] = ..., picture: _Optional[str] = ..., website: _Optional[str] = ..., email: _Optional[str] = ..., email_verified: bool = ..., gender: _Optional[str] = ..., birthdate: _Optional[str] = ..., zoneinfo: _Optional[str] = ..., locale: _Optional[str] = ..., phone_number: _Optional[str] = ..., phone_number_verified: bool = ..., address: _Optional[_Iterable[_Union[Address, _Mapping]]] = ..., updated_at: _Optional[int] = ..., id: _Optional[str] = ..., owner: _Optional[str] = ..., type: _Optional[str] = ..., password: _Optional[str] = ..., password_salt: _Optional[str] = ..., password_type: _Optional[str] = ..., display_name: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., avatar: _Optional[str] = ..., avatar_type: _Optional[str] = ..., permanent_avatar: _Optional[str] = ..., properties: _Optional[_Mapping[str, _any_pb2.Any]] = ...) -> None: ...

class BasicAuth(_message.Message):
    __slots__ = ("uid", "name", "role", "audience", "issuer", "not_before", "expiration", "issued_at", "is_keep_login", "token")
    UID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    AUDIENCE_FIELD_NUMBER: _ClassVar[int]
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    NOT_BEFORE_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    ISSUED_AT_FIELD_NUMBER: _ClassVar[int]
    IS_KEEP_LOGIN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    uid: str
    name: str
    role: Role
    audience: str
    issuer: str
    not_before: int
    expiration: int
    issued_at: int
    is_keep_login: bool
    token: str
    def __init__(self, uid: _Optional[str] = ..., name: _Optional[str] = ..., role: _Optional[_Union[Role, str]] = ..., audience: _Optional[str] = ..., issuer: _Optional[str] = ..., not_before: _Optional[int] = ..., expiration: _Optional[int] = ..., issued_at: _Optional[int] = ..., is_keep_login: bool = ..., token: _Optional[str] = ...) -> None: ...

class PostUserRequest(_message.Message):
    __slots__ = ("name", "password", "email", "phone", "role", "status", "dept", "owner", "avatar", "tenant_id", "update_mask")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DEPT_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    name: str
    password: str
    email: str
    phone: str
    role: Role
    status: USER_STATUS
    dept: str
    owner: str
    avatar: str
    tenant_id: str
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, name: _Optional[str] = ..., password: _Optional[str] = ..., email: _Optional[str] = ..., phone: _Optional[str] = ..., role: _Optional[_Union[Role, str]] = ..., status: _Optional[_Union[USER_STATUS, str]] = ..., dept: _Optional[str] = ..., owner: _Optional[str] = ..., avatar: _Optional[str] = ..., tenant_id: _Optional[str] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("uid",)
    UID_FIELD_NUMBER: _ClassVar[int]
    uid: str
    def __init__(self, uid: _Optional[str] = ...) -> None: ...

class DeleteUserRequest(_message.Message):
    __slots__ = ("uid",)
    UID_FIELD_NUMBER: _ClassVar[int]
    uid: str
    def __init__(self, uid: _Optional[str] = ...) -> None: ...

class DeleteUserResponse(_message.Message):
    __slots__ = ("uid",)
    UID_FIELD_NUMBER: _ClassVar[int]
    uid: str
    def __init__(self, uid: _Optional[str] = ...) -> None: ...

class PatchUserRequest(_message.Message):
    __slots__ = ("uid", "name", "password", "email", "phone", "role", "status", "dept", "owner", "avatar", "update_mask")
    UID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DEPT_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    uid: str
    name: str
    password: str
    email: str
    phone: str
    role: Role
    status: USER_STATUS
    dept: str
    owner: str
    avatar: str
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, uid: _Optional[str] = ..., name: _Optional[str] = ..., password: _Optional[str] = ..., email: _Optional[str] = ..., phone: _Optional[str] = ..., role: _Optional[_Union[Role, str]] = ..., status: _Optional[_Union[USER_STATUS, str]] = ..., dept: _Optional[str] = ..., owner: _Optional[str] = ..., avatar: _Optional[str] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

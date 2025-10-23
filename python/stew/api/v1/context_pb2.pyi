from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Tenant(_message.Message):
    __slots__ = ("sub", "name", "tenant_id", "roles", "permissions", "departments", "attributes")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _any_pb2.Any
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
    SUB_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    DEPARTMENTS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    sub: str
    name: str
    tenant_id: str
    roles: _containers.RepeatedScalarFieldContainer[str]
    permissions: _containers.RepeatedScalarFieldContainer[str]
    departments: _containers.RepeatedScalarFieldContainer[str]
    attributes: _containers.MessageMap[str, _any_pb2.Any]
    def __init__(self, sub: _Optional[str] = ..., name: _Optional[str] = ..., tenant_id: _Optional[str] = ..., roles: _Optional[_Iterable[str]] = ..., permissions: _Optional[_Iterable[str]] = ..., departments: _Optional[_Iterable[str]] = ..., attributes: _Optional[_Mapping[str, _any_pb2.Any]] = ...) -> None: ...

class ClientContext(_message.Message):
    __slots__ = ("ip", "device", "location", "token", "tenant", "ua", "referer", "origin", "host", "browser", "os", "country", "region", "additional")
    class AdditionalEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _any_pb2.Any
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
    IP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    TENANT_FIELD_NUMBER: _ClassVar[int]
    UA_FIELD_NUMBER: _ClassVar[int]
    REFERER_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    BROWSER_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_FIELD_NUMBER: _ClassVar[int]
    ip: str
    device: str
    location: str
    token: str
    tenant: Tenant
    ua: str
    referer: str
    origin: str
    host: str
    browser: str
    os: str
    country: str
    region: str
    additional: _containers.MessageMap[str, _any_pb2.Any]
    def __init__(self, ip: _Optional[str] = ..., device: _Optional[str] = ..., location: _Optional[str] = ..., token: _Optional[str] = ..., tenant: _Optional[_Union[Tenant, _Mapping]] = ..., ua: _Optional[str] = ..., referer: _Optional[str] = ..., origin: _Optional[str] = ..., host: _Optional[str] = ..., browser: _Optional[str] = ..., os: _Optional[str] = ..., country: _Optional[str] = ..., region: _Optional[str] = ..., additional: _Optional[_Mapping[str, _any_pb2.Any]] = ...) -> None: ...

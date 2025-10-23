import datetime

from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from stew.api.v1 import web_pb2 as _web_pb2
import user_pb2 as _user_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TokenRequest(_message.Message):
    __slots__ = ("code", "redirect_uri", "state")
    CODE_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    code: str
    redirect_uri: str
    state: str
    def __init__(self, code: _Optional[str] = ..., redirect_uri: _Optional[str] = ..., state: _Optional[str] = ...) -> None: ...

class TokenResponse(_message.Message):
    __slots__ = ("access_token", "token_type", "expires_in", "refresh_token", "id_token", "user_info")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ID_TOKEN_FIELD_NUMBER: _ClassVar[int]
    USER_INFO_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    id_token: str
    user_info: _user_pb2.User
    def __init__(self, access_token: _Optional[str] = ..., token_type: _Optional[str] = ..., expires_in: _Optional[int] = ..., refresh_token: _Optional[str] = ..., id_token: _Optional[str] = ..., user_info: _Optional[_Union[_user_pb2.User, _Mapping]] = ...) -> None: ...

class ValidateTokenRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class ValidateTokenResponse(_message.Message):
    __slots__ = ("valid", "user", "claims", "expires_at")
    VALID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    CLAIMS_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    user: _user_pb2.User
    claims: _struct_pb2.Struct
    expires_at: int
    def __init__(self, valid: bool = ..., user: _Optional[_Union[_user_pb2.User, _Mapping]] = ..., claims: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., expires_at: _Optional[int] = ...) -> None: ...

class AuthorizationRequest(_message.Message):
    __slots__ = ("subject", "action", "resource", "context", "domain", "force_opa", "subject_type")
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    FORCE_OPA_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    subject: str
    action: str
    resource: str
    context: _struct_pb2.Struct
    domain: str
    force_opa: bool
    subject_type: str
    def __init__(self, subject: _Optional[str] = ..., action: _Optional[str] = ..., resource: _Optional[str] = ..., context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., domain: _Optional[str] = ..., force_opa: bool = ..., subject_type: _Optional[str] = ...) -> None: ...

class AuthorizationResponse(_message.Message):
    __slots__ = ("allowed", "reason", "decision_source", "decision_time_ms", "recommendations", "trace_id")
    ALLOWED_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    DECISION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    DECISION_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    RECOMMENDATIONS_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    allowed: bool
    reason: str
    decision_source: str
    decision_time_ms: int
    recommendations: _containers.RepeatedScalarFieldContainer[str]
    trace_id: str
    def __init__(self, allowed: bool = ..., reason: _Optional[str] = ..., decision_source: _Optional[str] = ..., decision_time_ms: _Optional[int] = ..., recommendations: _Optional[_Iterable[str]] = ..., trace_id: _Optional[str] = ...) -> None: ...

class BatchAuthorizationRequest(_message.Message):
    __slots__ = ("requests",)
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[AuthorizationRequest]
    def __init__(self, requests: _Optional[_Iterable[_Union[AuthorizationRequest, _Mapping]]] = ...) -> None: ...

class BatchAuthorizationResponse(_message.Message):
    __slots__ = ("responses",)
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    responses: _containers.RepeatedCompositeFieldContainer[AuthorizationResponse]
    def __init__(self, responses: _Optional[_Iterable[_Union[AuthorizationResponse, _Mapping]]] = ...) -> None: ...

class PolicyRule(_message.Message):
    __slots__ = ("ptype", "rule")
    PTYPE_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    ptype: str
    rule: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ptype: _Optional[str] = ..., rule: _Optional[_Iterable[str]] = ...) -> None: ...

class SyncPolicyRequest(_message.Message):
    __slots__ = ("domain", "policies", "version")
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    domain: str
    policies: _containers.RepeatedCompositeFieldContainer[PolicyRule]
    version: int
    def __init__(self, domain: _Optional[str] = ..., policies: _Optional[_Iterable[_Union[PolicyRule, _Mapping]]] = ..., version: _Optional[int] = ...) -> None: ...

class SyncPolicyResponse(_message.Message):
    __slots__ = ("success", "message", "synced_count", "synced_at")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SYNCED_COUNT_FIELD_NUMBER: _ClassVar[int]
    SYNCED_AT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    synced_count: int
    synced_at: _timestamp_pb2.Timestamp
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., synced_count: _Optional[int] = ..., synced_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetPolicyRequest(_message.Message):
    __slots__ = ("domain", "subject")
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    domain: str
    subject: str
    def __init__(self, domain: _Optional[str] = ..., subject: _Optional[str] = ...) -> None: ...

class GetPolicyResponse(_message.Message):
    __slots__ = ("policies", "version", "updated_at")
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[PolicyRule]
    version: int
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, policies: _Optional[_Iterable[_Union[PolicyRule, _Mapping]]] = ..., version: _Optional[int] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AddPolicyRequest(_message.Message):
    __slots__ = ("domain", "policy")
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    domain: str
    policy: PolicyRule
    def __init__(self, domain: _Optional[str] = ..., policy: _Optional[_Union[PolicyRule, _Mapping]] = ...) -> None: ...

class RemovePolicyRequest(_message.Message):
    __slots__ = ("domain", "policy")
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    domain: str
    policy: PolicyRule
    def __init__(self, domain: _Optional[str] = ..., policy: _Optional[_Union[PolicyRule, _Mapping]] = ...) -> None: ...

class PolicyOperationResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class AuditLog(_message.Message):
    __slots__ = ("trace_id", "timestamp", "subject", "action", "resource", "allowed", "decision_source", "reason", "context", "ip_address", "user_agent")
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_FIELD_NUMBER: _ClassVar[int]
    DECISION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    trace_id: str
    timestamp: _timestamp_pb2.Timestamp
    subject: str
    action: str
    resource: str
    allowed: bool
    decision_source: str
    reason: str
    context: _struct_pb2.Struct
    ip_address: str
    user_agent: str
    def __init__(self, trace_id: _Optional[str] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., subject: _Optional[str] = ..., action: _Optional[str] = ..., resource: _Optional[str] = ..., allowed: bool = ..., decision_source: _Optional[str] = ..., reason: _Optional[str] = ..., context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., ip_address: _Optional[str] = ..., user_agent: _Optional[str] = ...) -> None: ...

class QueryAuditLogsRequest(_message.Message):
    __slots__ = ("subject", "resource", "start_time", "end_time", "page_size", "page_token")
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    subject: str
    resource: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    page_size: int
    page_token: str
    def __init__(self, subject: _Optional[str] = ..., resource: _Optional[str] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class QueryAuditLogsResponse(_message.Message):
    __slots__ = ("logs", "next_page_token", "total_count")
    LOGS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[AuditLog]
    next_page_token: str
    total_count: int
    def __init__(self, logs: _Optional[_Iterable[_Union[AuditLog, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_count: _Optional[int] = ...) -> None: ...

class HealthCheckRequest(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: str
    def __init__(self, service: _Optional[str] = ...) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ("status", "components", "version")
    class ServingStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[HealthCheckResponse.ServingStatus]
        SERVING: _ClassVar[HealthCheckResponse.ServingStatus]
        NOT_SERVING: _ClassVar[HealthCheckResponse.ServingStatus]
        SERVICE_UNKNOWN: _ClassVar[HealthCheckResponse.ServingStatus]
    UNKNOWN: HealthCheckResponse.ServingStatus
    SERVING: HealthCheckResponse.ServingStatus
    NOT_SERVING: HealthCheckResponse.ServingStatus
    SERVICE_UNKNOWN: HealthCheckResponse.ServingStatus
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    status: HealthCheckResponse.ServingStatus
    components: _struct_pb2.Struct
    version: str
    def __init__(self, status: _Optional[_Union[HealthCheckResponse.ServingStatus, str]] = ..., components: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., version: _Optional[str] = ...) -> None: ...

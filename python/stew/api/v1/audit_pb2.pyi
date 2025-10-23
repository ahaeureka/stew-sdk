import datetime

from google.api import annotations_pb2 as _annotations_pb2
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

class AuditLogEntry(_message.Message):
    __slots__ = ("id", "trace_id", "user_id", "api_key_id", "session_id", "action", "resource", "domain", "ip_address", "user_agent", "success", "decision_source", "reason", "error_message", "request_size", "response_size", "duration_ms", "metadata", "created_at")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    API_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    DECISION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_SIZE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_SIZE_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    trace_id: str
    user_id: str
    api_key_id: str
    session_id: str
    action: str
    resource: str
    domain: str
    ip_address: str
    user_agent: str
    success: bool
    decision_source: str
    reason: str
    error_message: str
    request_size: int
    response_size: int
    duration_ms: int
    metadata: _containers.ScalarMap[str, str]
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., trace_id: _Optional[str] = ..., user_id: _Optional[str] = ..., api_key_id: _Optional[str] = ..., session_id: _Optional[str] = ..., action: _Optional[str] = ..., resource: _Optional[str] = ..., domain: _Optional[str] = ..., ip_address: _Optional[str] = ..., user_agent: _Optional[str] = ..., success: bool = ..., decision_source: _Optional[str] = ..., reason: _Optional[str] = ..., error_message: _Optional[str] = ..., request_size: _Optional[int] = ..., response_size: _Optional[int] = ..., duration_ms: _Optional[int] = ..., metadata: _Optional[_Mapping[str, str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetAuditLogsRequest(_message.Message):
    __slots__ = ("trace_id", "user_id", "api_key_id", "session_id", "action", "resource", "domain", "success_filter", "decision_source", "start_time", "end_time", "page", "limit")
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    API_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FILTER_FIELD_NUMBER: _ClassVar[int]
    DECISION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    trace_id: str
    user_id: str
    api_key_id: str
    session_id: str
    action: str
    resource: str
    domain: str
    success_filter: int
    decision_source: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    page: int
    limit: int
    def __init__(self, trace_id: _Optional[str] = ..., user_id: _Optional[str] = ..., api_key_id: _Optional[str] = ..., session_id: _Optional[str] = ..., action: _Optional[str] = ..., resource: _Optional[str] = ..., domain: _Optional[str] = ..., success_filter: _Optional[int] = ..., decision_source: _Optional[str] = ..., start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., page: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class GetAuditLogsResponse(_message.Message):
    __slots__ = ("logs", "total", "page", "limit")
    LOGS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[AuditLogEntry]
    total: int
    page: int
    limit: int
    def __init__(self, logs: _Optional[_Iterable[_Union[AuditLogEntry, _Mapping]]] = ..., total: _Optional[int] = ..., page: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class GetAuditStatisticsRequest(_message.Message):
    __slots__ = ("start_time", "end_time")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, start_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ActionStatistic(_message.Message):
    __slots__ = ("action", "count")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    action: str
    count: int
    def __init__(self, action: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class GetAuditStatisticsResponse(_message.Message):
    __slots__ = ("total_count", "success_count", "failure_count", "action_stats")
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_COUNT_FIELD_NUMBER: _ClassVar[int]
    FAILURE_COUNT_FIELD_NUMBER: _ClassVar[int]
    ACTION_STATS_FIELD_NUMBER: _ClassVar[int]
    total_count: int
    success_count: int
    failure_count: int
    action_stats: _containers.RepeatedCompositeFieldContainer[ActionStatistic]
    def __init__(self, total_count: _Optional[int] = ..., success_count: _Optional[int] = ..., failure_count: _Optional[int] = ..., action_stats: _Optional[_Iterable[_Union[ActionStatistic, _Mapping]]] = ...) -> None: ...

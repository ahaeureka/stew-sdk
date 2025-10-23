import datetime

from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from stew.api.v1 import web_pb2 as _web_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BalanceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BALANCE_TYPE_UNKNOWN: _ClassVar[BalanceType]
    BALANCE_TYPE_ROUND_ROBIN: _ClassVar[BalanceType]
    BALANCE_TYPE_WEIGHTED_ROUND_ROBIN: _ClassVar[BalanceType]
    BALANCE_TYPE_CONSISTENT_HASH: _ClassVar[BalanceType]
    BALANCE_TYPE_LEAST_CONNECTIONS: _ClassVar[BalanceType]
    BALANCE_TYPE_SED: _ClassVar[BalanceType]
    BALANCE_TYPE_WEIGHTED_LEAST_CONNECTIONS: _ClassVar[BalanceType]
    BALANCE_TYPE_NEVER_QUEUE: _ClassVar[BalanceType]

class ServiceStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SERVICE_STATUS_UNKNOWN: _ClassVar[ServiceStatus]
    SERVICE_STATUS_HEALTHY: _ClassVar[ServiceStatus]
    SERVICE_STATUS_UNHEALTHY: _ClassVar[ServiceStatus]
    SERVICE_STATUS_MAINTENANCE: _ClassVar[ServiceStatus]
    SERVICE_STATUS_DRAINING: _ClassVar[ServiceStatus]
BALANCE_TYPE_UNKNOWN: BalanceType
BALANCE_TYPE_ROUND_ROBIN: BalanceType
BALANCE_TYPE_WEIGHTED_ROUND_ROBIN: BalanceType
BALANCE_TYPE_CONSISTENT_HASH: BalanceType
BALANCE_TYPE_LEAST_CONNECTIONS: BalanceType
BALANCE_TYPE_SED: BalanceType
BALANCE_TYPE_WEIGHTED_LEAST_CONNECTIONS: BalanceType
BALANCE_TYPE_NEVER_QUEUE: BalanceType
SERVICE_STATUS_UNKNOWN: ServiceStatus
SERVICE_STATUS_HEALTHY: ServiceStatus
SERVICE_STATUS_UNHEALTHY: ServiceStatus
SERVICE_STATUS_MAINTENANCE: ServiceStatus
SERVICE_STATUS_DRAINING: ServiceStatus

class Endpoint(_message.Message):
    __slots__ = ("address", "port", "weight")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    address: str
    port: int
    weight: int
    def __init__(self, address: _Optional[str] = ..., port: _Optional[int] = ..., weight: _Optional[int] = ...) -> None: ...

class LoadBalancer(_message.Message):
    __slots__ = ("type", "endpoints")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    type: BalanceType
    endpoints: _containers.RepeatedCompositeFieldContainer[Endpoint]
    def __init__(self, type: _Optional[_Union[BalanceType, str]] = ..., endpoints: _Optional[_Iterable[_Union[Endpoint, _Mapping]]] = ...) -> None: ...

class HealthCheckConfig(_message.Message):
    __slots__ = ("grpc_method", "http_path", "interval_seconds", "timeout_seconds", "healthy_threshold", "unhealthy_threshold", "enabled")
    GRPC_METHOD_FIELD_NUMBER: _ClassVar[int]
    HTTP_PATH_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    HEALTHY_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    UNHEALTHY_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    grpc_method: str
    http_path: str
    interval_seconds: int
    timeout_seconds: int
    healthy_threshold: int
    unhealthy_threshold: int
    enabled: bool
    def __init__(self, grpc_method: _Optional[str] = ..., http_path: _Optional[str] = ..., interval_seconds: _Optional[int] = ..., timeout_seconds: _Optional[int] = ..., healthy_threshold: _Optional[int] = ..., unhealthy_threshold: _Optional[int] = ..., enabled: bool = ...) -> None: ...

class ServiceInstance(_message.Message):
    __slots__ = ("service_name", "instance_id", "lb", "version", "metadata", "health_endpoint", "health_check_config", "registered_at", "status", "weight", "tags", "protocol", "tls_enabled", "protobuf_descriptor")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    LB_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    HEALTH_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CHECK_CONFIG_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    TLS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PROTOBUF_DESCRIPTOR_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    instance_id: str
    lb: LoadBalancer
    version: str
    metadata: _struct_pb2.Struct
    health_endpoint: str
    health_check_config: HealthCheckConfig
    registered_at: _timestamp_pb2.Timestamp
    status: ServiceStatus
    weight: int
    tags: _containers.ScalarMap[str, str]
    protocol: str
    tls_enabled: bool
    protobuf_descriptor: bytes
    def __init__(self, service_name: _Optional[str] = ..., instance_id: _Optional[str] = ..., lb: _Optional[_Union[LoadBalancer, _Mapping]] = ..., version: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., health_endpoint: _Optional[str] = ..., health_check_config: _Optional[_Union[HealthCheckConfig, _Mapping]] = ..., registered_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[ServiceStatus, str]] = ..., weight: _Optional[int] = ..., tags: _Optional[_Mapping[str, str]] = ..., protocol: _Optional[str] = ..., tls_enabled: bool = ..., protobuf_descriptor: _Optional[bytes] = ...) -> None: ...

class RegisterServiceRequest(_message.Message):
    __slots__ = ("service", "ttl")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    service: ServiceInstance
    ttl: int
    def __init__(self, service: _Optional[_Union[ServiceInstance, _Mapping]] = ..., ttl: _Optional[int] = ...) -> None: ...

class RegisterServiceResponse(_message.Message):
    __slots__ = ("success", "message", "lease_id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LEASE_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    lease_id: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., lease_id: _Optional[str] = ...) -> None: ...

class DeregisterServiceRequest(_message.Message):
    __slots__ = ("service_name", "instance_id")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    instance_id: str
    def __init__(self, service_name: _Optional[str] = ..., instance_id: _Optional[str] = ...) -> None: ...

class DeregisterServiceResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class GetServiceInstancesRequest(_message.Message):
    __slots__ = ("service_name", "tag_filters", "healthy_only")
    class TagFiltersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    TAG_FILTERS_FIELD_NUMBER: _ClassVar[int]
    HEALTHY_ONLY_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    tag_filters: _containers.ScalarMap[str, str]
    healthy_only: bool
    def __init__(self, service_name: _Optional[str] = ..., tag_filters: _Optional[_Mapping[str, str]] = ..., healthy_only: bool = ...) -> None: ...

class GetServiceInstancesResponse(_message.Message):
    __slots__ = ("instances", "total_count")
    INSTANCES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    instances: _containers.RepeatedCompositeFieldContainer[ServiceInstance]
    total_count: int
    def __init__(self, instances: _Optional[_Iterable[_Union[ServiceInstance, _Mapping]]] = ..., total_count: _Optional[int] = ...) -> None: ...

class ListServicesRequest(_message.Message):
    __slots__ = ("name_prefix", "tag_filters")
    class TagFiltersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_PREFIX_FIELD_NUMBER: _ClassVar[int]
    TAG_FILTERS_FIELD_NUMBER: _ClassVar[int]
    name_prefix: str
    tag_filters: _containers.ScalarMap[str, str]
    def __init__(self, name_prefix: _Optional[str] = ..., tag_filters: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ListServicesResponse(_message.Message):
    __slots__ = ("services", "total_count")
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    services: _containers.RepeatedCompositeFieldContainer[ServiceInstance]
    total_count: int
    def __init__(self, services: _Optional[_Iterable[_Union[ServiceInstance, _Mapping]]] = ..., total_count: _Optional[int] = ...) -> None: ...

class ServiceSummary(_message.Message):
    __slots__ = ("service_name", "instance_count", "healthy_count", "versions")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    HEALTHY_COUNT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    instance_count: int
    healthy_count: int
    versions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, service_name: _Optional[str] = ..., instance_count: _Optional[int] = ..., healthy_count: _Optional[int] = ..., versions: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateServiceHealthRequest(_message.Message):
    __slots__ = ("service_name", "instance_id", "status", "health_message")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HEALTH_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    instance_id: str
    status: ServiceStatus
    health_message: str
    def __init__(self, service_name: _Optional[str] = ..., instance_id: _Optional[str] = ..., status: _Optional[_Union[ServiceStatus, str]] = ..., health_message: _Optional[str] = ...) -> None: ...

class UpdateServiceHealthResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class ServiceHealthCheckRequest(_message.Message):
    __slots__ = ("service_name", "instance_id")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    instance_id: str
    def __init__(self, service_name: _Optional[str] = ..., instance_id: _Optional[str] = ...) -> None: ...

class ServiceHealthCheckResponse(_message.Message):
    __slots__ = ("instance_healths",)
    INSTANCE_HEALTHS_FIELD_NUMBER: _ClassVar[int]
    instance_healths: _containers.RepeatedCompositeFieldContainer[ServiceInstanceHealth]
    def __init__(self, instance_healths: _Optional[_Iterable[_Union[ServiceInstanceHealth, _Mapping]]] = ...) -> None: ...

class ServiceInstanceHealth(_message.Message):
    __slots__ = ("instance", "status", "message", "last_check")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LAST_CHECK_FIELD_NUMBER: _ClassVar[int]
    instance: ServiceInstance
    status: ServiceStatus
    message: str
    last_check: _timestamp_pb2.Timestamp
    def __init__(self, instance: _Optional[_Union[ServiceInstance, _Mapping]] = ..., status: _Optional[_Union[ServiceStatus, str]] = ..., message: _Optional[str] = ..., last_check: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UploadServiceConfigRequest(_message.Message):
    __slots__ = ("service_name", "config_version", "config_data", "description")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
    CONFIG_DATA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    config_version: str
    config_data: _struct_pb2.Struct
    description: str
    def __init__(self, service_name: _Optional[str] = ..., config_version: _Optional[str] = ..., config_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., description: _Optional[str] = ...) -> None: ...

class UploadServiceConfigResponse(_message.Message):
    __slots__ = ("success", "message", "config_key")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_KEY_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    config_key: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., config_key: _Optional[str] = ...) -> None: ...

class GetServiceConfigRequest(_message.Message):
    __slots__ = ("service_name", "config_version")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    config_version: str
    def __init__(self, service_name: _Optional[str] = ..., config_version: _Optional[str] = ...) -> None: ...

class GetServiceConfigResponse(_message.Message):
    __slots__ = ("config_data", "config_version", "updated_at", "description")
    CONFIG_DATA_FIELD_NUMBER: _ClassVar[int]
    CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    config_data: _struct_pb2.Struct
    config_version: str
    updated_at: _timestamp_pb2.Timestamp
    description: str
    def __init__(self, config_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., config_version: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., description: _Optional[str] = ...) -> None: ...

class UploadProtobufDescriptorRequest(_message.Message):
    __slots__ = ("service_name", "descriptor_version", "descriptor_data", "description")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_DATA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    descriptor_version: str
    descriptor_data: bytes
    description: str
    def __init__(self, service_name: _Optional[str] = ..., descriptor_version: _Optional[str] = ..., descriptor_data: _Optional[bytes] = ..., description: _Optional[str] = ...) -> None: ...

class UploadProtobufDescriptorResponse(_message.Message):
    __slots__ = ("success", "message", "descriptor_key", "discovered_services")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_KEY_FIELD_NUMBER: _ClassVar[int]
    DISCOVERED_SERVICES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    descriptor_key: str
    discovered_services: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., descriptor_key: _Optional[str] = ..., discovered_services: _Optional[_Iterable[str]] = ...) -> None: ...

class GetProtobufDescriptorRequest(_message.Message):
    __slots__ = ("service_name", "descriptor_version")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    descriptor_version: str
    def __init__(self, service_name: _Optional[str] = ..., descriptor_version: _Optional[str] = ...) -> None: ...

class GetProtobufDescriptorResponse(_message.Message):
    __slots__ = ("descriptor_data", "descriptor_version", "updated_at", "description", "services")
    DESCRIPTOR_DATA_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    descriptor_data: bytes
    descriptor_version: str
    updated_at: _timestamp_pb2.Timestamp
    description: str
    services: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, descriptor_data: _Optional[bytes] = ..., descriptor_version: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., description: _Optional[str] = ..., services: _Optional[_Iterable[str]] = ...) -> None: ...

class ListProtobufDescriptorsRequest(_message.Message):
    __slots__ = ("service_name_prefix",)
    SERVICE_NAME_PREFIX_FIELD_NUMBER: _ClassVar[int]
    service_name_prefix: str
    def __init__(self, service_name_prefix: _Optional[str] = ...) -> None: ...

class ListProtobufDescriptorsResponse(_message.Message):
    __slots__ = ("descriptors",)
    DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    descriptors: _containers.RepeatedCompositeFieldContainer[ProtobufDescriptorInfo]
    def __init__(self, descriptors: _Optional[_Iterable[_Union[ProtobufDescriptorInfo, _Mapping]]] = ...) -> None: ...

class ProtobufDescriptorInfo(_message.Message):
    __slots__ = ("service_name", "descriptor_version", "updated_at", "description", "services", "size_bytes")
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    descriptor_version: str
    updated_at: _timestamp_pb2.Timestamp
    description: str
    services: _containers.RepeatedScalarFieldContainer[str]
    size_bytes: int
    def __init__(self, service_name: _Optional[str] = ..., descriptor_version: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., description: _Optional[str] = ..., services: _Optional[_Iterable[str]] = ..., size_bytes: _Optional[int] = ...) -> None: ...

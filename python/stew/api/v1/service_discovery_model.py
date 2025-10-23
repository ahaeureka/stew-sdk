# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   service_discovery_model.py
@Time    :   2025-10-22 08:37:13
@Desc    :   Generated Pydantic models from protobuf definitions
"""

import datetime
from enum import Enum as _Enum
from google.protobuf import message as _message, message_factory
from protobuf_pydantic_gen.ext import model2protobuf, pool, protobuf2model
from pydantic import BaseModel, ConfigDict, Field as _Field
from typing import Dict, List, Optional, Type


class BalanceType(_Enum):
    BALANCE_TYPE_UNKNOWN = 0
    BALANCE_TYPE_ROUND_ROBIN = 1
    BALANCE_TYPE_WEIGHTED_ROUND_ROBIN = 2
    BALANCE_TYPE_CONSISTENT_HASH = 3
    BALANCE_TYPE_LEAST_CONNECTIONS = 4
    BALANCE_TYPE_SED = 5
    BALANCE_TYPE_WEIGHTED_LEAST_CONNECTIONS = 6
    BALANCE_TYPE_NEVER_QUEUE = 7


class ServiceStatus(_Enum):
    SERVICE_STATUS_UNKNOWN = 0
    SERVICE_STATUS_HEALTHY = 1
    SERVICE_STATUS_UNHEALTHY = 2
    SERVICE_STATUS_MAINTENANCE = 3
    SERVICE_STATUS_DRAINING = 4


class Endpoint(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    address: Optional[str] = _Field(default="")
    port: Optional[int] = _Field(default=0)
    weight: Optional[int] = _Field(default=0)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.Endpoint")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "Endpoint":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class LoadBalancer(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    type: Optional[BalanceType] = _Field(default=BalanceType(0))
    endpoints: Optional[List[Endpoint]] = _Field(default=None)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.LoadBalancer")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "LoadBalancer":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class HealthCheckConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    grpc_method: Optional[str] = _Field(default="")
    http_path: Optional[str] = _Field(default="")
    interval_seconds: Optional[int] = _Field(default=0)
    timeout_seconds: Optional[int] = _Field(default=0)
    healthy_threshold: Optional[int] = _Field(default=0)
    unhealthy_threshold: Optional[int] = _Field(default=0)
    enabled: Optional[bool] = _Field(default=False)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.HealthCheckConfig")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "HealthCheckConfig":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class ServiceInstance(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service_name: Optional[str] = _Field(default="")
    instance_id: Optional[str] = _Field(default="")
    lb: Optional[LoadBalancer] = _Field(default=None)
    version: Optional[str] = _Field(default="")
    metadata: Optional[Struct] = _Field(default=None)
    health_endpoint: Optional[str] = _Field(default="")
    health_check_config: Optional[HealthCheckConfig] = _Field(default=None)
    registered_at: Optional[datetime.datetime] = _Field(default=None)
    status: Optional[ServiceStatus] = _Field(default=ServiceStatus(0))
    weight: Optional[int] = _Field(default=0)
    tags: Optional[Dict[str, str]] = _Field(default=None)
    protocol: Optional[str] = _Field(default="")
    tls_enabled: Optional[bool] = _Field(default=False)
    protobuf_descriptor: Optional[bytes] = _Field(default=b"")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.ServiceInstance")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "ServiceInstance":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class RegisterServiceRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service: Optional[ServiceInstance] = _Field(default=None)
    ttl: Optional[int] = _Field(default=0)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.RegisterServiceRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "RegisterServiceRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class RegisterServiceResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    success: Optional[bool] = _Field(default=False)
    message: Optional[str] = _Field(default="")
    lease_id: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.RegisterServiceResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "RegisterServiceResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class DeregisterServiceRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service_name: Optional[str] = _Field(default="")
    instance_id: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.DeregisterServiceRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "DeregisterServiceRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class DeregisterServiceResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    success: Optional[bool] = _Field(default=False)
    message: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.DeregisterServiceResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "DeregisterServiceResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class GetServiceInstancesRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service_name: Optional[str] = _Field(default="")
    tag_filters: Optional[Dict[str, str]] = _Field(default=None)
    healthy_only: Optional[bool] = _Field(default=False)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.GetServiceInstancesRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "GetServiceInstancesRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class GetServiceInstancesResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    instances: Optional[List[ServiceInstance]] = _Field(default=None)
    total_count: Optional[int] = _Field(default=0)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.GetServiceInstancesResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "GetServiceInstancesResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class ListServicesRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    name_prefix: Optional[str] = _Field(default="")
    tag_filters: Optional[Dict[str, str]] = _Field(default=None)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.ListServicesRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "ListServicesRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class ListServicesResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    services: Optional[List[ServiceInstance]] = _Field(default=None)
    total_count: Optional[int] = _Field(default=0)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.ListServicesResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "ListServicesResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class ServiceSummary(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service_name: Optional[str] = _Field(default="")
    instance_count: Optional[int] = _Field(default=0)
    healthy_count: Optional[int] = _Field(default=0)
    versions: Optional[List[str]] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.ServiceSummary")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "ServiceSummary":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class UpdateServiceHealthRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service_name: Optional[str] = _Field(default="")
    instance_id: Optional[str] = _Field(default="")
    status: Optional[ServiceStatus] = _Field(default=ServiceStatus(0))
    health_message: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.UpdateServiceHealthRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UpdateServiceHealthRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class UpdateServiceHealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    success: Optional[bool] = _Field(default=False)
    message: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.UpdateServiceHealthResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UpdateServiceHealthResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class ServiceHealthCheckRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service_name: Optional[str] = _Field(default="")
    instance_id: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.ServiceHealthCheckRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "ServiceHealthCheckRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class ServiceHealthCheckResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    instance_healths: Optional[List[ServiceInstanceHealth]] = _Field(default=None)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.ServiceHealthCheckResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "ServiceHealthCheckResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class ServiceInstanceHealth(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    instance: Optional[ServiceInstance] = _Field(default=None)
    status: Optional[ServiceStatus] = _Field(default=ServiceStatus(0))
    message: Optional[str] = _Field(default="")
    last_check: Optional[datetime.datetime] = _Field(default=None)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.ServiceInstanceHealth")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "ServiceInstanceHealth":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class UploadServiceConfigRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service_name: Optional[str] = _Field(default="")
    config_version: Optional[str] = _Field(default="")
    config_data: Optional[Struct] = _Field(default=None)
    description: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.UploadServiceConfigRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UploadServiceConfigRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class UploadServiceConfigResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    success: Optional[bool] = _Field(default=False)
    message: Optional[str] = _Field(default="")
    config_key: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.UploadServiceConfigResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UploadServiceConfigResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class GetServiceConfigRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service_name: Optional[str] = _Field(default="")
    config_version: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.GetServiceConfigRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "GetServiceConfigRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class GetServiceConfigResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    config_data: Optional[Struct] = _Field(default=None)
    config_version: Optional[str] = _Field(default="")
    updated_at: Optional[datetime.datetime] = _Field(default=None)
    description: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.GetServiceConfigResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "GetServiceConfigResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class UploadProtobufDescriptorRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service_name: Optional[str] = _Field(default="")
    descriptor_version: Optional[str] = _Field(default="")
    descriptor_data: Optional[bytes] = _Field(default=b"")
    description: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName(
            "stew.api.v1.UploadProtobufDescriptorRequest"
        )
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UploadProtobufDescriptorRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class UploadProtobufDescriptorResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    success: Optional[bool] = _Field(default=False)
    message: Optional[str] = _Field(default="")
    descriptor_key: Optional[str] = _Field(default="")
    discovered_services: Optional[List[str]] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName(
            "stew.api.v1.UploadProtobufDescriptorResponse"
        )
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UploadProtobufDescriptorResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class GetProtobufDescriptorRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service_name: Optional[str] = _Field(default="")
    descriptor_version: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.GetProtobufDescriptorRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "GetProtobufDescriptorRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class GetProtobufDescriptorResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    descriptor_data: Optional[bytes] = _Field(default=b"")
    descriptor_version: Optional[str] = _Field(default="")
    updated_at: Optional[datetime.datetime] = _Field(default=None)
    description: Optional[str] = _Field(default="")
    services: Optional[List[str]] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.GetProtobufDescriptorResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "GetProtobufDescriptorResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class ListProtobufDescriptorsRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service_name_prefix: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName(
            "stew.api.v1.ListProtobufDescriptorsRequest"
        )
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "ListProtobufDescriptorsRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class ListProtobufDescriptorsResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    descriptors: Optional[List[ProtobufDescriptorInfo]] = _Field(default=None)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName(
            "stew.api.v1.ListProtobufDescriptorsResponse"
        )
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "ListProtobufDescriptorsResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class ProtobufDescriptorInfo(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    service_name: Optional[str] = _Field(default="")
    descriptor_version: Optional[str] = _Field(default="")
    updated_at: Optional[datetime.datetime] = _Field(default=None)
    description: Optional[str] = _Field(default="")
    services: Optional[List[str]] = _Field(default="")
    size_bytes: Optional[int] = _Field(default=0)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.ProtobufDescriptorInfo")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "ProtobufDescriptorInfo":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)

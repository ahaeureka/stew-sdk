"""Stew Gateway runtime entitlement gRPC clients."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import grpc
import grpc.aio

from stew.api.v1 import entitlement_model as _ent_model
from stew.api.v1 import entitlement_pb2 as _ent_pb
from stew.api.v1 import entitlement_pb2_grpc as _ent_grpc

from ._discovery.errors import DiscoveryError
from ._discovery.helpers import (
    AioGatewayClientBase,
    MetadataEntry,
    SyncGatewayClientBase,
    wrap_rpc_error,
)

EntitlementError = DiscoveryError


def _coerce_protobuf_message(value: Any, message_type: type[Any]) -> Any:
    if isinstance(value, message_type):
        return value
    if hasattr(value, "to_protobuf"):
        message = value.to_protobuf()
        if isinstance(message, message_type):
            return message
    raise TypeError(f"Expected {message_type.__name__}, got {type(value).__name__}")


class EntitlementClient(AioGatewayClientBase[_ent_grpc.EntitlementServiceStub]):
    """Async gRPC client for stew.api.v1.EntitlementService.

    This client only exposes runtime entitlement reads and quota checks for
    business-side callers. Plan, subscription, and renewal management stay on
    the gateway-side admin surface.
    """

    def _create_stub(
        self, channel: grpc.aio.Channel
    ) -> _ent_grpc.EntitlementServiceStub:
        return _ent_grpc.EntitlementServiceStub(channel)

    async def _call(self, coro: Any) -> Any:
        try:
            return await coro
        except grpc.RpcError as exc:
            raise wrap_rpc_error(exc) from exc

    async def get_quota_usage(
        self,
        request: _ent_model.GetQuotaUsageRequest
        | _ent_pb.GetQuotaUsageRequest
        | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        quota_key: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.QuotaUsage:
        message = (
            _coerce_protobuf_message(request, _ent_pb.GetQuotaUsageRequest)
            if request is not None
            else _ent_pb.GetQuotaUsageRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                quota_key=quota_key,
            )
        )
        response = await self._call(
            self._s.GetQuotaUsage(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _ent_model.QuotaUsage.from_protobuf(response)

    async def increment_quota(
        self,
        request: _ent_model.IncrementQuotaRequest
        | _ent_pb.IncrementQuotaRequest
        | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        quota_key: str = "",
        delta: int = 0,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.QuotaUsage:
        message = (
            _coerce_protobuf_message(request, _ent_pb.IncrementQuotaRequest)
            if request is not None
            else _ent_pb.IncrementQuotaRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                quota_key=quota_key,
                delta=delta,
            )
        )
        response = await self._call(
            self._s.IncrementQuota(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _ent_model.QuotaUsage.from_protobuf(response)

    async def check_quota(
        self,
        request: _ent_model.CheckQuotaRequest | _ent_pb.CheckQuotaRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        quota_key: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.CheckQuotaResponse:
        message = (
            _coerce_protobuf_message(request, _ent_pb.CheckQuotaRequest)
            if request is not None
            else _ent_pb.CheckQuotaRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                quota_key=quota_key,
            )
        )
        response = await self._call(
            self._s.CheckQuota(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _ent_model.CheckQuotaResponse.from_protobuf(response)

    async def get_my_entitlement(
        self,
        request: _ent_model.GetMyEntitlementRequest
        | _ent_pb.GetMyEntitlementRequest
        | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.ResolvedEntitlementResponse:
        message = (
            _coerce_protobuf_message(request, _ent_pb.GetMyEntitlementRequest)
            if request is not None
            else _ent_pb.GetMyEntitlementRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
            )
        )
        response = await self._call(
            self._s.GetMyEntitlement(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _ent_model.ResolvedEntitlementResponse.from_protobuf(response)

    async def check_feature(
        self,
        request: _ent_model.CheckFeatureRequest
        | _ent_pb.CheckFeatureRequest
        | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        feature_key: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.CheckFeatureResponse:
        message = (
            _coerce_protobuf_message(request, _ent_pb.CheckFeatureRequest)
            if request is not None
            else _ent_pb.CheckFeatureRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                feature_key=feature_key,
            )
        )
        response = await self._call(
            self._s.CheckFeature(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _ent_model.CheckFeatureResponse.from_protobuf(response)


class SyncEntitlementClient(SyncGatewayClientBase[EntitlementClient]):
    """Synchronous facade over :class:`EntitlementClient`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(EntitlementClient, *args, **kwargs)

    def get_quota_usage(self, *args: Any, **kwargs: Any) -> _ent_model.QuotaUsage:
        return self._run(self._client.get_quota_usage(*args, **kwargs))

    def increment_quota(self, *args: Any, **kwargs: Any) -> _ent_model.QuotaUsage:
        return self._run(self._client.increment_quota(*args, **kwargs))

    def check_quota(self, *args: Any, **kwargs: Any) -> _ent_model.CheckQuotaResponse:
        return self._run(self._client.check_quota(*args, **kwargs))

    def get_my_entitlement(
        self, *args: Any, **kwargs: Any
    ) -> _ent_model.ResolvedEntitlementResponse:
        return self._run(self._client.get_my_entitlement(*args, **kwargs))

    def check_feature(
        self, *args: Any, **kwargs: Any
    ) -> _ent_model.CheckFeatureResponse:
        return self._run(self._client.check_feature(*args, **kwargs))


__all__ = [
    "EntitlementClient",
    "EntitlementError",
    "SyncEntitlementClient",
]

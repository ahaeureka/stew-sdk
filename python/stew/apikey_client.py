"""Stew Gateway API key gRPC clients."""

from __future__ import annotations

import datetime
from typing import Any

import grpc
import grpc.aio

from stew.api.v1 import apikey_model as _apikey_model
from stew.api.v1 import apikey_pb2 as _apikey_pb
from stew.api.v1 import apikey_pb2_grpc as _apikey_grpc

from ._discovery.errors import DiscoveryError
from ._discovery.helpers import (
    AioGatewayClientBase,
    MetadataEntry,
    SyncGatewayClientBase,
    wrap_rpc_error,
)

ApiKeyError = DiscoveryError


def _coerce_protobuf_message(value: Any, message_type: type[Any]) -> Any:
    if isinstance(value, message_type):
        return value
    if hasattr(value, "to_protobuf"):
        message = value.to_protobuf()
        if isinstance(message, message_type):
            return message
    raise TypeError(f"Expected {message_type.__name__}, got {type(value).__name__}")


class ApiKeyClient(AioGatewayClientBase[_apikey_grpc.ApiKeyServiceStub]):
    """Async gRPC client for stew.api.v1.ApiKeyService.

    The backend requires x-business-id for the main API key management flows,
    so the business_id parameter on this client should normally be provided.
    """

    def _create_stub(self, channel: grpc.aio.Channel) -> _apikey_grpc.ApiKeyServiceStub:
        return _apikey_grpc.ApiKeyServiceStub(channel)

    async def _call(self, coro: Any) -> Any:
        try:
            return await coro
        except grpc.RpcError as exc:
            raise wrap_rpc_error(exc) from exc

    async def create_api_key(
        self,
        request: _apikey_model.CreateApiKeyRequest | _apikey_pb.CreateApiKeyRequest | None = None,
        *,
        name: str = "",
        user_id: str = "",
        scopes: list[str] | None = None,
        expires_at: datetime.datetime | None = None,
        metadata: dict[str, str] | None = None,
        description: str = "",
        business_id: str = "",
        extra_metadata: list[MetadataEntry] | tuple[MetadataEntry, ...] = (),
    ) -> _apikey_model.CreateApiKeyResponse:
        message = (
            _coerce_protobuf_message(request, _apikey_pb.CreateApiKeyRequest)
            if request is not None
            else _apikey_model.CreateApiKeyRequest(
                name=name,
                user_id=user_id,
                scopes=scopes or [],
                expires_at=expires_at,
                metadata=metadata,
                description=description,
            ).to_protobuf()
        )
        response = await self._call(
            self._s.CreateApiKey(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _apikey_model.CreateApiKeyResponse.from_protobuf(response)

    async def list_api_keys(
        self,
        request: _apikey_model.ListApiKeysRequest | _apikey_pb.ListApiKeysRequest | None = None,
        *,
        user_id: str = "",
        page: int = 0,
        limit: int = 0,
        include_inactive: bool = False,
        business_id: str = "",
        extra_metadata: list[MetadataEntry] | tuple[MetadataEntry, ...] = (),
    ) -> _apikey_model.ListApiKeysResponse:
        message = (
            _coerce_protobuf_message(request, _apikey_pb.ListApiKeysRequest)
            if request is not None
            else _apikey_model.ListApiKeysRequest(
                user_id=user_id,
                page=page,
                limit=limit,
                include_inactive=include_inactive,
            ).to_protobuf()
        )
        response = await self._call(
            self._s.ListApiKeys(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _apikey_model.ListApiKeysResponse.from_protobuf(response)

    async def get_api_key(
        self,
        request: _apikey_model.GetApiKeyRequest | _apikey_pb.GetApiKeyRequest | None = None,
        *,
        key_id: str = "",
        business_id: str = "",
        extra_metadata: list[MetadataEntry] | tuple[MetadataEntry, ...] = (),
    ) -> _apikey_model.ApiKey:
        message = (
            _coerce_protobuf_message(request, _apikey_pb.GetApiKeyRequest)
            if request is not None
            else _apikey_pb.GetApiKeyRequest(id=key_id)
        )
        response = await self._call(
            self._s.GetApiKey(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _apikey_model.ApiKey.from_protobuf(response)

    async def update_api_key(
        self,
        request: _apikey_model.UpdateApiKeyRequest | _apikey_pb.UpdateApiKeyRequest | None = None,
        *,
        key_id: str = "",
        name: str = "",
        scopes: list[str] | None = None,
        expires_at: datetime.datetime | None = None,
        is_active: bool = False,
        metadata: dict[str, str] | None = None,
        business_id: str = "",
        extra_metadata: list[MetadataEntry] | tuple[MetadataEntry, ...] = (),
    ) -> _apikey_model.ApiKey:
        message = (
            _coerce_protobuf_message(request, _apikey_pb.UpdateApiKeyRequest)
            if request is not None
            else _apikey_model.UpdateApiKeyRequest(
                id=key_id,
                name=name,
                scopes=scopes or [],
                expires_at=expires_at,
                is_active=is_active,
                metadata=metadata,
            ).to_protobuf()
        )
        response = await self._call(
            self._s.UpdateApiKey(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _apikey_model.ApiKey.from_protobuf(response)

    async def delete_api_key(
        self,
        request: _apikey_model.DeleteApiKeyRequest | _apikey_pb.DeleteApiKeyRequest | None = None,
        *,
        key_id: str = "",
        business_id: str = "",
        extra_metadata: list[MetadataEntry] | tuple[MetadataEntry, ...] = (),
    ) -> None:
        message = (
            _coerce_protobuf_message(request, _apikey_pb.DeleteApiKeyRequest)
            if request is not None
            else _apikey_pb.DeleteApiKeyRequest(id=key_id)
        )
        await self._call(
            self._s.DeleteApiKey(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )

    async def validate_api_key(
        self,
        request: _apikey_model.ValidateApiKeyRequest | _apikey_pb.ValidateApiKeyRequest | None = None,
        *,
        api_key: str = "",
        required_scopes: list[str] | None = None,
        business_id: str = "",
        extra_metadata: list[MetadataEntry] | tuple[MetadataEntry, ...] = (),
    ) -> _apikey_model.ValidateApiKeyResponse:
        message = (
            _coerce_protobuf_message(request, _apikey_pb.ValidateApiKeyRequest)
            if request is not None
            else _apikey_model.ValidateApiKeyRequest(
                api_key=api_key,
                required_scopes=required_scopes or [],
            ).to_protobuf()
        )
        response = await self._call(
            self._s.ValidateApiKey(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _apikey_model.ValidateApiKeyResponse.from_protobuf(response)

    async def rotate_api_key(
        self,
        request: _apikey_model.RotateApiKeyRequest | _apikey_pb.RotateApiKeyRequest | None = None,
        *,
        key_id: str = "",
        business_id: str = "",
        extra_metadata: list[MetadataEntry] | tuple[MetadataEntry, ...] = (),
    ) -> _apikey_model.RotateApiKeyResponse:
        message = (
            _coerce_protobuf_message(request, _apikey_pb.RotateApiKeyRequest)
            if request is not None
            else _apikey_pb.RotateApiKeyRequest(id=key_id)
        )
        response = await self._call(
            self._s.RotateApiKey(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _apikey_model.RotateApiKeyResponse.from_protobuf(response)


class SyncApiKeyClient(SyncGatewayClientBase[ApiKeyClient]):
    """Synchronous facade over :class:`ApiKeyClient`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(ApiKeyClient, *args, **kwargs)

    def create_api_key(self, *args: Any, **kwargs: Any) -> _apikey_model.CreateApiKeyResponse:
        return self._run(self._client.create_api_key(*args, **kwargs))

    def list_api_keys(self, *args: Any, **kwargs: Any) -> _apikey_model.ListApiKeysResponse:
        return self._run(self._client.list_api_keys(*args, **kwargs))

    def get_api_key(self, *args: Any, **kwargs: Any) -> _apikey_model.ApiKey:
        return self._run(self._client.get_api_key(*args, **kwargs))

    def update_api_key(self, *args: Any, **kwargs: Any) -> _apikey_model.ApiKey:
        return self._run(self._client.update_api_key(*args, **kwargs))

    def delete_api_key(self, *args: Any, **kwargs: Any) -> None:
        self._run(self._client.delete_api_key(*args, **kwargs))

    def validate_api_key(
        self, *args: Any, **kwargs: Any
    ) -> _apikey_model.ValidateApiKeyResponse:
        return self._run(self._client.validate_api_key(*args, **kwargs))

    def rotate_api_key(self, *args: Any, **kwargs: Any) -> _apikey_model.RotateApiKeyResponse:
        return self._run(self._client.rotate_api_key(*args, **kwargs))


__all__ = [
    "ApiKeyClient",
    "ApiKeyError",
    "SyncApiKeyClient",
]
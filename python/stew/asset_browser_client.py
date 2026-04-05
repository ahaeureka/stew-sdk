"""Stew Gateway business asset browser gRPC clients."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Sequence
from types import TracebackType
from typing import Any

import grpc
import grpc.aio

from stew.api.v1 import business_asset_browser_model as _ab_model
from stew.api.v1 import business_asset_browser_pb2 as _ab_pb
from stew.api.v1 import business_asset_browser_pb2_grpc as _ab_grpc

from ._discovery.errors import ConflictError, DiscoveryError
from ._discovery.helpers import make_metadata, wrap_rpc_error

AssetBrowserError = DiscoveryError


class AssetBrowserClient:
    """Async gRPC client for stew.api.v1.BusinessAssetBrowserService."""

    def __init__(
        self,
        gateway_addr: str,
        *,
        app_secret: str = "",
        api_key: str = "",
        use_tls: bool = False,
        timeout: float = 30.0,
    ) -> None:
        self._addr = gateway_addr
        self._api_key = (
            app_secret
            or api_key
            or os.environ.get("APP_SECRET")
            or os.environ.get("SERVICE_API_KEY", "")
        )
        self._use_tls = use_tls
        self._timeout = timeout
        self._channel: grpc.aio.Channel | None = None
        self._stub: _ab_grpc.BusinessAssetBrowserServiceStub | None = None

    async def connect(self) -> None:
        if self._use_tls:
            credentials = grpc.ssl_channel_credentials()
            self._channel = grpc.aio.secure_channel(self._addr, credentials)
        else:
            self._channel = grpc.aio.insecure_channel(self._addr)
        self._stub = _ab_grpc.BusinessAssetBrowserServiceStub(self._channel)

    async def close(self) -> None:
        if self._channel is not None:
            await self._channel.close()
            self._channel = None
        self._stub = None

    async def __aenter__(self) -> "AssetBrowserClient":
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()

    @property
    def _s(self) -> _ab_grpc.BusinessAssetBrowserServiceStub:
        if self._stub is None:
            raise RuntimeError(
                "Client is not connected. Call connect() or use async with."
            )
        return self._stub

    def _meta(
        self,
        extra_metadata: Sequence[tuple[str, str]] = (),
    ) -> list[tuple[str, str]]:
        return make_metadata(self._api_key, extra_metadata=extra_metadata)

    async def _call(self, coro: Any) -> Any:
        try:
            return await coro
        except grpc.RpcError as exc:
            raise wrap_rpc_error(exc) from exc

    # ===== Collection =====

    async def list_collections(
        self,
        *,
        asset_space: str = "",
        scope_kind: _ab_model.AssetScopeKind = _ab_model.AssetScopeKind.ASSET_SCOPE_KIND_UNSPECIFIED,
        scope_value: str = "",
        page_size: int = 0,
        page_token: str = "",
    ) -> _ab_model.ListAssetCollectionsResponse:
        response = await self._call(
            self._s.ListAssetCollections(
                _ab_pb.ListAssetCollectionsRequest(
                    asset_space=asset_space,
                    scope_kind=scope_kind.value,
                    scope_value=scope_value,
                    page_size=page_size,
                    page_token=page_token,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.ListAssetCollectionsResponse.from_protobuf(response)

    async def get_collection(
        self,
        *,
        asset_space: str,
        asset_id: str,
    ) -> _ab_model.AssetCollection:
        response = await self._call(
            self._s.GetAssetCollection(
                _ab_pb.GetAssetCollectionRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.AssetCollection.from_protobuf(response)

    # ===== Tree =====

    async def list_tree(
        self,
        *,
        asset_space: str,
        asset_id: str,
        version_id: str = "",
        folder: str = "",
        page_size: int = 0,
        page_token: str = "",
        include_files: bool = True,
        include_directories: bool = True,
    ) -> _ab_model.ListAssetTreeResponse:
        response = await self._call(
            self._s.ListAssetTree(
                _ab_pb.ListAssetTreeRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    version_id=version_id,
                    folder=folder,
                    page_size=page_size,
                    page_token=page_token,
                    include_files=include_files,
                    include_directories=include_directories,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.ListAssetTreeResponse.from_protobuf(response)

    # ===== Versions =====

    async def list_versions(
        self,
        *,
        asset_space: str,
        asset_id: str,
        include_archived: bool = False,
    ) -> _ab_model.ListAssetVersionsResponse:
        response = await self._call(
            self._s.ListAssetVersions(
                _ab_pb.ListAssetVersionsRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    include_archived=include_archived,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.ListAssetVersionsResponse.from_protobuf(response)

    async def get_version(
        self,
        *,
        asset_space: str,
        asset_id: str,
        version_id: str,
    ) -> _ab_model.GetAssetVersionResponse:
        response = await self._call(
            self._s.GetAssetVersion(
                _ab_pb.GetAssetVersionRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    version_id=version_id,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.GetAssetVersionResponse.from_protobuf(response)

    # ===== Draft lifecycle =====

    async def create_draft(
        self,
        *,
        asset_space: str,
        asset_id: str,
        base_version_id: str = "",
        draft_version_id: str = "",
        description: str = "",
    ) -> _ab_model.CreateDraftVersionResponse:
        response = await self._call(
            self._s.CreateDraftVersion(
                _ab_pb.CreateDraftVersionRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    base_version_id=base_version_id,
                    draft_version_id=draft_version_id,
                    description=description,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.CreateDraftVersionResponse.from_protobuf(response)

    async def discard_draft(
        self,
        *,
        asset_space: str,
        asset_id: str,
        draft_version_id: str,
    ) -> None:
        await self._call(
            self._s.DiscardDraftVersion(
                _ab_pb.DiscardDraftVersionRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    draft_version_id=draft_version_id,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )

    async def publish_draft(
        self,
        *,
        asset_space: str,
        asset_id: str,
        draft_version_id: str,
        version_id: str = "",
        description: str = "",
        previous_version_id: str = "",
    ) -> _ab_model.PublishDraftVersionResponse:
        response = await self._call(
            self._s.PublishDraftVersion(
                _ab_pb.PublishDraftVersionRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    draft_version_id=draft_version_id,
                    version_id=version_id,
                    description=description,
                    previous_version_id=previous_version_id,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.PublishDraftVersionResponse.from_protobuf(response)

    # ===== Draft editing =====

    async def get_entry_text(
        self,
        *,
        asset_space: str,
        asset_id: str,
        version_id: str,
        path: str,
    ) -> _ab_model.GetAssetEntryTextResponse:
        response = await self._call(
            self._s.GetAssetEntryText(
                _ab_pb.GetAssetEntryTextRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    version_id=version_id,
                    path=path,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.GetAssetEntryTextResponse.from_protobuf(response)

    async def update_draft_text(
        self,
        *,
        asset_space: str,
        asset_id: str,
        draft_version_id: str,
        path: str,
        text: str,
        content_type: str = "",
        expected_entry_revision: int = 0,
        commit_message: str = "",
    ) -> _ab_model.UpdateDraftTextEntryResponse:
        response = await self._call(
            self._s.UpdateDraftTextEntry(
                _ab_pb.UpdateDraftTextEntryRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    draft_version_id=draft_version_id,
                    path=path,
                    text=text,
                    content_type=content_type,
                    expected_entry_revision=expected_entry_revision,
                    commit_message=commit_message,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.UpdateDraftTextEntryResponse.from_protobuf(response)

    async def rename_draft_entry(
        self,
        *,
        asset_space: str,
        asset_id: str,
        draft_version_id: str,
        path: str,
        new_path: str,
    ) -> _ab_model.RenameDraftEntryResponse:
        response = await self._call(
            self._s.RenameDraftEntry(
                _ab_pb.RenameDraftEntryRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    draft_version_id=draft_version_id,
                    path=path,
                    new_path=new_path,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.RenameDraftEntryResponse.from_protobuf(response)

    async def delete_draft_entry(
        self,
        *,
        asset_space: str,
        asset_id: str,
        draft_version_id: str,
        path: str,
    ) -> _ab_model.DeleteDraftEntryResponse:
        response = await self._call(
            self._s.DeleteDraftEntry(
                _ab_pb.DeleteDraftEntryRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    draft_version_id=draft_version_id,
                    path=path,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.DeleteDraftEntryResponse.from_protobuf(response)

    # ===== Diff =====

    async def diff_versions(
        self,
        *,
        asset_space: str,
        asset_id: str,
        left_version_id: str,
        right_version_id: str,
        diff_mode: _ab_model.AssetDiffMode = _ab_model.AssetDiffMode.ASSET_DIFF_MODE_UNSPECIFIED,
        path_prefix: str = "",
        page_size: int = 0,
        page_token: str = "",
    ) -> _ab_model.DiffAssetVersionsResponse:
        response = await self._call(
            self._s.DiffAssetVersions(
                _ab_pb.DiffAssetVersionsRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    left_version_id=left_version_id,
                    right_version_id=right_version_id,
                    diff_mode=diff_mode.value,
                    path_prefix=path_prefix,
                    page_size=page_size,
                    page_token=page_token,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.DiffAssetVersionsResponse.from_protobuf(response)

    async def diff_draft(
        self,
        *,
        asset_space: str,
        asset_id: str,
        draft_version_id: str,
        base_version_id: str = "",
        diff_mode: _ab_model.AssetDiffMode = _ab_model.AssetDiffMode.ASSET_DIFF_MODE_UNSPECIFIED,
        path_prefix: str = "",
        page_size: int = 0,
        page_token: str = "",
    ) -> _ab_model.DiffAssetDraftResponse:
        response = await self._call(
            self._s.DiffAssetDraft(
                _ab_pb.DiffAssetDraftRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    draft_version_id=draft_version_id,
                    base_version_id=base_version_id,
                    diff_mode=diff_mode.value,
                    path_prefix=path_prefix,
                    page_size=page_size,
                    page_token=page_token,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.DiffAssetDraftResponse.from_protobuf(response)

    async def get_diff_entry_detail(
        self,
        *,
        asset_space: str,
        asset_id: str,
        left_version_id: str,
        right_version_id: str,
        path: str,
        diff_mode: _ab_model.AssetDiffMode = _ab_model.AssetDiffMode.ASSET_DIFF_MODE_UNSPECIFIED,
    ) -> _ab_model.GetAssetDiffEntryDetailResponse:
        response = await self._call(
            self._s.GetAssetDiffEntryDetail(
                _ab_pb.GetAssetDiffEntryDetailRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    left_version_id=left_version_id,
                    right_version_id=right_version_id,
                    path=path,
                    diff_mode=diff_mode.value,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.GetAssetDiffEntryDetailResponse.from_protobuf(response)

    # ===== Activation =====

    async def activate_version(
        self,
        *,
        asset_space: str,
        asset_id: str,
        target_version_id: str,
        previous_version_id: str = "",
    ) -> _ab_model.ActivateAssetVersionResponse:
        response = await self._call(
            self._s.ActivateAssetVersion(
                _ab_pb.ActivateAssetVersionRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    target_version_id=target_version_id,
                    previous_version_id=previous_version_id,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        return _ab_model.ActivateAssetVersionResponse.from_protobuf(response)


class SyncAssetBrowserClient:
    """Synchronous facade over :class:`AssetBrowserClient`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._client = AssetBrowserClient(*args, **kwargs)
        self._loop = asyncio.new_event_loop()

    def _run(self, coro: Any) -> Any:
        return self._loop.run_until_complete(coro)

    def __enter__(self) -> "SyncAssetBrowserClient":
        self._run(self._client.connect())
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self._run(self._client.close())
        self._loop.close()

    def list_collections(
        self, **kwargs: Any
    ) -> _ab_model.ListAssetCollectionsResponse:
        return self._run(self._client.list_collections(**kwargs))

    def get_collection(self, **kwargs: Any) -> _ab_model.AssetCollection:
        return self._run(self._client.get_collection(**kwargs))

    def list_tree(self, **kwargs: Any) -> _ab_model.ListAssetTreeResponse:
        return self._run(self._client.list_tree(**kwargs))

    def list_versions(
        self, **kwargs: Any
    ) -> _ab_model.ListAssetVersionsResponse:
        return self._run(self._client.list_versions(**kwargs))

    def get_version(self, **kwargs: Any) -> _ab_model.GetAssetVersionResponse:
        return self._run(self._client.get_version(**kwargs))

    def create_draft(
        self, **kwargs: Any
    ) -> _ab_model.CreateDraftVersionResponse:
        return self._run(self._client.create_draft(**kwargs))

    def discard_draft(self, **kwargs: Any) -> None:
        self._run(self._client.discard_draft(**kwargs))

    def publish_draft(
        self, **kwargs: Any
    ) -> _ab_model.PublishDraftVersionResponse:
        return self._run(self._client.publish_draft(**kwargs))

    def get_entry_text(
        self, **kwargs: Any
    ) -> _ab_model.GetAssetEntryTextResponse:
        return self._run(self._client.get_entry_text(**kwargs))

    def update_draft_text(
        self, **kwargs: Any
    ) -> _ab_model.UpdateDraftTextEntryResponse:
        return self._run(self._client.update_draft_text(**kwargs))

    def rename_draft_entry(
        self, **kwargs: Any
    ) -> _ab_model.RenameDraftEntryResponse:
        return self._run(self._client.rename_draft_entry(**kwargs))

    def delete_draft_entry(
        self, **kwargs: Any
    ) -> _ab_model.DeleteDraftEntryResponse:
        return self._run(self._client.delete_draft_entry(**kwargs))

    def diff_versions(
        self, **kwargs: Any
    ) -> _ab_model.DiffAssetVersionsResponse:
        return self._run(self._client.diff_versions(**kwargs))

    def diff_draft(self, **kwargs: Any) -> _ab_model.DiffAssetDraftResponse:
        return self._run(self._client.diff_draft(**kwargs))

    def get_diff_entry_detail(
        self, **kwargs: Any
    ) -> _ab_model.GetAssetDiffEntryDetailResponse:
        return self._run(self._client.get_diff_entry_detail(**kwargs))

    def activate_version(
        self, **kwargs: Any
    ) -> _ab_model.ActivateAssetVersionResponse:
        return self._run(self._client.activate_version(**kwargs))


__all__ = [
    "AssetBrowserClient",
    "AssetBrowserError",
    "SyncAssetBrowserClient",
]

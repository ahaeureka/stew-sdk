"""Stew Gateway business asset browser gRPC clients.

Public version-related fields and parameters use the business version ID from
``asset_versions.version_id`` instead of the internal database UUID. The
gateway still accepts internal UUIDs in request parameters for backward
compatibility, but new integrations should persist and pass the business
version IDs only.
"""

from __future__ import annotations

import asyncio
import os
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import grpc
import grpc.aio

from stew.api.v1 import business_asset_browser_model as _ab_model
from stew.api.v1 import business_asset_browser_pb2 as _ab_pb
from stew.api.v1 import business_asset_browser_pb2_grpc as _ab_grpc
from stew.api.v1 import file_storage_model as _fs_model
from stew.api.v1 import file_storage_pb2 as _fs_pb

from ._discovery.errors import ConflictError, DiscoveryError
from ._discovery.helpers import AioGatewayClientBase, SyncGatewayClientBase, wrap_rpc_error

AssetBrowserError = DiscoveryError


@dataclass
class ExportedAsset:
    data: bytes
    content_type: str
    filename: str = ""
    content_disposition: str = ""
    etag: str = ""
    metadata: _fs_model.DownloadFileHttpMetadata | None = None


@dataclass
class SavedExportedAsset:
    path: str
    bytes_written: int
    content_type: str
    filename: str = ""
    content_disposition: str = ""
    etag: str = ""
    metadata: _fs_model.DownloadFileHttpMetadata | None = None


def _extract_export_metadata(response: Any) -> _fs_model.DownloadFileHttpMetadata | None:
    for extension in response.extensions:
        metadata = _fs_pb.DownloadFileHttpMetadata()
        if extension.Unpack(metadata):
            return _fs_model.DownloadFileHttpMetadata.from_protobuf(metadata)
    return None


def _resolve_export_filename(
    *,
    asset_id: str,
    path: str,
    metadata: _fs_model.DownloadFileHttpMetadata | None,
) -> str:
    if metadata is not None and metadata.filename:
        return metadata.filename

    normalized_path = path.strip("/")
    if normalized_path:
        return normalized_path.split("/")[-1]

    return f"{asset_id}.bin"


class AssetBrowserClient(AioGatewayClientBase[_ab_grpc.BusinessAssetBrowserServiceStub]):
    """Async gRPC client for stew.api.v1.BusinessAssetBrowserService.

    All public version_id, active_version_id, draft_version_id and
    base_version_id values exposed by this client are business version IDs.
    """

    def _create_stub(self, channel: grpc.aio.Channel) -> _ab_grpc.BusinessAssetBrowserServiceStub:
        return _ab_grpc.BusinessAssetBrowserServiceStub(channel)

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

    async def ensure_collection(
        self,
        *,
        asset_space: str,
        asset_id: str,
        scope_kind: _ab_model.AssetScopeKind = _ab_model.AssetScopeKind.ASSET_SCOPE_KIND_SERVICE,
        scope_value: str = "",
        display_name: str = "",
        description: str = "",
    ) -> _ab_model.AssetCollection:
        response = await self._call(
            self._s.EnsureAssetCollection(
                _ab_pb.EnsureAssetCollectionRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    scope_kind=scope_kind.value,
                    scope_value=scope_value,
                    display_name=display_name,
                    description=description,
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

    async def export_entry(
        self,
        *,
        asset_space: str,
        asset_id: str,
        version_id: str = "",
        path: str = "",
    ) -> ExportedAsset:
        response = await self._call(
            self._s.ExportAssetEntry(
                _ab_pb.ExportAssetEntryRequest(
                    asset_space=asset_space,
                    asset_id=asset_id,
                    version_id=version_id,
                    path=path,
                ),
                metadata=self._meta(),
                timeout=self._timeout,
            )
        )
        metadata = _extract_export_metadata(response)
        return ExportedAsset(
            data=response.data,
            content_type=response.content_type,
            filename=_resolve_export_filename(
                asset_id=asset_id,
                path=path,
                metadata=metadata,
            ),
            content_disposition=(
                metadata.content_disposition
                if metadata is not None and metadata.content_disposition
                else ""
            ),
            etag=metadata.etag if metadata is not None and metadata.etag else "",
            metadata=metadata,
        )

    async def export_entry_to_path(
        self,
        *,
        asset_space: str,
        asset_id: str,
        version_id: str = "",
        path: str = "",
        output_path: str = "",
        replace_existing: bool = False,
    ) -> SavedExportedAsset:
        exported = await self.export_entry(
            asset_space=asset_space,
            asset_id=asset_id,
            version_id=version_id,
            path=path,
        )
        resolved_output_path = output_path or exported.filename or f"{asset_id}.bin"

        parent = os.path.dirname(os.path.abspath(resolved_output_path))
        if parent:
            os.makedirs(parent, exist_ok=True)

        if os.path.exists(resolved_output_path) and not replace_existing:
            raise FileExistsError(
                f"Output file already exists: {resolved_output_path}. "
                "Pass replace_existing=True to overwrite it."
            )

        with open(resolved_output_path, "wb") as fh:
            fh.write(exported.data)

        return SavedExportedAsset(
            path=resolved_output_path,
            bytes_written=len(exported.data),
            content_type=exported.content_type,
            filename=exported.filename,
            content_disposition=exported.content_disposition,
            etag=exported.etag,
            metadata=exported.metadata,
        )


class SyncAssetBrowserClient(SyncGatewayClientBase[AssetBrowserClient]):
    """Synchronous facade over :class:`AssetBrowserClient`.

    Version-related fields keep the same business-ID semantics as the async
    client.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(AssetBrowserClient, *args, **kwargs)

    def list_collections(
        self, **kwargs: Any
    ) -> _ab_model.ListAssetCollectionsResponse:
        return self._run(self._client.list_collections(**kwargs))

    def get_collection(self, **kwargs: Any) -> _ab_model.AssetCollection:
        return self._run(self._client.get_collection(**kwargs))

    def ensure_collection(self, **kwargs: Any) -> _ab_model.AssetCollection:
        return self._run(self._client.ensure_collection(**kwargs))

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

    def export_entry(self, **kwargs: Any) -> ExportedAsset:
        return self._run(self._client.export_entry(**kwargs))

    def export_entry_to_path(self, **kwargs: Any) -> SavedExportedAsset:
        return self._run(self._client.export_entry_to_path(**kwargs))


__all__ = [
    "AssetBrowserClient",
    "AssetBrowserError",
    "ExportedAsset",
    "SavedExportedAsset",
    "SyncAssetBrowserClient",
]

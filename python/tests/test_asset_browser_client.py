import asyncio
import os
import tempfile

import pytest
from google.api import httpbody_pb2
from google.protobuf.any_pb2 import Any as AnyMessage

from stew import (
    AssetBrowserClient,
    AssetBrowserError,
    ExportedAsset,
    SavedExportedAsset,
    SyncAssetBrowserClient,
)
from stew.api.v1 import business_asset_browser_model as ab_model
from stew.api.v1 import business_asset_browser_pb2 as ab_pb
from stew.api.v1 import file_storage_pb2 as fs_pb


def test_asset_browser_client_is_exported() -> None:
    assert AssetBrowserClient is not None
    assert SyncAssetBrowserClient is not None
    assert AssetBrowserError is not None
    assert ExportedAsset is not None
    assert SavedExportedAsset is not None


def test_client_raises_when_not_connected() -> None:
    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    with pytest.raises(RuntimeError, match="not connected"):
        _ = client._s


def test_list_collections() -> None:
    collection_pb = ab_pb.AssetCollection(
        asset_space="configs",
        asset_id="my-app",
        display_name="My App",
        has_draft=True,
        total_versions=3,
    )
    response_pb = ab_pb.ListAssetCollectionsResponse(
        collections=[collection_pb],
        next_page_token="tok-2",
        total_count=1,
    )

    class Stub:
        async def ListAssetCollections(self, request, metadata, timeout):
            assert request.asset_space == "configs"
            assert request.page_size == 10
            assert timeout == 30.0
            return response_pb

    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.list_collections(asset_space="configs", page_size=10)
    )
    assert isinstance(result, ab_model.ListAssetCollectionsResponse)
    assert result.total_count == 1
    assert len(result.collections) == 1
    assert result.collections[0].asset_space == "configs"
    assert result.collections[0].asset_id == "my-app"
    assert result.collections[0].has_draft is True
    assert result.next_page_token == "tok-2"


def test_get_collection() -> None:
    collection_pb = ab_pb.AssetCollection(
        asset_space="docs",
        asset_id="readme",
        display_name="README",
        active_version_id="v20260401",
        total_versions=1,
    )

    class Stub:
        async def GetAssetCollection(self, request, metadata, timeout):
            assert request.asset_space == "docs"
            assert request.asset_id == "readme"
            return collection_pb

    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.get_collection(asset_space="docs", asset_id="readme")
    )
    assert isinstance(result, ab_model.AssetCollection)
    assert result.display_name == "README"
    assert result.active_version_id == "v20260401"


def test_list_versions_uses_business_version_ids() -> None:
    response_pb = ab_pb.ListAssetVersionsResponse(
        collection=ab_pb.AssetCollection(
            asset_space="configs",
            asset_id="my-app",
            active_version_id="v2",
            draft_version_id="draft-001",
        ),
        versions=[
            ab_pb.AssetVersionSummary(
                asset_space="configs",
                asset_id="my-app",
                version_id="v2",
                status=ab_pb.ASSET_VERSION_STATUS_READY,
                is_active=True,
                base_version_id="v1",
            ),
            ab_pb.AssetVersionSummary(
                asset_space="configs",
                asset_id="my-app",
                version_id="draft-001",
                status=ab_pb.ASSET_VERSION_STATUS_DRAFT,
                is_draft=True,
                base_version_id="v2",
            ),
        ],
        active_version_id="v2",
        draft_version_id="draft-001",
    )

    class Stub:
        async def ListAssetVersions(self, request, metadata, timeout):
            assert request.asset_space == "configs"
            assert request.asset_id == "my-app"
            return response_pb

    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.list_versions(asset_space="configs", asset_id="my-app")
    )
    assert isinstance(result, ab_model.ListAssetVersionsResponse)
    assert result.active_version_id == "v2"
    assert result.draft_version_id == "draft-001"
    assert result.collection.active_version_id == "v2"
    assert result.versions[0].version_id == "v2"
    assert result.versions[0].base_version_id == "v1"
    assert result.versions[1].version_id == "draft-001"
    assert result.versions[1].base_version_id == "v2"


def test_create_draft() -> None:
    draft_pb = ab_pb.AssetVersionSummary(
        asset_space="configs",
        asset_id="my-app",
        version_id="draft-001",
        status=ab_pb.ASSET_VERSION_STATUS_DRAFT,
        is_draft=True,
    )
    response_pb = ab_pb.CreateDraftVersionResponse(
        collection=ab_pb.AssetCollection(
            asset_space="configs",
            asset_id="my-app",
        ),
        draft_version=draft_pb,
    )

    class Stub:
        async def CreateDraftVersion(self, request, metadata, timeout):
            assert request.asset_space == "configs"
            assert request.asset_id == "my-app"
            assert request.description == "test draft"
            return response_pb

    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.create_draft(
            asset_space="configs",
            asset_id="my-app",
            description="test draft",
        )
    )
    assert isinstance(result, ab_model.CreateDraftVersionResponse)
    assert result.draft_version.version_id == "draft-001"
    assert result.draft_version.is_draft is True


def test_get_entry_text() -> None:
    response_pb = ab_pb.GetAssetEntryTextResponse(
        version_id="v1",
        text="hello world",
        content_type="text/plain",
        checksum="abc123",
        size_bytes=11,
        entry_revision=1,
        truncated=False,
        lossy=False,
        language_hint="plaintext",
    )

    class Stub:
        async def GetAssetEntryText(self, request, metadata, timeout):
            assert request.asset_space == "docs"
            assert request.path == "/readme.md"
            return response_pb

    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.get_entry_text(
            asset_space="docs",
            asset_id="readme",
            version_id="v1",
            path="/readme.md",
        )
    )
    assert isinstance(result, ab_model.GetAssetEntryTextResponse)
    assert result.text == "hello world"
    assert result.entry_revision == 1


def test_update_draft_text() -> None:
    response_pb = ab_pb.UpdateDraftTextEntryResponse(
        draft_version_id="draft-001",
        file_id="file-xyz",
        checksum="new-hash",
        size_bytes=20,
        entry_revision=2,
    )

    class Stub:
        async def UpdateDraftTextEntry(self, request, metadata, timeout):
            assert request.draft_version_id == "draft-001"
            assert request.path == "/config.yaml"
            assert request.text == "key: value"
            assert request.expected_entry_revision == 1
            return response_pb

    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.update_draft_text(
            asset_space="configs",
            asset_id="my-app",
            draft_version_id="draft-001",
            path="/config.yaml",
            text="key: value",
            expected_entry_revision=1,
        )
    )
    assert isinstance(result, ab_model.UpdateDraftTextEntryResponse)
    assert result.entry_revision == 2
    assert result.file_id == "file-xyz"


def test_discard_draft() -> None:
    from google.protobuf.empty_pb2 import Empty

    class Stub:
        async def DiscardDraftVersion(self, request, metadata, timeout):
            assert request.draft_version_id == "draft-001"
            return Empty()

    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.discard_draft(
            asset_space="configs",
            asset_id="my-app",
            draft_version_id="draft-001",
        )
    )
    assert result is None


def test_diff_versions() -> None:
    response_pb = ab_pb.DiffAssetVersionsResponse(
        collection=ab_pb.AssetCollection(
            asset_space="configs",
            asset_id="my-app",
        ),
        summary=ab_pb.AssetDiffSummary(
            total_changes=2,
            added_count=1,
            modified_count=1,
        ),
        entries=[
            ab_pb.AssetDiffEntry(
                path="/new-file.txt",
                change_type=ab_pb.ASSET_CHANGE_TYPE_ADDED,
            ),
            ab_pb.AssetDiffEntry(
                path="/config.yaml",
                change_type=ab_pb.ASSET_CHANGE_TYPE_MODIFIED,
                diff_detail_available=True,
            ),
        ],
        total_count=2,
    )

    class Stub:
        async def DiffAssetVersions(self, request, metadata, timeout):
            assert request.left_version_id == "v1"
            assert request.right_version_id == "v2"
            return response_pb

    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.diff_versions(
            asset_space="configs",
            asset_id="my-app",
            left_version_id="v1",
            right_version_id="v2",
        )
    )
    assert isinstance(result, ab_model.DiffAssetVersionsResponse)
    assert result.summary.total_changes == 2
    assert len(result.entries) == 2
    assert result.entries[1].diff_detail_available is True


def test_publish_draft() -> None:
    response_pb = ab_pb.PublishDraftVersionResponse(
        collection=ab_pb.AssetCollection(
            asset_space="configs",
            asset_id="my-app",
        ),
        published_version=ab_pb.AssetVersionSummary(
            version_id="v2",
            status=ab_pb.ASSET_VERSION_STATUS_READY,
        ),
        active_version_id="v2",
    )

    class Stub:
        async def PublishDraftVersion(self, request, metadata, timeout):
            assert request.draft_version_id == "draft-001"
            assert request.description == "Release v2"
            return response_pb

    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.publish_draft(
            asset_space="configs",
            asset_id="my-app",
            draft_version_id="draft-001",
            description="Release v2",
        )
    )
    assert isinstance(result, ab_model.PublishDraftVersionResponse)
    assert result.published_version.version_id == "v2"
    assert result.active_version_id == "v2"


def test_activate_version() -> None:
    response_pb = ab_pb.ActivateAssetVersionResponse(
        collection=ab_pb.AssetCollection(
            asset_space="configs",
            asset_id="my-app",
        ),
        active_version_id="v1",
        active_version=ab_pb.AssetVersionSummary(
            version_id="v1",
            is_active=True,
        ),
    )

    class Stub:
        async def ActivateAssetVersion(self, request, metadata, timeout):
            assert request.target_version_id == "v1"
            return response_pb

    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.activate_version(
            asset_space="configs",
            asset_id="my-app",
            target_version_id="v1",
        )
    )
    assert isinstance(result, ab_model.ActivateAssetVersionResponse)
    assert result.active_version_id == "v1"
    assert result.active_version.is_active is True


def test_export_entry() -> None:
    metadata_pb = fs_pb.DownloadFileHttpMetadata(
        filename="templates.zip",
        content_disposition='attachment; filename="templates.zip"',
        etag='"zip-etag"',
    )
    extension = AnyMessage()
    extension.Pack(metadata_pb)
    response_pb = httpbody_pb2.HttpBody(
        content_type="application/zip",
        data=b"zip-bytes",
        extensions=[extension],
    )

    class Stub:
        async def ExportAssetEntry(self, request, metadata, timeout):
            assert request.asset_space == "configs"
            assert request.asset_id == "my-app"
            assert request.version_id == "v1"
            assert request.path == "/templates"
            return response_pb

    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.export_entry(
            asset_space="configs",
            asset_id="my-app",
            version_id="v1",
            path="/templates",
        )
    )
    assert isinstance(result, ExportedAsset)
    assert result.data == b"zip-bytes"
    assert result.content_type == "application/zip"
    assert result.filename == "templates.zip"
    assert result.etag == '"zip-etag"'


def test_export_entry_to_path() -> None:
    response_pb = httpbody_pb2.HttpBody(
        content_type="text/plain",
        data=b"hello export",
    )

    class Stub:
        async def ExportAssetEntry(self, request, metadata, timeout):
            return response_pb

    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_test")
    client._stub = Stub()  # type: ignore[assignment]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "exported.txt")
        result = asyncio.run(
            client.export_entry_to_path(
                asset_space="configs",
                asset_id="my-app",
                version_id="v1",
                path="/hello.txt",
                output_path=output_path,
            )
        )

        assert isinstance(result, SavedExportedAsset)
        assert result.path == output_path
        assert result.bytes_written == len(b"hello export")
        with open(output_path, "rb") as fh:
            assert fh.read() == b"hello export"


def test_metadata_includes_api_key() -> None:
    client = AssetBrowserClient("127.0.0.1:3012", app_secret="ak_secret")
    meta = client._meta()
    assert ("x-api-key", "ak_secret") in meta


def test_sync_client_delegates() -> None:
    collection_pb = ab_pb.AssetCollection(
        asset_space="configs",
        asset_id="my-app",
        display_name="My App",
    )

    class Stub:
        async def GetAssetCollection(self, request, metadata, timeout):
            return collection_pb

    sync_client = SyncAssetBrowserClient(
        "127.0.0.1:3012", app_secret="ak_test"
    )
    sync_client._client._stub = Stub()  # type: ignore[assignment]

    result = sync_client.get_collection(
        asset_space="configs", asset_id="my-app"
    )
    assert isinstance(result, ab_model.AssetCollection)
    assert result.display_name == "My App"
    sync_client._loop.close()


def test_sync_client_export_entry_delegates() -> None:
    response_pb = httpbody_pb2.HttpBody(
        content_type="application/zip",
        data=b"sync-export",
    )

    class Stub:
        async def ExportAssetEntry(self, request, metadata, timeout):
            return response_pb

    sync_client = SyncAssetBrowserClient(
        "127.0.0.1:3012", app_secret="ak_test"
    )
    sync_client._client._stub = Stub()  # type: ignore[assignment]

    result = sync_client.export_entry(
        asset_space="configs",
        asset_id="my-app",
        version_id="v1",
        path="/templates",
    )
    assert isinstance(result, ExportedAsset)
    assert result.data == b"sync-export"
    sync_client._loop.close()

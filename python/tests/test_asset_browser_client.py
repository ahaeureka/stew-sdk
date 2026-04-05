import asyncio

import pytest

from stew import (
    AssetBrowserClient,
    AssetBrowserError,
    SyncAssetBrowserClient,
)
from stew.api.v1 import business_asset_browser_model as ab_model
from stew.api.v1 import business_asset_browser_pb2 as ab_pb


def test_asset_browser_client_is_exported() -> None:
    assert AssetBrowserClient is not None
    assert SyncAssetBrowserClient is not None
    assert AssetBrowserError is not None


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

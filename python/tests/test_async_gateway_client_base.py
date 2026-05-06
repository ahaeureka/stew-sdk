import asyncio

import pytest

from stew.asset_browser_client import AssetBrowserClient
from stew.file_storage_client import FileStorageClient
from stew._discovery.client import DiscoveryClient


@pytest.mark.parametrize(
    ("client_factory", "stub_target"),
    [
        (
            lambda: DiscoveryClient("127.0.0.1:3012", app_secret="ak_shared", timeout=5.0),
            "stew._discovery.client._grpc.ServiceDiscoveryServiceStub",
        ),
        (
            lambda: FileStorageClient("127.0.0.1:3012", app_secret="ak_shared", timeout=5.0),
            "stew.file_storage_client._fs_grpc.FileStorageServiceStub",
        ),
        (
            lambda: AssetBrowserClient("127.0.0.1:3012", app_secret="ak_shared", timeout=5.0),
            "stew.asset_browser_client._ab_grpc.BusinessAssetBrowserServiceStub",
        ),
    ],
)
def test_async_gateway_clients_share_channel_and_metadata(
    monkeypatch: pytest.MonkeyPatch,
    client_factory,
    stub_target: str,
) -> None:
    captured: dict[str, object] = {}

    class FakeChannel:
        def __init__(self) -> None:
            self.closed = False

        async def close(self) -> None:
            self.closed = True

    class Stub:
        def __init__(self, channel) -> None:
            captured["channel"] = channel

    fake_channel = FakeChannel()
    monkeypatch.setattr(
        "stew._discovery.helpers.grpc.aio.insecure_channel",
        lambda addr: fake_channel,
    )
    monkeypatch.setattr(stub_target, Stub)

    async def run() -> None:
        client = client_factory()
        await client.connect()

        assert captured["channel"] is fake_channel
        assert client._meta(extra_metadata=[("x-request-id", "req-1")]) == [
            ("x-api-key", "ak_shared"),
            ("x-request-id", "req-1"),
        ]

        await client.close()

    asyncio.run(run())

    assert fake_channel.closed is True
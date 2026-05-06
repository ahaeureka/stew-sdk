import asyncio

import pytest

from stew.asset_browser_client import SyncAssetBrowserClient
from stew.file_storage_client import SyncFileStorageClient
from stew._discovery.client import SyncDiscoveryClient


@pytest.mark.parametrize(
    ("sync_client_factory", "client_target"),
    [
        (
            lambda: SyncDiscoveryClient("127.0.0.1:3012", app_secret="ak_sync"),
            "stew._discovery.client.DiscoveryClient",
        ),
        (
            lambda: SyncFileStorageClient("127.0.0.1:3012", app_secret="ak_sync"),
            "stew.file_storage_client.FileStorageClient",
        ),
        (
            lambda: SyncAssetBrowserClient("127.0.0.1:3012", app_secret="ak_sync"),
            "stew.asset_browser_client.AssetBrowserClient",
        ),
    ],
)
def test_sync_gateway_clients_share_lifecycle_wrapper(
    monkeypatch: pytest.MonkeyPatch,
    sync_client_factory,
    client_target: str,
) -> None:
    events: list[str] = []

    class AsyncClient:
        def __init__(self, *args, **kwargs) -> None:
            self.args = args
            self.kwargs = kwargs

        async def connect(self) -> None:
            events.append("connect")

        async def close(self) -> None:
            events.append("close")

        async def ping(self) -> str:
            events.append("ping")
            return "pong"

    monkeypatch.setattr(client_target, AsyncClient)

    client = sync_client_factory()
    assert isinstance(client._loop, asyncio.AbstractEventLoop)
    assert client._run(client._client.ping()) == "pong"
    assert events == ["ping"]

    with client as entered:
        assert entered is client
        assert isinstance(client._client, AsyncClient)

    assert events == ["ping", "connect", "close"]
    assert client._loop.is_closed() is True
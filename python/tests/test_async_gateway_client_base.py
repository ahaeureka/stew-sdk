import asyncio

import pytest

from stew.entitlement_client import EntitlementClient
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
        (
            lambda: EntitlementClient("127.0.0.1:3012", app_secret="ak_shared", timeout=5.0),
            "stew.entitlement_client._ent_grpc.EntitlementServiceStub",
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

    def fake_insecure_channel(addr, **kwargs):
        captured["addr"] = addr
        captured["interceptors"] = kwargs.get("interceptors")
        return fake_channel

    fake_channel = FakeChannel()
    monkeypatch.setattr(
        "stew._discovery.helpers.grpc.aio.insecure_channel",
        fake_insecure_channel,
    )
    monkeypatch.setattr(stub_target, Stub)

    async def run() -> None:
        client = client_factory()
        await client.connect()

        assert captured["channel"] is fake_channel
        assert captured["interceptors"]
        assert client._meta(extra_metadata=[("x-request-id", "req-1")]) == [
            ("x-request-id", "req-1"),
        ]

        await client.close()

    asyncio.run(run())

    assert fake_channel.closed is True


def test_async_gateway_client_base_supports_default_metadata_and_business_id() -> None:
    client = FileStorageClient(
        "127.0.0.1:3012",
        app_secret="ak_shared",
        business_id="biz-default",
        default_metadata=[("x-sdk-source", "python")],
        timeout=5.0,
    )

    assert dict(
        client._meta(
            extra_metadata=[("x-request-id", "req-1"), ("x-business-id", "biz-override")]
        )
    ) == {
        "x-api-key": "ak_shared",
        "x-business-id": "biz-override",
        "x-sdk-source": "python",
        "x-request-id": "req-1",
    }
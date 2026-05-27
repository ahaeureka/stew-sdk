import asyncio

import grpc
import pytest

from stew.billing_internal_client import BillingInternalClient
from stew.billing_public_client import BillingPublicClient
from stew.entitlement_client import EntitlementClient
from stew.asset_browser_client import AssetBrowserClient
from stew.file_storage_client import FileStorageClient
from stew.payment_client import PaymentClient
from stew._discovery.client import DiscoveryClient
from stew._discovery.helpers import (
    AioGrpcMetadataClientInterceptor,
    build_aio_metadata_client_interceptors,
    create_aio_channel,
)


@pytest.mark.parametrize(
    ("client_factory", "stub_target"),
    [
        (
            lambda: DiscoveryClient(
                "127.0.0.1:3012", app_secret="ak_shared", timeout=5.0
            ),
            "stew._discovery.client._grpc.ServiceDiscoveryServiceStub",
        ),
        (
            lambda: FileStorageClient(
                "127.0.0.1:3012", app_secret="ak_shared", timeout=5.0
            ),
            "stew.file_storage_client._fs_grpc.FileStorageServiceStub",
        ),
        (
            lambda: AssetBrowserClient(
                "127.0.0.1:3012", app_secret="ak_shared", timeout=5.0
            ),
            "stew.asset_browser_client._ab_grpc.BusinessAssetBrowserServiceStub",
        ),
        (
            lambda: EntitlementClient(
                "127.0.0.1:3012", app_secret="ak_shared", timeout=5.0
            ),
            "stew.entitlement_client._ent_grpc.EntitlementServiceStub",
        ),
        (
            lambda: BillingPublicClient(
                "127.0.0.1:3012", app_secret="ak_shared", timeout=5.0
            ),
            "stew.billing_public_client._bill_public_grpc.BillingPublicServiceStub",
        ),
        (
            lambda: BillingInternalClient(
                "127.0.0.1:3012", app_secret="ak_shared", timeout=5.0
            ),
            "stew.billing_internal_client._bill_internal_grpc.BillingInternalServiceStub",
        ),
        (
            lambda: PaymentClient(
                "127.0.0.1:3012", app_secret="ak_shared", timeout=5.0
            ),
            "stew.payment_client._payment_grpc.PaymentGatewayServiceStub",
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

        def unary_unary(self, *args, **kwargs):
            return object()

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
        assert len(captured["interceptors"]) == 4
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
            extra_metadata=[
                ("x-request-id", "req-1"),
                ("x-business-id", "biz-override"),
            ]
        )
    ) == {
        "x-api-key": "ak_shared",
        "x-business-id": "biz-override",
        "x-sdk-source": "python",
        "x-request-id": "req-1",
    }


def test_build_aio_metadata_client_interceptors_cover_all_rpc_arities() -> None:
    interceptors = build_aio_metadata_client_interceptors(
        app_secret="ak_shared",
        business_id="biz-default",
        default_metadata=[("x-sdk-source", "python")],
    )

    assert len(interceptors) == 4
    assert (
        sum(isinstance(it, grpc.aio.UnaryUnaryClientInterceptor) for it in interceptors)
        == 1
    )
    assert (
        sum(
            isinstance(it, grpc.aio.UnaryStreamClientInterceptor) for it in interceptors
        )
        == 1
    )
    assert (
        sum(
            isinstance(it, grpc.aio.StreamUnaryClientInterceptor) for it in interceptors
        )
        == 1
    )
    assert (
        sum(
            isinstance(it, grpc.aio.StreamStreamClientInterceptor)
            for it in interceptors
        )
        == 1
    )

    async def run() -> None:
        captured: dict[str, object] = {}
        stream_unary = next(
            it
            for it in interceptors
            if isinstance(it, grpc.aio.StreamUnaryClientInterceptor)
        )
        call_details = grpc.aio.ClientCallDetails(
            method="/stew.api.v1.FileStorageService/UploadFile",
            timeout=5.0,
            metadata=[("x-request-id", "req-1")],
            credentials=None,
            wait_for_ready=None,
        )

        async def continuation(next_call_details, request_iterator):
            captured["metadata"] = list(next_call_details.metadata)
            captured["request_iterator"] = request_iterator
            return "ok"

        request_iterator = iter((b"chunk",))
        result = await stream_unary.intercept_stream_unary(
            continuation,
            call_details,
            request_iterator,
        )

        assert result == "ok"
        assert captured["request_iterator"] is request_iterator
        assert dict(captured["metadata"]) == {
            "x-api-key": "ak_shared",
            "x-sdk-source": "python",
            "x-business-id": "biz-default",
            "x-request-id": "req-1",
        }

    asyncio.run(run())


def test_create_aio_channel_expands_legacy_metadata_interceptor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_insecure_channel(addr, **kwargs):
        captured["addr"] = addr
        captured["interceptors"] = kwargs.get("interceptors")
        return object()

    monkeypatch.setattr(
        "stew._discovery.helpers.grpc.aio.insecure_channel",
        fake_insecure_channel,
    )

    create_aio_channel(
        "127.0.0.1:3012",
        interceptors=[
            AioGrpcMetadataClientInterceptor(
                app_secret="ak_shared",
                business_id="biz-default",
                default_metadata=[("x-sdk-source", "python")],
            )
        ],
    )

    expanded = captured["interceptors"]
    assert len(expanded) == 4
    assert (
        sum(isinstance(it, grpc.aio.UnaryUnaryClientInterceptor) for it in expanded)
        == 1
    )
    assert (
        sum(isinstance(it, grpc.aio.UnaryStreamClientInterceptor) for it in expanded)
        == 1
    )
    assert (
        sum(isinstance(it, grpc.aio.StreamUnaryClientInterceptor) for it in expanded)
        == 1
    )
    assert (
        sum(isinstance(it, grpc.aio.StreamStreamClientInterceptor) for it in expanded)
        == 1
    )

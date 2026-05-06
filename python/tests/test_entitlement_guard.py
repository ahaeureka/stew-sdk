import asyncio
from typing import Any, cast

import pytest

from stew._discovery import grpc_context_passthrough
from stew._discovery import helpers as _discovery_helpers
from stew.api.v1 import entitlement_pb2 as entitlement_pb2
from stew.entitlement_guard import EntitlementGuard


_with_service_auth = cast(Any, getattr(_discovery_helpers, "with_service_auth"))


def test_entitlement_guard_injects_app_secret_metadata() -> None:
    captured: dict[str, object] = {}

    class FakeContext:
        def invocation_metadata(self):
            return [
                ("x-user-id", "user-1"),
                ("x-request-id", "req-1"),
                ("x-api-key", "inbound-secret"),
            ]

    class Stub:
        async def CheckFeature(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            captured["timeout"] = timeout
            return entitlement_pb2.CheckFeatureResponse(enabled=True)

    guard = cast(Any, EntitlementGuard)(
        Stub(),  # type: ignore[arg-type]
        business_id="skillforge",
        app_secret="ak_guard",
        timeout=5.0,
    )

    with grpc_context_passthrough(FakeContext()):
        asyncio.run(
            guard.require_feature(cast(Any, FakeContext()), "extraction.mode.standard")
        )

    request = cast(entitlement_pb2.CheckFeatureRequest, captured["request"])
    assert request.business_id == "skillforge"
    assert request.subject_id == "user-1"
    assert request.feature_key == "extraction.mode.standard"
    assert captured["timeout"] == 5.0
    assert captured["metadata"] == [
        ("x-user-id", "user-1"),
        ("x-request-id", "req-1"),
        ("x-api-key", "ak_guard"),
    ]


def test_entitlement_guard_uses_app_secret_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}
    monkeypatch.setenv("APP_SECRET", "ak_from_env")

    class Stub:
        async def CheckQuota(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            captured["timeout"] = timeout
            return entitlement_pb2.CheckQuotaResponse(used=1, limit=10)

    guard = EntitlementGuard(
        Stub(),  # type: ignore[arg-type]
        business_id="skillforge",
        timeout=2.5,
    )

    allowed, used, limit = asyncio.run(
        guard.check_quota("user-2", "credits.monthly", requested=3)
    )

    request = cast(entitlement_pb2.CheckQuotaRequest, captured["request"])
    assert request.business_id == "skillforge"
    assert request.subject_id == "user-2"
    assert request.quota_key == "credits.monthly"
    assert captured["timeout"] == 2.5
    assert captured["metadata"] == [("x-api-key", "ak_from_env")]
    assert allowed is True
    assert used == 1
    assert limit == 10


def test_with_service_auth_wraps_bare_stub_and_injects_metadata() -> None:
    captured: dict[str, object] = {}

    class FakeContext:
        def invocation_metadata(self):
            return [
                ("authorization", "Bearer token-123"),
                ("x-user-id", "user-9"),
                ("x-api-key", "inbound-secret"),
            ]

    class Stub:
        async def CheckFeature(self, request, metadata, timeout):
            captured["metadata"] = list(metadata)
            return entitlement_pb2.CheckFeatureResponse(enabled=True)

    stub = _with_service_auth(Stub(), app_secret="ak_proxy")

    with grpc_context_passthrough(FakeContext()):
        asyncio.run(
            stub.CheckFeature(
                entitlement_pb2.CheckFeatureRequest(
                    business_id="skillforge",
                    subject_id="user-9",
                    feature_key="extraction.mode.standard",
                ),
                timeout=3.0,
            )
        )

    assert captured["metadata"] == [
        ("authorization", "Bearer token-123"),
        ("x-user-id", "user-9"),
        ("x-api-key", "ak_proxy"),
    ]


def test_entitlement_guard_connect_creates_owned_channel(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class FakeChannel:
        def __init__(self) -> None:
            self.closed = False

        async def close(self) -> None:
            self.closed = True

    class Stub:
        def __init__(self, channel) -> None:
            captured["channel"] = channel

        async def CheckFeature(self, request, metadata, timeout):
            captured["metadata"] = list(metadata)
            return entitlement_pb2.CheckFeatureResponse(enabled=True)

    channel = FakeChannel()
    monkeypatch.setattr(
        "stew.entitlement_guard._create_aio_channel",
        lambda addr, use_tls=False: channel,
    )
    monkeypatch.setattr(
        "stew.entitlement_guard.entitlement_pb2_grpc.EntitlementServiceStub",
        Stub,
    )

    async def run() -> None:
        async with cast(Any, EntitlementGuard).connect(
            "127.0.0.1:3012",
            "skillforge",
            app_secret="ak_connect",
            timeout=2.0,
        ) as guard:
            await guard.check_feature("user-3", "extraction.mode.standard")

    asyncio.run(run())

    assert captured["channel"] is channel
    assert captured["metadata"] == [("x-api-key", "ak_connect")]
    assert channel.closed is True
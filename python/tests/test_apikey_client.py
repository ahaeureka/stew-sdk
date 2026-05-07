import asyncio

from stew import ApiKeyClient, ApiKeyError, SyncApiKeyClient
from stew.api.v1 import apikey_model as apikey_model
from stew.api.v1 import apikey_pb2 as apikey_pb2


def test_apikey_client_is_exported() -> None:
    assert ApiKeyClient is not None
    assert SyncApiKeyClient is not None
    assert ApiKeyError is not None


def test_create_api_key_injects_required_business_header() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def CreateApiKey(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            assert timeout == 30.0
            return apikey_pb2.CreateApiKeyResponse(
                api_key=apikey_pb2.ApiKey(
                    id="key-1",
                    name=request.name,
                    user_id=request.user_id,
                ),
                raw_key="raw-secret",
            )

    client = ApiKeyClient("127.0.0.1:3012", app_secret="ak_admin")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.create_api_key(
            name="demo",
            user_id="user-1",
            scopes=["read"],
            business_id="biz-123",
            extra_metadata=[("x-request-id", "req-1")],
        )
    )

    request = captured["request"]
    assert request.name == "demo"
    assert request.user_id == "user-1"
    assert captured["metadata"] == [
        ("x-api-key", "ak_admin"),
        ("x-business-id", "biz-123"),
        ("x-request-id", "req-1"),
    ]
    assert isinstance(result, apikey_model.CreateApiKeyResponse)
    assert result.raw_key == "raw-secret"
    assert result.api_key is not None
    assert result.api_key.id == "key-1"


def test_validate_api_key_accepts_optional_scope_header() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def ValidateApiKey(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            return apikey_pb2.ValidateApiKeyResponse(is_valid=True)

    client = ApiKeyClient("127.0.0.1:3012", app_secret="ak_admin")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.validate_api_key(
            api_key="sk_live_xxx",
            required_scopes=["apikey:read"],
            business_id="biz-optional",
        )
    )

    assert captured["request"].api_key == "sk_live_xxx"
    assert captured["metadata"] == [
        ("x-api-key", "ak_admin"),
        ("x-business-id", "biz-optional"),
    ]
    assert isinstance(result, apikey_model.ValidateApiKeyResponse)
    assert result.is_valid is True
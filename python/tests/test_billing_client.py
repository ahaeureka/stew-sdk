import asyncio

from stew import BillingClient, BillingError, SyncBillingClient
from stew.api.v1 import billing_model as billing_model
from stew.api.v1 import billing_pb2 as billing_pb2


def test_billing_client_is_exported() -> None:
    assert BillingClient is not None
    assert SyncBillingClient is not None
    assert BillingError is not None


def test_query_balance_separates_scope_business_id_from_header_business_id() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def QueryBalance(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            assert timeout == 30.0
            return billing_pb2.BalanceSnapshot(
                business_id=request.business_id,
                subject_id=request.subject_id,
                user_id=request.user_id,
                available_balance=42,
            )

    client = BillingClient(
        "127.0.0.1:3012",
        app_secret="ak_bill",
        business_id="biz-default",
        default_metadata=[("x-sdk-source", "python")],
    )
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.query_balance(
            scope_business_id="ledger-biz",
            subject_id="subject-1",
            user_id="user-1",
            business_id="biz-override",
            extra_metadata=[("x-request-id", "req-1")],
        )
    )

    request = captured["request"]
    assert request.business_id == "ledger-biz"
    assert captured["metadata"] == [
        ("x-api-key", "ak_bill"),
        ("x-sdk-source", "python"),
        ("x-business-id", "biz-override"),
        ("x-request-id", "req-1"),
    ]
    assert isinstance(result, billing_model.BalanceSnapshot)
    assert result.business_id == "ledger-biz"
    assert result.available_balance == 42


def test_finalize_accepts_model_inputs() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def Finalize(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            assert timeout == 30.0
            return billing_pb2.SettlementDecision(
                success=True,
                points=128,
                message="captured",
            )

    client = BillingClient("127.0.0.1:3012", app_secret="ak_bill")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.finalize(
            context=billing_model.AuthorizationContext(
                business_id="ledger-biz",
                subject_id="subject-1",
                request_id="req-2",
            ),
            report=billing_model.BillingReport(
                business_id="ledger-biz",
                authorization_id="auth-1",
                request_id="req-2",
                billed_points_candidate=128,
            ),
        )
    )

    request = captured["request"]
    assert request.context.business_id == "ledger-biz"
    assert request.report.authorization_id == "auth-1"
    assert captured["metadata"] == [("x-api-key", "ak_bill")]
    assert isinstance(result, billing_model.SettlementDecision)
    assert result.success is True
    assert result.points == 128


def test_create_policy_artifact_supports_scope_and_metadata() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def CreatePolicyArtifact(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            assert timeout == 30.0
            return billing_pb2.BillingPolicyArtifact(
                artifact_id="artifact-1",
                business_id=request.business_id,
                artifact_version=request.artifact_version,
            )

    client = BillingClient("127.0.0.1:3012", app_secret="ak_bill")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.create_policy_artifact(
            scope_business_id="ledger-biz",
            artifact_version="v1",
            policy_id="policy-1",
            content={"tier": "gold"},
            business_id="header-biz",
        )
    )

    assert captured["request"].business_id == "ledger-biz"
    assert captured["metadata"] == [
        ("x-api-key", "ak_bill"),
        ("x-business-id", "header-biz"),
    ]
    assert isinstance(result, billing_model.BillingPolicyArtifact)
    assert result.artifact_id == "artifact-1"


def test_list_policy_bundles_returns_model_response() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def ListPolicyBundles(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            return billing_pb2.ListBillingPolicyBundlesResponse(
                bundles=[
                    billing_pb2.BillingPolicyBundle(
                        policy_id=request.policy_id,
                        business_id=request.business_id,
                        bundle_version=3,
                    )
                ]
            )

    client = BillingClient("127.0.0.1:3012", app_secret="ak_bill")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.list_policy_bundles(
            scope_business_id="ledger-biz",
            policy_id="policy-1",
            active_only=True,
        )
    )

    assert captured["request"].business_id == "ledger-biz"
    assert captured["request"].active_only is True
    assert captured["metadata"] == [("x-api-key", "ak_bill")]
    assert isinstance(result, billing_model.ListBillingPolicyBundlesResponse)
    assert result.bundles is not None
    assert result.bundles[0].bundle_version == 3
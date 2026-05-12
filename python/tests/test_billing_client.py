import asyncio

from google.protobuf import empty_pb2

from stew import (
    BillingAdminClient,
    BillingClient,
    BillingError,
    BillingInternalClient,
    BillingPublicClient,
    SyncBillingAdminClient,
    SyncBillingClient,
    SyncBillingInternalClient,
    SyncBillingPublicClient,
)
from stew.api.v1 import billing_common_model as billing_model
from stew.api.v1 import billing_common_pb2 as billing_pb2


def test_billing_clients_are_exported() -> None:
    assert BillingClient is not None
    assert BillingPublicClient is not None
    assert BillingAdminClient is not None
    assert BillingInternalClient is not None
    assert SyncBillingClient is not None
    assert SyncBillingPublicClient is not None
    assert SyncBillingAdminClient is not None
    assert SyncBillingInternalClient is not None
    assert BillingError is not None


def test_public_query_balance_separates_scope_business_id_from_header_business_id() -> (
    None
):
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

    client = BillingPublicClient(
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


def test_internal_finalize_accepts_model_inputs() -> None:
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

    client = BillingInternalClient("127.0.0.1:3012", app_secret="ak_bill")
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


def test_admin_create_policy_supports_scope_and_metadata() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def CreatePolicy(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            assert timeout == 30.0
            return billing_pb2.BillingPolicy(
                policy_id="policy-1",
                business_id=request.business_id,
                display_name=request.display_name,
            )

    client = BillingAdminClient("127.0.0.1:3012", app_secret="ak_bill")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.create_policy(
            scope_business_id="ledger-biz",
            display_name="Gold Plan",
            description="premium",
            business_id="header-biz",
        )
    )

    assert captured["request"].business_id == "ledger-biz"
    assert captured["request"].display_name == "Gold Plan"
    assert captured["metadata"] == [
        ("x-api-key", "ak_bill"),
        ("x-business-id", "header-biz"),
    ]
    assert isinstance(result, billing_model.BillingPolicy)
    assert result.policy_id == "policy-1"


def test_admin_create_policy_artifact_supports_scope_and_metadata() -> None:
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

    client = BillingAdminClient("127.0.0.1:3012", app_secret="ak_bill")
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


def test_admin_list_policy_bundles_returns_model_response() -> None:
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

    client = BillingAdminClient("127.0.0.1:3012", app_secret="ak_bill")
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


def test_admin_query_reservations_supports_status_filter() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def QueryReservations(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            assert timeout == 30.0
            return billing_pb2.QueryBillingReservationsResponse(
                reservations=[
                    billing_pb2.BillingReservation(
                        business_id=request.business_id,
                        authorization_id=request.authorization_id,
                        status=request.status,
                    )
                ],
                next_page_token="next-page",
            )

    client = BillingAdminClient("127.0.0.1:3012", app_secret="ak_bill")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.query_reservations(
            scope_business_id="ledger-biz",
            authorization_id="auth-1",
            page_size=20,
            status=billing_model.BillingReservationStatus.BILLING_RESERVATION_STATUS_AWAITING_REPORT,
            business_id="header-biz",
        )
    )

    assert captured["request"].business_id == "ledger-biz"
    assert captured["request"].authorization_id == "auth-1"
    assert (
        captured["request"].status
        == billing_pb2.BILLING_RESERVATION_STATUS_AWAITING_REPORT
    )
    assert captured["metadata"] == [
        ("x-api-key", "ak_bill"),
        ("x-business-id", "header-biz"),
    ]
    assert isinstance(result, billing_model.QueryBillingReservationsResponse)
    assert result.reservations is not None
    assert result.reservations[0].status is not None
    assert result.next_page_token == "next-page"


def test_internal_submit_billing_report_uses_ingress_stub() -> None:
    captured: dict[str, object] = {}

    class IngressStub:
        async def SubmitBillingReport(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            assert timeout == 30.0
            return billing_pb2.SubmitBillingReportResponse(
                business_id=request.report.business_id,
                authorization_id=request.report.authorization_id,
                request_id=request.report.request_id,
                deduped=True,
                decision=billing_pb2.SettlementDecision(success=True, points=42),
            )

    client = BillingInternalClient("127.0.0.1:3012", app_secret="ak_bill")
    client._report_ingress_stub = IngressStub()  # type: ignore[assignment]

    result = asyncio.run(
        client.submit_billing_report(
            report=billing_model.BillingReport(
                business_id="ledger-biz",
                authorization_id="auth-1",
                request_id="req-1",
                user_id="user-1",
                final_status=billing_model.BillingFinalStatus.BILLING_FINAL_STATUS_SUCCESS,
                usage_source=billing_model.BillingUsageSource.BILLING_USAGE_SOURCE_ACTUAL,
                dedupe_key="job-42",
            ),
            delivery_request_id="delivery-1",
            source_service="your.service.v1.AsyncWorker",
            labels={"attempt": "1"},
            business_id="header-biz",
            extra_metadata=[("x-request-id", "req-1")],
        )
    )

    assert captured["request"].report.authorization_id == "auth-1"
    assert captured["request"].delivery_request_id == "delivery-1"
    assert captured["request"].source_service == "your.service.v1.AsyncWorker"
    assert captured["request"].labels["attempt"] == "1"
    assert captured["metadata"] == [
        ("x-api-key", "ak_bill"),
        ("x-business-id", "header-biz"),
        ("x-request-id", "req-1"),
    ]
    assert isinstance(result, billing_model.SubmitBillingReportResponse)
    assert result.deduped is True
    assert result.decision is not None
    assert result.decision.points == 42


def test_admin_delete_policy_returns_empty_response() -> None:
    class Stub:
        async def DeletePolicy(self, request, metadata, timeout):
            assert request.business_id == "ledger-biz"
            assert request.policy_id == "policy-1"
            assert list(metadata) == [("x-api-key", "ak_bill")]
            assert timeout == 30.0
            return empty_pb2.Empty()

    client = BillingAdminClient("127.0.0.1:3012", app_secret="ak_bill")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.delete_policy(
            scope_business_id="ledger-biz",
            policy_id="policy-1",
        )
    )

    assert isinstance(result, empty_pb2.Empty)


def test_compatibility_billing_client_routes_to_split_clients() -> None:
    client = BillingClient("127.0.0.1:3012", app_secret="ak_bill")
    calls: list[tuple[str, tuple[object, ...], dict[str, object]]] = []

    async def fake_query_balance(*args, **kwargs):
        calls.append(("public", args, kwargs))
        return billing_model.BalanceSnapshot(available_balance=9)

    async def fake_grant_credits(*args, **kwargs):
        calls.append(("admin", args, kwargs))
        return billing_model.CreditGrant(grant_id="grant-1")

    async def fake_finalize(*args, **kwargs):
        calls.append(("internal", args, kwargs))
        return billing_model.SettlementDecision(success=True)

    client.public.query_balance = fake_query_balance  # type: ignore[method-assign]
    client.admin.grant_credits = fake_grant_credits  # type: ignore[method-assign]
    client.internal.finalize = fake_finalize  # type: ignore[method-assign]

    balance = asyncio.run(client.query_balance(scope_business_id="ledger-biz"))
    grant = asyncio.run(client.grant_credits(scope_business_id="ledger-biz"))
    decision = asyncio.run(client.finalize())

    assert balance.available_balance == 9
    assert grant.grant_id == "grant-1"
    assert decision.success is True
    assert [entry[0] for entry in calls] == ["public", "admin", "internal"]

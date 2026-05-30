import asyncio
import logging

from stew import (
    BillingClient,
    BillingError,
    BillingInternalClient,
    BillingPublicClient,
    SyncBillingClient,
    SyncBillingInternalClient,
    SyncBillingPublicClient,
    build_submit_billing_report_metadata,
)
from stew.api.v1 import billing_common_model as billing_model
from stew.api.v1 import billing_common_pb2 as billing_pb2
from stew._discovery.errors import DiscoveryError


def test_billing_root_exports_business_surfaces_only() -> None:
    assert BillingClient is not None
    assert BillingPublicClient is not None
    assert BillingInternalClient is not None
    assert SyncBillingClient is not None
    assert SyncBillingPublicClient is not None
    assert SyncBillingInternalClient is not None
    assert BillingError is not None


def test_billing_admin_surfaces_are_not_root_exports() -> None:
    import stew
    import importlib
    import pytest

    assert not hasattr(stew, "BillingAdminClient")
    assert not hasattr(stew, "SyncBillingAdminClient")
    assert not hasattr(stew, "BillingReservationTroubleshooter")
    assert not hasattr(stew, "SyncBillingReservationTroubleshooter")

    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("stew.billing_admin_client")

    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("stew.billing_reservation_troubleshooting")


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

    assert captured["request"].business_id == "ledger-biz"
    assert captured["metadata"] == [
        ("x-api-key", "ak_bill"),
        ("x-sdk-source", "python"),
        ("x-business-id", "biz-override"),
        ("x-request-id", "req-1"),
    ]
    assert isinstance(result, billing_model.BalanceSnapshot)
    assert result.business_id == "ledger-biz"
    assert result.available_balance == 42


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


def test_build_submit_billing_report_metadata_sets_minimal_headers() -> None:
    metadata = build_submit_billing_report_metadata(
        service_id="skills-app",
        request_id="req-1",
        extra_metadata=[("x-request-id", "req-old"), ("x-extra", "ok")],
    )

    assert metadata == [
        ("x-request-id", "req-1"),
        ("x-extra", "ok"),
        ("x-stew-service-id", "skills-app"),
    ]


def test_submit_billing_report_warns_on_risky_identity_headers(caplog) -> None:
    captured: dict[str, object] = {}

    class IngressStub:
        async def SubmitBillingReport(self, request, metadata, timeout):
            captured["metadata"] = list(metadata)
            return billing_pb2.SubmitBillingReportResponse(
                business_id=request.report.business_id,
                authorization_id=request.report.authorization_id,
                request_id=request.report.request_id,
            )

    client = BillingInternalClient("127.0.0.1:3012", app_secret="ak_bill")
    client._report_ingress_stub = IngressStub()  # type: ignore[assignment]

    with caplog.at_level(logging.WARNING, logger="stew.billing_internal_client"):
        asyncio.run(
            client.submit_billing_report(
                report=billing_model.BillingReport(
                    business_id="ledger-biz",
                    authorization_id="auth-1",
                    request_id="req-1",
                    user_id="user-1",
                    final_status=billing_model.BillingFinalStatus.BILLING_FINAL_STATUS_SUCCESS,
                ),
                source_service="skills-app",
                extra_metadata=[("x-user-id", "user-1")],
            )
        )

    assert "not report-ingress auth inputs" in caplog.text
    assert captured["metadata"] == [
        ("x-api-key", "ak_bill"),
        ("x-user-id", "user-1"),
        ("x-request-id", "req-1"),
    ]


def test_submit_billing_report_warns_on_legacy_error_signature(caplog) -> None:
    client = BillingInternalClient("127.0.0.1:3012", app_secret="ak_bill")

    async def fake_call(_coro):
        raise DiscoveryError(
            "[PERMISSION_DENIED] billing report ingress requires admin or report-ingress privileges"
        )

    class IngressStub:
        def SubmitBillingReport(self, request, metadata, timeout):
            return object()

    client._report_ingress_stub = IngressStub()  # type: ignore[assignment]
    client._call = fake_call  # type: ignore[method-assign]

    import pytest

    with caplog.at_level(logging.WARNING, logger="stew.billing_internal_client"):
        with pytest.raises(DiscoveryError):
            asyncio.run(
                client.submit_billing_report(
                    report=billing_model.BillingReport(
                        business_id="ledger-biz",
                        authorization_id="auth-1",
                        request_id="req-1",
                        user_id="user-1",
                        final_status=billing_model.BillingFinalStatus.BILLING_FINAL_STATUS_SUCCESS,
                    ),
                    source_service="skills-app",
                )
            )

    assert "legacy report-ingress error signature" in caplog.text


def test_internal_authorize_supports_minimal_input_and_returns_resolved_context() -> (
    None
):
    captured: dict[str, object] = {}

    class Stub:
        async def Authorize(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            assert timeout == 30.0
            return billing_pb2.BillingAuthorizationResponse(
                success=True,
                authorization_id=request.context.authorization_id,
                held_points=request.estimated_points,
                resolved_context=billing_pb2.AuthorizationContext(
                    business_id=request.context.business_id,
                    user_id=request.context.user_id,
                    subject_id=request.context.subject_id,
                    subject_type=request.context.subject_type,
                    authorization_id=request.context.authorization_id,
                    request_id=request.context.request_id,
                    policy_id="policy-pro",
                    factor_schema_version="billing.factors.v1",
                ),
            )

    client = BillingInternalClient(
        "127.0.0.1:3012",
        app_secret="ak_bill",
        business_id="biz-default",
    )
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.authorize(
            scope_business_id="ledger-biz",
            user_id="user-1",
            estimated_points=42,
            plan_id_hint="plan-pro",
            business_id="biz-override",
            extra_metadata=[("x-request-id", "req-1")],
        )
    )

    request = captured["request"]

    assert request.context.business_id == "ledger-biz"
    assert request.context.user_id == "user-1"
    assert request.context.subject_id == "user-1"
    assert (
        request.context.subject_type
        == billing_model.BillingSubjectType.BILLING_SUBJECT_TYPE_USER.value
    )
    assert request.plan_id_hint == "plan-pro"
    assert request.estimated_points == 42
    assert request.context.authorization_id != ""
    assert request.context.request_id != ""
    assert captured["metadata"] == [
        ("x-api-key", "ak_bill"),
        ("x-business-id", "biz-override"),
        ("x-request-id", "req-1"),
    ]
    assert isinstance(result, billing_model.BillingAuthorizationResponse)
    assert result.authorization_id == request.context.authorization_id
    assert result.resolved_context is not None
    assert result.resolved_context.policy_id == "policy-pro"
    assert result.resolved_context.request_id == request.context.request_id


def test_compatibility_billing_client_routes_to_split_clients() -> None:
    client = BillingClient("127.0.0.1:3012", app_secret="ak_bill")
    calls: list[tuple[str, tuple[object, ...], dict[str, object]]] = []

    async def fake_query_balance(*args, **kwargs):
        calls.append(("public", args, kwargs))
        return billing_model.BalanceSnapshot(available_balance=9)

    async def fake_finalize(*args, **kwargs):
        calls.append(("internal", args, kwargs))
        return billing_model.SettlementDecision(success=True)

    client.public.query_balance = fake_query_balance  # type: ignore[method-assign]
    client.internal.finalize = fake_finalize  # type: ignore[method-assign]

    balance = asyncio.run(client.query_balance(scope_business_id="ledger-biz"))
    decision = asyncio.run(client.finalize())

    assert balance.available_balance == 9
    assert decision.success is True
    assert [entry[0] for entry in calls] == ["public", "internal"]

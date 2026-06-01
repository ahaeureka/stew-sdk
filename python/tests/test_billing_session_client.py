"""Tests for BillingSessionClient and BillingSessionQueryClient.

Covers the four canonical billing session actions (create, activate,
complete, get_outcome) and proto <-> dict serialization roundtrip.
"""

from __future__ import annotations

import asyncio
from typing import Any

from stew.billing_session_client import (
    BillingSessionClient,
    BillingSessionQueryClient,
)
from stew.api.v1.billing_session_pb2 import (
    ActivateBillingSessionResponse,
    BillingSessionContext,
    BillingSessionStatus,
    CompleteBillingSessionResponse,
    CreateBillingSessionResponse,
)
from stew.api.v1.billing_session_query_pb2 import (
    BillingDiagnostics,
    BillingSessionOutcome,
    GetBillingSessionOutcomeResponse,
    ReservationSummary,
)
from stew.api.v1.billing_common_pb2 import (
    BillingFinalStatus,
    BillingSubjectType,
)

# ---------------------------------------------------------------------------
# Proto <-> dict serialization helpers (mirrors skillforge bridge)
# ---------------------------------------------------------------------------


def _proto_to_dict(ctx: BillingSessionContext) -> dict[str, Any]:
    return {
        "billing_session_id": ctx.billing_session_id,
        "authorization_id": ctx.authorization_id,
        "business_id": ctx.business_id,
        "request_id": ctx.request_id,
        "policy_id": ctx.policy_id,
        "factor_schema_version": ctx.factor_schema_version,
        "subject_id": ctx.subject_id,
        "subject_type": int(ctx.subject_type),
        "execution_token": ctx.execution_token,
        "token_version": ctx.token_version,
    }


def _dict_to_proto(d: dict[str, Any]) -> BillingSessionContext:
    return BillingSessionContext(
        billing_session_id=str(d.get("billing_session_id", "")),
        authorization_id=str(d.get("authorization_id", "")),
        business_id=str(d.get("business_id", "")),
        request_id=str(d.get("request_id", "")),
        policy_id=str(d.get("policy_id", "")),
        factor_schema_version=str(d.get("factor_schema_version", "")),
        subject_id=str(d.get("subject_id", "")),
        subject_type=int(d.get("subject_type", 1)),
        execution_token=str(d.get("execution_token", "")),
        token_version=str(d.get("token_version", "")),
    )


# ---------------------------------------------------------------------------
# Client existence & attribute checks
# ---------------------------------------------------------------------------


def test_billing_session_client_exists() -> None:
    """BillingSessionClient and BillingSessionQueryClient are importable."""
    assert BillingSessionClient is not None
    assert BillingSessionQueryClient is not None


def test_billing_session_client_has_expected_methods() -> None:
    """All four canonical lifecycle methods are present."""
    client = BillingSessionClient("127.0.0.1:3012")
    assert hasattr(client, "start_task_billing")
    assert hasattr(client, "activate_task_billing")
    assert hasattr(client, "complete_task_billing")
    assert callable(client.start_task_billing)
    assert callable(client.activate_task_billing)
    assert callable(client.complete_task_billing)


def test_billing_session_query_client_has_expected_methods() -> None:
    """Outcome and query methods are present."""
    client = BillingSessionQueryClient("127.0.0.1:3012")
    assert hasattr(client, "get_billing_outcome")
    assert hasattr(client, "query_billing_sessions")
    assert callable(client.get_billing_outcome)
    assert callable(client.query_billing_sessions)


# ---------------------------------------------------------------------------
# Proto <-> dict roundtrip
# ---------------------------------------------------------------------------


def test_proto_to_dict_preserves_all_fields() -> None:
    """_proto_to_dict serializes all essential session context fields."""
    ctx = BillingSessionContext(
        billing_session_id="bs_roundtrip",
        authorization_id="auth_1",
        business_id="skillforge",
        request_id="req_1",
        policy_id="pol_1",
        factor_schema_version="v1",
        subject_id="user_1",
        subject_type=BillingSubjectType.BILLING_SUBJECT_TYPE_USER,
        execution_token="tok_secret",
        token_version="1",
    )
    d = _proto_to_dict(ctx)
    assert d["billing_session_id"] == "bs_roundtrip"
    assert d["execution_token"] == "tok_secret"
    assert d["subject_type"] == 1
    assert d["factor_schema_version"] == "v1"
    assert len(d) == 10  # 10 serialized fields


def test_dict_to_proto_roundtrip() -> None:
    """proto -> dict -> proto preserves billing_session_id and execution_token."""
    original = BillingSessionContext(
        billing_session_id="bs_rt",
        authorization_id="auth_rt",
        business_id="biz_rt",
        request_id="req_rt",
        policy_id="pol_rt",
        factor_schema_version="v2",
        subject_id="sub_rt",
        subject_type=BillingSubjectType.BILLING_SUBJECT_TYPE_API_KEY,
        execution_token="tok_rt_secret",
        token_version="2",
    )
    d = _proto_to_dict(original)
    restored = _dict_to_proto(d)
    assert restored.billing_session_id == original.billing_session_id
    assert restored.execution_token == original.execution_token
    assert restored.subject_type == original.subject_type
    assert restored.business_id == original.business_id


def test_dict_to_proto_defaults_missing_keys() -> None:
    """_dict_to_proto fills missing keys with safe defaults."""
    proto = _dict_to_proto({})
    assert proto.billing_session_id == ""
    assert proto.execution_token == ""
    assert proto.subject_type == 1  # BILLING_SUBJECT_TYPE_USER
    assert proto.business_id == ""


def test_dict_to_proto_handles_string_subject_type() -> None:
    """_dict_to_proto coerces string subject_type to int."""
    proto = _dict_to_proto({"subject_type": "3"})
    assert proto.subject_type == 3


# ---------------------------------------------------------------------------
# start_task_billing (mocked stub)
# ---------------------------------------------------------------------------


def test_start_task_billing_returns_session_context() -> None:
    """start_task_billing calls CreateBillingSession and returns a valid response."""
    captured: dict[str, Any] = {}

    class Stub:
        async def CreateBillingSession(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            assert timeout == 30.0
            return CreateBillingSessionResponse(
                session_context=BillingSessionContext(
                    billing_session_id="bs_created",
                    business_id=request.business_id,
                    subject_id=request.subject_id,
                    subject_type=request.subject_type,
                    policy_id="pol_99",
                    factor_schema_version="v1",
                    execution_token="tok_created_abc",
                    token_version="1",
                ),
                held_points=0,
                message="Session created",
            )

    client = BillingSessionClient(
        "127.0.0.1:3012",
        app_secret="ak_test",
        business_id="biz-default",
    )
    client._stub = Stub()  # type: ignore[assignment]

    resp = asyncio.run(
        client.start_task_billing(
            business_id="biz-test",
            subject_id="user-1",
            subject_type=BillingSubjectType.BILLING_SUBJECT_TYPE_USER,
            task_id="task-1",
            request_id="req-1",
            estimated_points=100,
        )
    )

    assert resp.session_context is not None
    assert resp.session_context.billing_session_id == "bs_created"
    assert resp.session_context.execution_token == "tok_created_abc"
    assert resp.session_context.business_id == "biz-test"
    assert resp.session_context.subject_id == "user-1"
    assert resp.held_points == 0
    assert captured["request"].estimated_points == 100


def test_start_task_billing_rejects_empty_business_id() -> None:
    """start_task_billing raises ValueError when business_id is empty."""
    client = BillingSessionClient("127.0.0.1:3012")
    try:
        asyncio.run(
            client.start_task_billing(
                business_id="",
                subject_id="user-1",
            )
        )
        raise AssertionError("Expected ValueError")
    except ValueError as e:
        assert "business_id" in str(e)


def test_start_task_billing_rejects_empty_subject_id() -> None:
    """start_task_billing raises ValueError when subject_id is empty."""
    client = BillingSessionClient("127.0.0.1:3012")
    try:
        asyncio.run(
            client.start_task_billing(
                business_id="biz",
                subject_id="",
            )
        )
        raise AssertionError("Expected ValueError")
    except ValueError as e:
        assert "subject_id" in str(e)


# ---------------------------------------------------------------------------
# activate_task_billing (mocked stub)
# ---------------------------------------------------------------------------


def test_activate_task_billing_success() -> None:
    """activate_task_billing transitions session to AUTHORIZED."""
    captured: dict[str, Any] = {}

    class Stub:
        async def ActivateBillingSession(self, request, metadata, timeout):
            captured["request"] = request
            return ActivateBillingSessionResponse(
                billing_session_id="bs_act",
                authorization_id="auth_act_1",
                held_points=100,
                effective_estimated_points=100,
                override_applied=False,
                session_status=BillingSessionStatus.BILLING_SESSION_STATUS_AUTHORIZED,
                message="Activated",
            )

    client = BillingSessionClient("127.0.0.1:3012", app_secret="ak")
    client._stub = Stub()  # type: ignore[assignment]

    ctx = BillingSessionContext(
        billing_session_id="bs_act",
        execution_token="tok_act",
    )
    resp = asyncio.run(
        client.activate_task_billing(
            session_context=ctx,
            estimated_points_override=80,
        )
    )

    assert resp.authorization_id == "auth_act_1"
    assert resp.held_points == 100
    assert resp.effective_estimated_points == 100
    assert resp.override_applied is False
    assert resp.session_status == BillingSessionStatus.BILLING_SESSION_STATUS_AUTHORIZED


def test_activate_task_billing_with_override() -> None:
    """activate_task_billing passes estimated_points_override correctly."""
    captured: dict[str, Any] = {}

    class Stub:
        async def ActivateBillingSession(self, request, metadata, timeout):
            captured["request"] = request
            return ActivateBillingSessionResponse(
                billing_session_id="bs_ov",
                authorization_id="auth_ov_1",
                held_points=150,
                effective_estimated_points=150,
                override_applied=True,
                session_status=BillingSessionStatus.BILLING_SESSION_STATUS_AUTHORIZED,
                message="Activated with override",
            )

    client = BillingSessionClient("127.0.0.1:3012", app_secret="ak")
    client._stub = Stub()  # type: ignore[assignment]

    ctx = BillingSessionContext(
        billing_session_id="bs_ov",
        execution_token="tok_ov",
    )
    resp = asyncio.run(
        client.activate_task_billing(
            session_context=ctx,
            estimated_points_override=150,
        )
    )

    assert captured["request"].estimated_points_override == 150
    assert resp.override_applied is True
    assert resp.effective_estimated_points == 150


# ---------------------------------------------------------------------------
# complete_task_billing (mocked stub)
# ---------------------------------------------------------------------------


def test_complete_task_billing_success() -> None:
    """complete_task_billing submits final facts and returns decision."""
    captured: dict[str, Any] = {}

    class Stub:
        async def CompleteBillingSession(self, request, metadata, timeout):
            captured["request"] = request
            return CompleteBillingSessionResponse(
                billing_session_id="bs_comp",
                authorization_id="auth_comp_1",
                decision="captured",
                session_status=BillingSessionStatus.BILLING_SESSION_STATUS_CAPTURED,
                deduped=False,
                outcome_ref="outcome_ref_1",
            )

    client = BillingSessionClient("127.0.0.1:3012", app_secret="ak")
    client._stub = Stub()  # type: ignore[assignment]

    ctx = BillingSessionContext(
        billing_session_id="bs_comp",
        execution_token="tok_comp",
    )
    resp = asyncio.run(
        client.complete_task_billing(
            session_context=ctx,
            final_status=BillingFinalStatus.BILLING_FINAL_STATUS_SUCCESS,
            dedupe_key="dedup_1",
            raw_usage_totals={"input_tokens": 500},
            cost_breakdown={"total_tokens": 500},
        )
    )

    assert resp.decision == "captured"
    assert resp.session_status == BillingSessionStatus.BILLING_SESSION_STATUS_CAPTURED
    assert resp.deduped is False
    assert captured["request"].task_final_facts.dedupe_key == "dedup_1"


def test_complete_task_billing_deduped() -> None:
    """complete_task_billing returns deduped=True for repeated submission."""

    class Stub:
        async def CompleteBillingSession(self, request, metadata, timeout):
            return CompleteBillingSessionResponse(
                billing_session_id="bs_dedup",
                authorization_id="auth_dedup",
                decision="captured",
                session_status=BillingSessionStatus.BILLING_SESSION_STATUS_CAPTURED,
                deduped=True,
                outcome_ref="outcome_ref_dup",
            )

    client = BillingSessionClient("127.0.0.1:3012", app_secret="ak")
    client._stub = Stub()  # type: ignore[assignment]

    ctx = BillingSessionContext(
        billing_session_id="bs_dedup",
        execution_token="tok_dedup",
    )
    resp = asyncio.run(
        client.complete_task_billing(
            session_context=ctx,
            final_status=BillingFinalStatus.BILLING_FINAL_STATUS_SUCCESS,
            dedupe_key="dedup_repeat",
            raw_usage_totals={},
            cost_breakdown={},
        )
    )

    assert resp.deduped is True
    assert resp.decision == "captured"


# ---------------------------------------------------------------------------
# get_billing_outcome (mocked stub)
# ---------------------------------------------------------------------------


def test_get_billing_outcome_returns_diagnostics() -> None:
    """get_billing_outcome returns outcome with diagnostics."""

    class Stub:
        async def GetBillingSessionOutcome(self, request, metadata, timeout):
            return GetBillingSessionOutcomeResponse(
                outcome=BillingSessionOutcome(
                    billing_session=None,
                    reservation_summary=ReservationSummary(
                        authorization_id="auth_out",
                    ),
                    latest_decision="captured",
                    diagnostics=BillingDiagnostics(
                        current_stage=4,  # CAPTURED
                        blocking_reason_code=0,  # NONE
                        action_required=0,  # NONE
                        action_owner=0,  # NONE
                        reconcile_required=False,
                    ),
                )
            )

    client = BillingSessionQueryClient("127.0.0.1:3012", app_secret="ak")
    client._stub = Stub()  # type: ignore[assignment]

    resp = asyncio.run(
        client.get_billing_outcome(
            billing_session_id="bs_out",
        )
    )

    assert resp.latest_decision == "captured"
    assert resp.diagnostics is not None
    assert resp.diagnostics.current_stage == 4
    assert resp.diagnostics.blocking_reason_code == 0
    assert resp.diagnostics.reconcile_required is False


def test_get_billing_outcome_uses_task_id() -> None:
    """get_billing_outcome supports query by task_id."""
    captured: dict[str, Any] = {}

    class Stub:
        async def GetBillingSessionOutcome(self, request, metadata, timeout):
            captured["request"] = request
            return GetBillingSessionOutcomeResponse(outcome=BillingSessionOutcome())

    client = BillingSessionQueryClient("127.0.0.1:3012", app_secret="ak")
    client._stub = Stub()  # type: ignore[assignment]

    asyncio.run(
        client.get_billing_outcome(
            task_id="task-42",
        )
    )

    assert captured["request"].task_id == "task-42"


# ---------------------------------------------------------------------------
# End-to-end lifecycle simulation (all stubs wired)
# ---------------------------------------------------------------------------


def test_full_lifecycle_create_activate_complete_outcome() -> None:
    """Simulate a complete billing session lifecycle with mocked stubs."""

    session_id = "bs_lifecycle"
    exec_token = "tok_lifecycle_999"

    class SessionStub:
        async def CreateBillingSession(self, request, metadata, timeout):
            return CreateBillingSessionResponse(
                session_context=BillingSessionContext(
                    billing_session_id=session_id,
                    business_id=request.business_id,
                    subject_id=request.subject_id,
                    policy_id="pol_lc",
                    factor_schema_version="v1",
                    execution_token=exec_token,
                    token_version="1",
                ),
                held_points=0,
            )

        async def ActivateBillingSession(self, request, metadata, timeout):
            return ActivateBillingSessionResponse(
                billing_session_id=session_id,
                authorization_id="auth_lc",
                held_points=200,
                effective_estimated_points=200,
                override_applied=False,
                session_status=BillingSessionStatus.BILLING_SESSION_STATUS_AUTHORIZED,
            )

        async def CompleteBillingSession(self, request, metadata, timeout):
            return CompleteBillingSessionResponse(
                billing_session_id=session_id,
                authorization_id="auth_lc",
                decision="captured",
                session_status=BillingSessionStatus.BILLING_SESSION_STATUS_CAPTURED,
                deduped=False,
                outcome_ref="out_lc",
            )

    class QueryStub:
        async def GetBillingSessionOutcome(self, request, metadata, timeout):
            return GetBillingSessionOutcomeResponse(
                outcome=BillingSessionOutcome(
                    billing_session=None,
                    reservation_summary=ReservationSummary(
                        authorization_id="auth_lc",
                    ),
                    latest_decision="captured",
                    diagnostics=BillingDiagnostics(
                        current_stage=4,
                        blocking_reason_code=0,
                        action_required=0,
                        action_owner=0,
                        reconcile_required=False,
                    ),
                )
            )

    session_client = BillingSessionClient("127.0.0.1:3012", app_secret="ak")
    session_client._stub = SessionStub()  # type: ignore[assignment]

    query_client = BillingSessionQueryClient("127.0.0.1:3012", app_secret="ak")
    query_client._stub = QueryStub()  # type: ignore[assignment]

    async def _run() -> dict[str, Any]:
        # 1. Create
        create_resp = await session_client.start_task_billing(
            business_id="biz-lifecycle",
            subject_id="user-lc",
            task_id="task-lc",
            estimated_points=200,
        )
        ctx = create_resp.session_context
        assert ctx is not None
        assert ctx.billing_session_id == session_id
        assert ctx.execution_token == exec_token

        # Serialize context (simulates persistence)
        ctx_dict = _proto_to_dict(ctx)
        assert ctx_dict["execution_token"] == exec_token

        # 2. Activate (after deserialization)
        restored_ctx = _dict_to_proto(ctx_dict)
        act_resp = await session_client.activate_task_billing(
            session_context=restored_ctx,
            estimated_points_override=0,
        )
        assert act_resp.authorization_id == "auth_lc"
        assert (
            act_resp.session_status
            == BillingSessionStatus.BILLING_SESSION_STATUS_AUTHORIZED
        )

        # 3. Complete
        comp_resp = await session_client.complete_task_billing(
            session_context=restored_ctx,
            final_status=BillingFinalStatus.BILLING_FINAL_STATUS_SUCCESS,
            dedupe_key="dedup_lc",
            raw_usage_totals={"input_tokens": 1000},
            cost_breakdown={"total_tokens": 1000},
        )
        assert comp_resp.decision == "captured"
        assert comp_resp.deduped is False

        # 4. Get outcome
        outcome = await query_client.get_billing_outcome(
            billing_session_id=session_id,
        )
        assert outcome.latest_decision == "captured"
        assert outcome.diagnostics is not None

        return {
            "session_id": session_id,
            "authorization_id": act_resp.authorization_id,
            "decision": comp_resp.decision,
        }

    result = asyncio.run(_run())
    assert result["session_id"] == session_id
    assert result["authorization_id"] == "auth_lc"
    assert result["decision"] == "captured"

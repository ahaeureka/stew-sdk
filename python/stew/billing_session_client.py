"""Stew Gateway BillingSession gRPC client.

Provides high-level async methods for the billing session lifecycle:
  - start_task_billing()
  - activate_task_billing()
  - complete_task_billing()
  - get_billing_outcome()
  - query_billing_sessions()
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import Any
from uuid import uuid4

import grpc.aio

from stew.api.v1 import billing_session_pb2_grpc as _bill_session_grpc
from stew.api.v1 import billing_session_query_pb2_grpc as _bill_session_query_grpc
from stew.api.v1.billing_session_pb2 import (
    ActivateBillingSessionRequest,
    ActivateBillingSessionResponse,
    BillingSession,
    BillingSessionContext,
    BillingSessionExecutionMode,
    BillingSessionStatus,
    CompleteBillingSessionRequest,
    CompleteBillingSessionResponse,
    CreateBillingSessionRequest,
    CreateBillingSessionResponse,
    TaskFinalFacts,
)
from stew.api.v1.billing_session_query_pb2 import (
    BillingActionOwner,
    BillingActionRequired,
    BillingBlockingReasonCode,
    BillingDiagnostics,
    BillingDiagnosticsStage,
    BillingSessionOutcome,
    GetBillingSessionOutcomeRequest,
    GetBillingSessionOutcomeResponse,
    QueryBillingSessionsRequest,
    QueryBillingSessionsResponse,
    ReservationSummary,
)
from stew.api.v1.billing_common_pb2 import (
    BillingFinalStatus,
    BillingMissingReportAction,
    BillingReservationStatus,
    BillingSubjectType,
)

from ._billing_client_shared import BillingAioClientBase
from ._discovery.helpers import MetadataEntry, _normalize_extra_metadata

_logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Default idempotency helpers
# ---------------------------------------------------------------------------


def _generated_dedupe_key(task_id: str, run_id: str) -> str:
    suffix = uuid4().hex[:12]
    base = task_id or "task"
    if run_id:
        return f"{base}:{run_id}:{suffix}"
    return f"{base}:{suffix}"


def _generated_delivery_request_id() -> str:
    return f"delivery_{uuid4().hex}"


# ---------------------------------------------------------------------------
# BillingSessionClient
# ---------------------------------------------------------------------------


class BillingSessionClient(
    BillingAioClientBase[_bill_session_grpc.BillingSessionServiceStub]
):
    """Async gRPC client for stew.api.v1.BillingSessionService.

    This client provides the four canonical actions on the billing session
    lifecycle:
        start_task_billing  -> CreateBillingSession
        activate_task_billing -> ActivateBillingSession
        complete_task_billing -> CompleteBillingSession
        get_billing_outcome   -> GetBillingSessionOutcome
        query_billing_sessions -> QueryBillingSessions
    """

    def _create_stub(
        self,
        channel: grpc.aio.Channel,
    ) -> _bill_session_grpc.BillingSessionServiceStub:
        return _bill_session_grpc.BillingSessionServiceStub(channel)

    # ------------------------------------------------------------------
    # start_task_billing
    # ------------------------------------------------------------------

    async def start_task_billing(
        self,
        *,
        business_id: str,
        subject_id: str,
        subject_type: BillingSubjectType
        | int = BillingSubjectType.BILLING_SUBJECT_TYPE_USER,
        task_id: str = "",
        run_id: str = "",
        request_id: str = "",
        plan_id_hint: str = "",
        estimated_points: int = 0,
        request_factors: dict[str, Any] | None = None,
        execution_mode: BillingSessionExecutionMode
        | int = BillingSessionExecutionMode.BILLING_SESSION_EXECUTION_MODE_ASYNC_TASK,
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> CreateBillingSessionResponse:
        """Create a billing session at task acceptance (pre-check only, no hold).

        Returns a session context with an opaque execution token. The caller
        must persist this context and later call activate_task_billing() before
        real execution begins.
        """
        if not business_id:
            raise ValueError("business_id is required")
        if not subject_id:
            raise ValueError("subject_id is required")
        if not task_id:
            task_id = f"task_{uuid4().hex[:12]}"
        if not request_id:
            request_id = f"req_{uuid4().hex}"

        request = CreateBillingSessionRequest(
            business_id=business_id,
            subject_id=subject_id,
            subject_type=subject_type,
            task_id=task_id,
            run_id=run_id,
            request_id=request_id,
            plan_id_hint=plan_id_hint,
            estimated_points=estimated_points,
            execution_mode=execution_mode,
        )
        if request_factors:
            request.request_factors.update(request_factors)

        metadata = list(_normalize_extra_metadata(extra_metadata))
        return await self._call(
            self._s.CreateBillingSession(
                request,
                metadata=metadata,
                timeout=self._timeout,
            )
        )

    # ------------------------------------------------------------------
    # activate_task_billing
    # ------------------------------------------------------------------

    async def activate_task_billing(
        self,
        *,
        session_context: BillingSessionContext | None = None,
        billing_session_id: str = "",
        run_id: str = "",
        estimated_points_override: int = 0,
        activation_reason: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> ActivateBillingSessionResponse:
        """Activate a billing session before real task execution begins.

        This transitions the session from CREATED to AUTHORIZED/RUNNING and
        establishes a held reservation.

        estimated_points_override:
            0          -> use the original estimate from session creation
            <= original -> activate with reduced budget, no re-check needed
            >  original -> activate with increased budget, platform re-checks
                           balance and policy; rejected if above platform
                           threshold.
        """
        if session_context is not None:
            request = ActivateBillingSessionRequest(
                session_context=session_context,
                run_id=run_id,
                estimated_points_override=estimated_points_override,
                activation_reason=activation_reason,
            )
        elif billing_session_id:
            request = ActivateBillingSessionRequest(
                billing_session_id=billing_session_id,
                run_id=run_id,
                estimated_points_override=estimated_points_override,
                activation_reason=activation_reason,
            )
        else:
            raise ValueError("session_context or billing_session_id is required")

        metadata = list(_normalize_extra_metadata(extra_metadata))
        return await self._call(
            self._s.ActivateBillingSession(
                request,
                metadata=metadata,
                timeout=self._timeout,
            )
        )

    # ------------------------------------------------------------------
    # complete_task_billing
    # ------------------------------------------------------------------

    async def complete_task_billing(
        self,
        *,
        session_context: BillingSessionContext | None = None,
        billing_session_id: str = "",
        final_status: BillingFinalStatus
        | int = BillingFinalStatus.BILLING_FINAL_STATUS_SUCCESS,
        dedupe_key: str = "",
        delivery_request_id: str = "",
        raw_usage_totals: dict[str, Any] | None = None,
        cost_breakdown: dict[str, Any] | None = None,
        business_factors: dict[str, Any] | None = None,
        provider_usage_facts: dict[str, Any] | None = None,
        execution_hints: dict[str, Any] | None = None,
        refund_reason: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> CompleteBillingSessionResponse:
        """Submit one-shot terminal facts at task end.

        Only callable once per session. Repeated submissions with the same
        dedupe_key are idempotent; different payloads with the same
        dedupe_key produce a conflict error.
        """
        if not dedupe_key:
            dedupe_key = _generated_dedupe_key(billing_session_id or "session", "")
        if not delivery_request_id:
            delivery_request_id = _generated_delivery_request_id()

        facts = TaskFinalFacts(
            final_status=final_status,
            dedupe_key=dedupe_key,
            delivery_request_id=delivery_request_id,
            refund_reason=refund_reason,
        )
        if raw_usage_totals is not None:
            facts.raw_usage_totals.update(raw_usage_totals)
        if cost_breakdown is not None:
            facts.cost_breakdown.update(cost_breakdown)
        if business_factors is not None:
            facts.business_factors.update(business_factors)
        if provider_usage_facts is not None:
            facts.provider_usage_facts.update(provider_usage_facts)
        if execution_hints is not None:
            facts.execution_hints.update(execution_hints)

        if session_context is not None:
            request = CompleteBillingSessionRequest(
                session_context=session_context,
                task_final_facts=facts,
            )
        elif billing_session_id:
            request = CompleteBillingSessionRequest(
                billing_session_id=billing_session_id,
                task_final_facts=facts,
            )
        else:
            raise ValueError("session_context or billing_session_id is required")

        metadata = list(_normalize_extra_metadata(extra_metadata))
        return await self._call(
            self._s.CompleteBillingSession(
                request,
                metadata=metadata,
                timeout=self._timeout,
            )
        )


# ---------------------------------------------------------------------------
# BillingSessionQueryClient
# ---------------------------------------------------------------------------


class BillingSessionQueryClient(
    BillingAioClientBase[_bill_session_query_grpc.BillingSessionQueryServiceStub]
):
    """Async gRPC client for stew.api.v1.BillingSessionQueryService."""

    def _create_stub(
        self,
        channel: grpc.aio.Channel,
    ) -> _bill_session_query_grpc.BillingSessionQueryServiceStub:
        return _bill_session_query_grpc.BillingSessionQueryServiceStub(channel)

    async def get_billing_outcome(
        self,
        *,
        billing_session_id: str = "",
        authorization_id: str = "",
        request_id: str = "",
        task_id: str = "",
        run_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> BillingSessionOutcome:
        """Query the outcome and diagnostics for a billing session.

        Provide exactly one query key.
        """
        if billing_session_id:
            request = GetBillingSessionOutcomeRequest(
                billing_session_id=billing_session_id,
            )
        elif authorization_id:
            request = GetBillingSessionOutcomeRequest(
                authorization_id=authorization_id,
            )
        elif request_id:
            request = GetBillingSessionOutcomeRequest(
                request_id=request_id,
            )
        elif task_id:
            request = GetBillingSessionOutcomeRequest(
                task_id=task_id,
            )
        elif run_id:
            request = GetBillingSessionOutcomeRequest(
                run_id=run_id,
            )
        else:
            raise ValueError("one query key is required")

        metadata = list(_normalize_extra_metadata(extra_metadata))
        response = await self._call(
            self._s.GetBillingSessionOutcome(
                request,
                metadata=metadata,
                timeout=self._timeout,
            )
        )
        outcome = response.outcome
        if outcome is None:
            raise RuntimeError("GetBillingSessionOutcome returned empty outcome")
        return outcome

    async def query_billing_sessions(
        self,
        *,
        business_id: str = "",
        subject_id: str = "",
        subject_type: BillingSubjectType
        | int = BillingSubjectType.BILLING_SUBJECT_TYPE_USER,
        status_filter: Sequence[BillingSessionStatus | int] = (),
        created_after_seconds: int = 0,
        created_before_seconds: int = 0,
        page_size: int = 50,
        page_token: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> QueryBillingSessionsResponse:
        """List billing sessions with optional filters."""

        from google.protobuf.timestamp_pb2 import Timestamp as PbTimestamp

        request = QueryBillingSessionsRequest(
            business_id=business_id,
            subject_id=subject_id,
            subject_type=subject_type,
            page_size=page_size,
            page_token=page_token,
        )
        if status_filter:
            request.status_filter.extend(int(s) for s in status_filter)
        if created_after_seconds:
            ts_after = PbTimestamp()
            ts_after.FromSeconds(created_after_seconds)
            request.created_after.CopyFrom(ts_after)
        if created_before_seconds:
            ts_before = PbTimestamp()
            ts_before.FromSeconds(created_before_seconds)
            request.created_before.CopyFrom(ts_before)

        metadata = list(_normalize_extra_metadata(extra_metadata))
        return await self._call(
            self._s.QueryBillingSessions(
                request,
                metadata=metadata,
                timeout=self._timeout,
            )
        )

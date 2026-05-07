"""Stew Gateway billing gRPC clients."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import grpc
import grpc.aio

from stew.api.v1 import billing_model as _bill_model
from stew.api.v1 import billing_pb2 as _bill_pb
from stew.api.v1 import billing_pb2_grpc as _bill_grpc

from ._discovery.errors import DiscoveryError
from ._discovery.helpers import (
    AioGatewayClientBase,
    MetadataEntry,
    SyncGatewayClientBase,
    wrap_rpc_error,
)

BillingError = DiscoveryError


def _coerce_protobuf_message(value: Any, message_type: type[Any]) -> Any:
    if isinstance(value, message_type):
        return value
    if hasattr(value, "to_protobuf"):
        message = value.to_protobuf()
        if isinstance(message, message_type):
            return message
    raise TypeError(f"Expected {message_type.__name__}, got {type(value).__name__}")


def _enum_value(value: Any) -> int:
    return int(getattr(value, "value", value))


def _coerce_authorization_context(
    value: _bill_model.AuthorizationContext | _bill_pb.AuthorizationContext,
) -> _bill_pb.AuthorizationContext:
    return _coerce_protobuf_message(value, _bill_pb.AuthorizationContext)


def _coerce_billing_report(
    value: _bill_model.BillingReport | _bill_pb.BillingReport,
) -> _bill_pb.BillingReport:
    return _coerce_protobuf_message(value, _bill_pb.BillingReport)


def _coerce_billing_policy_artifact_type(value: Any) -> int:
    return _enum_value(value)


class BillingClient(AioGatewayClientBase[_bill_grpc.BillingServiceStub]):
    """Async gRPC client for stew.api.v1.BillingService.

    Connected clients inject API key and optional x-business-id through the
    shared client interceptor stack. Billing ledger scope still comes from the
    request body fields such as AuthorizationContext.business_id.
    """

    def _create_stub(self, channel: grpc.aio.Channel) -> _bill_grpc.BillingServiceStub:
        return _bill_grpc.BillingServiceStub(channel)

    async def _call(self, coro: Any) -> Any:
        try:
            return await coro
        except grpc.RpcError as exc:
            raise wrap_rpc_error(exc) from exc

    async def estimate_charge(
        self,
        request: _bill_model.EstimateChargeRequest | _bill_pb.EstimateChargeRequest | None = None,
        *,
        context: _bill_model.AuthorizationContext | _bill_pb.AuthorizationContext | None = None,
        request_factors: dict[str, Any] | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.EstimateChargeResponse:
        if request is not None:
            message = _coerce_protobuf_message(request, _bill_pb.EstimateChargeRequest)
        else:
            message = _bill_pb.EstimateChargeRequest()
            if context is not None:
                message.context.CopyFrom(_coerce_authorization_context(context))
            if request_factors is not None:
                message.request_factors.update(request_factors)

        response = await self._call(
            self._s.EstimateCharge(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.EstimateChargeResponse.from_protobuf(response)

    async def authorize(
        self,
        request: _bill_model.AuthorizeRequest | _bill_pb.AuthorizeRequest | None = None,
        *,
        context: _bill_model.AuthorizationContext | _bill_pb.AuthorizationContext | None = None,
        estimated_points: int = 0,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingAuthorizationResponse:
        if request is not None:
            message = _coerce_protobuf_message(request, _bill_pb.AuthorizeRequest)
        else:
            message = _bill_pb.AuthorizeRequest(estimated_points=estimated_points)
            if context is not None:
                message.context.CopyFrom(_coerce_authorization_context(context))

        response = await self._call(
            self._s.Authorize(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingAuthorizationResponse.from_protobuf(response)

    async def finalize(
        self,
        request: _bill_model.FinalizeRequest | _bill_pb.FinalizeRequest | None = None,
        *,
        context: _bill_model.AuthorizationContext | _bill_pb.AuthorizationContext | None = None,
        report: _bill_model.BillingReport | _bill_pb.BillingReport | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.SettlementDecision:
        if request is not None:
            message = _coerce_protobuf_message(request, _bill_pb.FinalizeRequest)
        else:
            message = _bill_pb.FinalizeRequest()
            if context is not None:
                message.context.CopyFrom(_coerce_authorization_context(context))
            if report is not None:
                message.report.CopyFrom(_coerce_billing_report(report))

        response = await self._call(
            self._s.Finalize(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.SettlementDecision.from_protobuf(response)

    async def release(
        self,
        request: _bill_model.ReleaseRequest | _bill_pb.ReleaseRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        authorization_id: str = "",
        request_id: str = "",
        reason: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.SettlementDecision:
        message = (
            _coerce_protobuf_message(request, _bill_pb.ReleaseRequest)
            if request is not None
            else _bill_pb.ReleaseRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                authorization_id=authorization_id,
                request_id=request_id,
                reason=reason,
            )
        )
        response = await self._call(
            self._s.Release(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.SettlementDecision.from_protobuf(response)

    async def refund(
        self,
        request: _bill_model.RefundRequest | _bill_pb.RefundRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        authorization_id: str = "",
        request_id: str = "",
        reason: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.SettlementDecision:
        message = (
            _coerce_protobuf_message(request, _bill_pb.RefundRequest)
            if request is not None
            else _bill_pb.RefundRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                authorization_id=authorization_id,
                request_id=request_id,
                reason=reason,
            )
        )
        response = await self._call(
            self._s.Refund(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.SettlementDecision.from_protobuf(response)

    async def query_balance(
        self,
        request: _bill_model.QueryBalanceRequest | _bill_pb.QueryBalanceRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        subject_type: _bill_model.BillingSubjectType | int = _bill_model.BillingSubjectType(0),
        user_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BalanceSnapshot:
        message = (
            _coerce_protobuf_message(request, _bill_pb.QueryBalanceRequest)
            if request is not None
            else _bill_pb.QueryBalanceRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                subject_type=_enum_value(subject_type),
                user_id=user_id,
            )
        )
        response = await self._call(
            self._s.QueryBalance(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.BalanceSnapshot.from_protobuf(response)

    async def grant_credits(
        self,
        request: _bill_model.GrantCreditsRequest | _bill_pb.GrantCreditsRequest | None = None,
        *,
        scope_business_id: str = "",
        user_id: str = "",
        subject_id: str = "",
        subject_type: _bill_model.BillingSubjectType | int = _bill_model.BillingSubjectType(0),
        credit_type: str = "",
        amount: int = 0,
        expires_at_epoch_seconds: int = 0,
        idempotency_key: str = "",
        metadata: dict[str, str] | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.CreditGrant:
        message = (
            _coerce_protobuf_message(request, _bill_pb.GrantCreditsRequest)
            if request is not None
            else _bill_pb.GrantCreditsRequest(
                business_id=scope_business_id,
                user_id=user_id,
                subject_id=subject_id,
                subject_type=_enum_value(subject_type),
                credit_type=credit_type,
                amount=amount,
                expires_at_epoch_seconds=expires_at_epoch_seconds,
                idempotency_key=idempotency_key,
                metadata=metadata or {},
            )
        )
        response = await self._call(
            self._s.GrantCredits(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.CreditGrant.from_protobuf(response)

    async def list_grants(
        self,
        request: _bill_model.ListGrantsRequest | _bill_pb.ListGrantsRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        subject_type: _bill_model.BillingSubjectType | int = _bill_model.BillingSubjectType(0),
        user_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.ListGrantsResponse:
        message = (
            _coerce_protobuf_message(request, _bill_pb.ListGrantsRequest)
            if request is not None
            else _bill_pb.ListGrantsRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                subject_type=_enum_value(subject_type),
                user_id=user_id,
            )
        )
        response = await self._call(
            self._s.ListGrants(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.ListGrantsResponse.from_protobuf(response)

    async def get_transaction(
        self,
        request: _bill_model.GetBillingTransactionRequest
        | _bill_pb.GetBillingTransactionRequest
        | None = None,
        *,
        scope_business_id: str = "",
        request_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingTransaction:
        message = (
            _coerce_protobuf_message(request, _bill_pb.GetBillingTransactionRequest)
            if request is not None
            else _bill_pb.GetBillingTransactionRequest(
                business_id=scope_business_id,
                request_id=request_id,
            )
        )
        response = await self._call(
            self._s.GetTransaction(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingTransaction.from_protobuf(response)

    async def query_transactions(
        self,
        request: _bill_model.QueryTransactionsRequest
        | _bill_pb.QueryTransactionsRequest
        | None = None,
        *,
        scope_business_id: str = "",
        request_id: str = "",
        authorization_id: str = "",
        subject_id: str = "",
        subject_type: _bill_model.BillingSubjectType | int = _bill_model.BillingSubjectType(0),
        user_id: str = "",
        start_time_epoch_seconds: int = 0,
        end_time_epoch_seconds: int = 0,
        page_size: int = 0,
        page_token: str = "",
        transaction_type: _bill_model.BillingTransactionType | int = _bill_model.BillingTransactionType(0),
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.QueryTransactionsResponse:
        message = (
            _coerce_protobuf_message(request, _bill_pb.QueryTransactionsRequest)
            if request is not None
            else _bill_pb.QueryTransactionsRequest(
                business_id=scope_business_id,
                request_id=request_id,
                authorization_id=authorization_id,
                subject_id=subject_id,
                subject_type=_enum_value(subject_type),
                user_id=user_id,
                start_time_epoch_seconds=start_time_epoch_seconds,
                end_time_epoch_seconds=end_time_epoch_seconds,
                page_size=page_size,
                page_token=page_token,
                transaction_type=_enum_value(transaction_type),
            )
        )
        response = await self._call(
            self._s.QueryTransactions(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.QueryTransactionsResponse.from_protobuf(response)

    async def query_snapshot(
        self,
        request: _bill_model.QuerySnapshotRequest | _bill_pb.QuerySnapshotRequest | None = None,
        *,
        scope_business_id: str = "",
        request_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingSettlementSnapshot:
        message = (
            _coerce_protobuf_message(request, _bill_pb.QuerySnapshotRequest)
            if request is not None
            else _bill_pb.QuerySnapshotRequest(
                business_id=scope_business_id,
                request_id=request_id,
            )
        )
        response = await self._call(
            self._s.QuerySnapshot(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingSettlementSnapshot.from_protobuf(response)

    async def manual_reconcile(
        self,
        request: _bill_model.ManualReconcileRequest | _bill_pb.ManualReconcileRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        request_id: str = "",
        authorization_id: str = "",
        reason: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.ManualReconcileResponse:
        message = (
            _coerce_protobuf_message(request, _bill_pb.ManualReconcileRequest)
            if request is not None
            else _bill_pb.ManualReconcileRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                request_id=request_id,
                authorization_id=authorization_id,
                reason=reason,
            )
        )
        response = await self._call(
            self._s.ManualReconcile(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.ManualReconcileResponse.from_protobuf(response)

    async def create_policy_artifact(
        self,
        request: _bill_model.CreateBillingPolicyArtifactRequest
        | _bill_pb.CreateBillingPolicyArtifactRequest
        | None = None,
        *,
        scope_business_id: str = "",
        artifact_type: _bill_model.BillingPolicyArtifactType | int = _bill_model.BillingPolicyArtifactType(0),
        artifact_version: str = "",
        content: dict[str, Any] | None = None,
        policy_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingPolicyArtifact:
        message = (
            _coerce_protobuf_message(request, _bill_pb.CreateBillingPolicyArtifactRequest)
            if request is not None
            else _bill_pb.CreateBillingPolicyArtifactRequest(
                business_id=scope_business_id,
                artifact_type=_coerce_billing_policy_artifact_type(artifact_type),
                artifact_version=artifact_version,
                content=content or {},
                policy_id=policy_id,
            )
        )
        response = await self._call(
            self._s.CreatePolicyArtifact(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingPolicyArtifact.from_protobuf(response)

    async def get_policy_artifact(
        self,
        request: _bill_model.GetBillingPolicyArtifactRequest
        | _bill_pb.GetBillingPolicyArtifactRequest
        | None = None,
        *,
        artifact_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingPolicyArtifact:
        message = (
            _coerce_protobuf_message(request, _bill_pb.GetBillingPolicyArtifactRequest)
            if request is not None
            else _bill_pb.GetBillingPolicyArtifactRequest(artifact_id=artifact_id)
        )
        response = await self._call(
            self._s.GetPolicyArtifact(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingPolicyArtifact.from_protobuf(response)

    async def list_policy_artifacts(
        self,
        request: _bill_model.ListBillingPolicyArtifactsRequest
        | _bill_pb.ListBillingPolicyArtifactsRequest
        | None = None,
        *,
        scope_business_id: str = "",
        artifact_type: _bill_model.BillingPolicyArtifactType | int = _bill_model.BillingPolicyArtifactType(0),
        policy_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.ListBillingPolicyArtifactsResponse:
        message = (
            _coerce_protobuf_message(request, _bill_pb.ListBillingPolicyArtifactsRequest)
            if request is not None
            else _bill_pb.ListBillingPolicyArtifactsRequest(
                business_id=scope_business_id,
                artifact_type=_coerce_billing_policy_artifact_type(artifact_type),
                policy_id=policy_id,
            )
        )
        response = await self._call(
            self._s.ListPolicyArtifacts(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.ListBillingPolicyArtifactsResponse.from_protobuf(response)

    async def publish_policy_bundle(
        self,
        request: _bill_model.PublishBillingPolicyBundleRequest
        | _bill_pb.PublishBillingPolicyBundleRequest
        | None = None,
        *,
        scope_business_id: str = "",
        policy_id: str = "",
        factor_schema_version: str = "",
        provider_rate_card_artifact_id: str = "",
        point_policy_artifact_id: str = "",
        money_policy_artifact_id: str = "",
        estimator_artifact_id: str = "",
        bundle_version: int = 0,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingPolicyBundle:
        message = (
            _coerce_protobuf_message(request, _bill_pb.PublishBillingPolicyBundleRequest)
            if request is not None
            else _bill_pb.PublishBillingPolicyBundleRequest(
                business_id=scope_business_id,
                policy_id=policy_id,
                factor_schema_version=factor_schema_version,
                provider_rate_card_artifact_id=provider_rate_card_artifact_id,
                point_policy_artifact_id=point_policy_artifact_id,
                money_policy_artifact_id=money_policy_artifact_id,
                estimator_artifact_id=estimator_artifact_id,
                bundle_version=bundle_version,
            )
        )
        response = await self._call(
            self._s.PublishPolicyBundle(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingPolicyBundle.from_protobuf(response)

    async def get_policy_bundle(
        self,
        request: _bill_model.GetBillingPolicyBundleRequest
        | _bill_pb.GetBillingPolicyBundleRequest
        | None = None,
        *,
        scope_business_id: str = "",
        policy_id: str = "",
        bundle_version: int = 0,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingPolicyBundle:
        message = (
            _coerce_protobuf_message(request, _bill_pb.GetBillingPolicyBundleRequest)
            if request is not None
            else _bill_pb.GetBillingPolicyBundleRequest(
                business_id=scope_business_id,
                policy_id=policy_id,
                bundle_version=bundle_version,
            )
        )
        response = await self._call(
            self._s.GetPolicyBundle(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingPolicyBundle.from_protobuf(response)

    async def list_policy_bundles(
        self,
        request: _bill_model.ListBillingPolicyBundlesRequest
        | _bill_pb.ListBillingPolicyBundlesRequest
        | None = None,
        *,
        scope_business_id: str = "",
        policy_id: str = "",
        active_only: bool = False,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.ListBillingPolicyBundlesResponse:
        message = (
            _coerce_protobuf_message(request, _bill_pb.ListBillingPolicyBundlesRequest)
            if request is not None
            else _bill_pb.ListBillingPolicyBundlesRequest(
                business_id=scope_business_id,
                policy_id=policy_id,
                active_only=active_only,
            )
        )
        response = await self._call(
            self._s.ListPolicyBundles(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _bill_model.ListBillingPolicyBundlesResponse.from_protobuf(response)


class SyncBillingClient(SyncGatewayClientBase[BillingClient]):
    """Synchronous facade over :class:`BillingClient`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(BillingClient, *args, **kwargs)

    def estimate_charge(self, *args: Any, **kwargs: Any) -> _bill_model.EstimateChargeResponse:
        return self._run(self._client.estimate_charge(*args, **kwargs))

    def authorize(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.BillingAuthorizationResponse:
        return self._run(self._client.authorize(*args, **kwargs))

    def finalize(self, *args: Any, **kwargs: Any) -> _bill_model.SettlementDecision:
        return self._run(self._client.finalize(*args, **kwargs))

    def release(self, *args: Any, **kwargs: Any) -> _bill_model.SettlementDecision:
        return self._run(self._client.release(*args, **kwargs))

    def refund(self, *args: Any, **kwargs: Any) -> _bill_model.SettlementDecision:
        return self._run(self._client.refund(*args, **kwargs))

    def query_balance(self, *args: Any, **kwargs: Any) -> _bill_model.BalanceSnapshot:
        return self._run(self._client.query_balance(*args, **kwargs))

    def grant_credits(self, *args: Any, **kwargs: Any) -> _bill_model.CreditGrant:
        return self._run(self._client.grant_credits(*args, **kwargs))

    def list_grants(self, *args: Any, **kwargs: Any) -> _bill_model.ListGrantsResponse:
        return self._run(self._client.list_grants(*args, **kwargs))

    def get_transaction(self, *args: Any, **kwargs: Any) -> _bill_model.BillingTransaction:
        return self._run(self._client.get_transaction(*args, **kwargs))

    def query_transactions(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.QueryTransactionsResponse:
        return self._run(self._client.query_transactions(*args, **kwargs))

    def query_snapshot(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.BillingSettlementSnapshot:
        return self._run(self._client.query_snapshot(*args, **kwargs))

    def manual_reconcile(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.ManualReconcileResponse:
        return self._run(self._client.manual_reconcile(*args, **kwargs))

    def create_policy_artifact(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.BillingPolicyArtifact:
        return self._run(self._client.create_policy_artifact(*args, **kwargs))

    def get_policy_artifact(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.BillingPolicyArtifact:
        return self._run(self._client.get_policy_artifact(*args, **kwargs))

    def list_policy_artifacts(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.ListBillingPolicyArtifactsResponse:
        return self._run(self._client.list_policy_artifacts(*args, **kwargs))

    def publish_policy_bundle(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.BillingPolicyBundle:
        return self._run(self._client.publish_policy_bundle(*args, **kwargs))

    def get_policy_bundle(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.BillingPolicyBundle:
        return self._run(self._client.get_policy_bundle(*args, **kwargs))

    def list_policy_bundles(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.ListBillingPolicyBundlesResponse:
        return self._run(self._client.list_policy_bundles(*args, **kwargs))


__all__ = [
    "BillingClient",
    "BillingError",
    "SyncBillingClient",
]
"""Stew Gateway entitlement management gRPC clients."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import grpc
import grpc.aio

from stew.api.v1 import entitlement_model as _ent_model
from stew.api.v1 import entitlement_pb2 as _ent_pb
from stew.api.v1 import entitlement_pb2_grpc as _ent_grpc

from ._discovery.errors import DiscoveryError
from ._discovery.helpers import (
    AioGatewayClientBase,
    MetadataEntry,
    SyncGatewayClientBase,
    wrap_rpc_error,
)

EntitlementError = DiscoveryError


def _coerce_protobuf_message(value: Any, message_type: type[Any]) -> Any:
    if isinstance(value, message_type):
        return value
    if hasattr(value, "to_protobuf"):
        message = value.to_protobuf()
        if isinstance(message, message_type):
            return message
    raise TypeError(f"Expected {message_type.__name__}, got {type(value).__name__}")


def _coerce_plan_feature(
    value: _ent_model.PlanFeature | _ent_pb.PlanFeature,
) -> _ent_pb.PlanFeature:
    return _coerce_protobuf_message(value, _ent_pb.PlanFeature)


def _coerce_plan_quota(
    value: _ent_model.PlanQuota | _ent_pb.PlanQuota,
) -> _ent_pb.PlanQuota:
    return _coerce_protobuf_message(value, _ent_pb.PlanQuota)


class EntitlementClient(AioGatewayClientBase[_ent_grpc.EntitlementServiceStub]):
    """Async gRPC client for stew.api.v1.EntitlementService.

    This client covers the full management surface for plans, subscriptions,
    quota usage, current-entitlement resolution, and plan change workflows.
    Request-body business scope is exposed as scope_business_id to avoid
    conflating it with metadata/header business_id injection.
    """

    def _create_stub(self, channel: grpc.aio.Channel) -> _ent_grpc.EntitlementServiceStub:
        return _ent_grpc.EntitlementServiceStub(channel)

    async def _call(self, coro: Any) -> Any:
        try:
            return await coro
        except grpc.RpcError as exc:
            raise wrap_rpc_error(exc) from exc

    async def create_plan(
        self,
        request: _ent_model.CreatePlanRequest | _ent_pb.CreatePlanRequest | None = None,
        *,
        scope_business_id: str = "",
        name: str = "",
        description: str = "",
        is_active: bool = False,
        sort_order: int = 0,
        features: Sequence[_ent_model.PlanFeature | _ent_pb.PlanFeature] = (),
        quotas: Sequence[_ent_model.PlanQuota | _ent_pb.PlanQuota] = (),
        metadata: dict[str, str] | None = None,
        localized_name: dict[str, str] | None = None,
        localized_description: dict[str, str] | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.EntitlementPlan:
        if request is not None:
            message = _coerce_protobuf_message(request, _ent_pb.CreatePlanRequest)
        else:
            message = _ent_pb.CreatePlanRequest(
                business_id=scope_business_id,
                name=name,
                description=description,
                is_active=is_active,
                sort_order=sort_order,
                metadata=metadata or {},
                localized_name=localized_name or {},
                localized_description=localized_description or {},
            )
            message.features.extend(_coerce_plan_feature(item) for item in features)
            message.quotas.extend(_coerce_plan_quota(item) for item in quotas)

        response = await self._call(
            self._s.CreatePlan(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.EntitlementPlan.from_protobuf(response)

    async def get_plan(
        self,
        request: _ent_model.GetPlanRequest | _ent_pb.GetPlanRequest | None = None,
        *,
        scope_business_id: str = "",
        plan_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.EntitlementPlan:
        message = (
            _coerce_protobuf_message(request, _ent_pb.GetPlanRequest)
            if request is not None
            else _ent_pb.GetPlanRequest(business_id=scope_business_id, plan_id=plan_id)
        )
        response = await self._call(
            self._s.GetPlan(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.EntitlementPlan.from_protobuf(response)

    async def list_plans(
        self,
        request: _ent_model.ListPlansRequest | _ent_pb.ListPlansRequest | None = None,
        *,
        scope_business_id: str = "",
        active_only: bool = False,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.ListPlansResponse:
        message = (
            _coerce_protobuf_message(request, _ent_pb.ListPlansRequest)
            if request is not None
            else _ent_pb.ListPlansRequest(business_id=scope_business_id, active_only=active_only)
        )
        response = await self._call(
            self._s.ListPlans(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.ListPlansResponse.from_protobuf(response)

    async def update_plan(
        self,
        request: _ent_model.UpdatePlanRequest | _ent_pb.UpdatePlanRequest | None = None,
        *,
        scope_business_id: str = "",
        plan_id: str = "",
        name: str = "",
        description: str = "",
        is_active: bool = False,
        sort_order: int = 0,
        features: Sequence[_ent_model.PlanFeature | _ent_pb.PlanFeature] = (),
        quotas: Sequence[_ent_model.PlanQuota | _ent_pb.PlanQuota] = (),
        metadata: dict[str, str] | None = None,
        localized_name: dict[str, str] | None = None,
        localized_description: dict[str, str] | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.EntitlementPlan:
        if request is not None:
            message = _coerce_protobuf_message(request, _ent_pb.UpdatePlanRequest)
        else:
            message = _ent_pb.UpdatePlanRequest(
                business_id=scope_business_id,
                plan_id=plan_id,
                name=name,
                description=description,
                is_active=is_active,
                sort_order=sort_order,
                metadata=metadata or {},
                localized_name=localized_name or {},
                localized_description=localized_description or {},
            )
            message.features.extend(_coerce_plan_feature(item) for item in features)
            message.quotas.extend(_coerce_plan_quota(item) for item in quotas)

        response = await self._call(
            self._s.UpdatePlan(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.EntitlementPlan.from_protobuf(response)

    async def delete_plan(
        self,
        request: _ent_model.DeletePlanRequest | _ent_pb.DeletePlanRequest | None = None,
        *,
        scope_business_id: str = "",
        plan_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> None:
        message = (
            _coerce_protobuf_message(request, _ent_pb.DeletePlanRequest)
            if request is not None
            else _ent_pb.DeletePlanRequest(business_id=scope_business_id, plan_id=plan_id)
        )
        await self._call(
            self._s.DeletePlan(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )

    async def upsert_plan_feature(
        self,
        request: _ent_model.UpsertPlanFeatureRequest | _ent_pb.UpsertPlanFeatureRequest | None = None,
        *,
        scope_business_id: str = "",
        plan_id: str = "",
        feature: _ent_model.PlanFeature | _ent_pb.PlanFeature | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.EntitlementPlan:
        if request is not None:
            message = _coerce_protobuf_message(request, _ent_pb.UpsertPlanFeatureRequest)
        else:
            message = _ent_pb.UpsertPlanFeatureRequest(
                business_id=scope_business_id,
                plan_id=plan_id,
            )
            if feature is not None:
                message.feature.CopyFrom(_coerce_plan_feature(feature))

        response = await self._call(
            self._s.UpsertPlanFeature(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.EntitlementPlan.from_protobuf(response)

    async def delete_plan_feature(
        self,
        request: _ent_model.DeletePlanFeatureRequest | _ent_pb.DeletePlanFeatureRequest | None = None,
        *,
        scope_business_id: str = "",
        plan_id: str = "",
        feature_key: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.EntitlementPlan:
        message = (
            _coerce_protobuf_message(request, _ent_pb.DeletePlanFeatureRequest)
            if request is not None
            else _ent_pb.DeletePlanFeatureRequest(
                business_id=scope_business_id,
                plan_id=plan_id,
                feature_key=feature_key,
            )
        )
        response = await self._call(
            self._s.DeletePlanFeature(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.EntitlementPlan.from_protobuf(response)

    async def upsert_plan_quota(
        self,
        request: _ent_model.UpsertPlanQuotaRequest | _ent_pb.UpsertPlanQuotaRequest | None = None,
        *,
        scope_business_id: str = "",
        plan_id: str = "",
        quota: _ent_model.PlanQuota | _ent_pb.PlanQuota | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.EntitlementPlan:
        if request is not None:
            message = _coerce_protobuf_message(request, _ent_pb.UpsertPlanQuotaRequest)
        else:
            message = _ent_pb.UpsertPlanQuotaRequest(
                business_id=scope_business_id,
                plan_id=plan_id,
            )
            if quota is not None:
                message.quota.CopyFrom(_coerce_plan_quota(quota))

        response = await self._call(
            self._s.UpsertPlanQuota(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.EntitlementPlan.from_protobuf(response)

    async def delete_plan_quota(
        self,
        request: _ent_model.DeletePlanQuotaRequest | _ent_pb.DeletePlanQuotaRequest | None = None,
        *,
        scope_business_id: str = "",
        plan_id: str = "",
        quota_key: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.EntitlementPlan:
        message = (
            _coerce_protobuf_message(request, _ent_pb.DeletePlanQuotaRequest)
            if request is not None
            else _ent_pb.DeletePlanQuotaRequest(
                business_id=scope_business_id,
                plan_id=plan_id,
                quota_key=quota_key,
            )
        )
        response = await self._call(
            self._s.DeletePlanQuota(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.EntitlementPlan.from_protobuf(response)

    async def create_subscription(
        self,
        request: _ent_model.CreateSubscriptionRequest | _ent_pb.CreateSubscriptionRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        subject_type: int = 0,
        plan_id: str = "",
        billing_cycle: str = "",
        current_period_start: int = 0,
        current_period_end: int = 0,
        metadata: dict[str, str] | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.Subscription:
        message = (
            _coerce_protobuf_message(request, _ent_pb.CreateSubscriptionRequest)
            if request is not None
            else _ent_pb.CreateSubscriptionRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                subject_type=subject_type,
                plan_id=plan_id,
                billing_cycle=billing_cycle,
                current_period_start=current_period_start,
                current_period_end=current_period_end,
                metadata=metadata or {},
            )
        )
        response = await self._call(
            self._s.CreateSubscription(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.Subscription.from_protobuf(response)

    async def get_subscription(
        self,
        request: _ent_model.GetSubscriptionRequest | _ent_pb.GetSubscriptionRequest | None = None,
        *,
        scope_business_id: str = "",
        subscription_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.Subscription:
        message = (
            _coerce_protobuf_message(request, _ent_pb.GetSubscriptionRequest)
            if request is not None
            else _ent_pb.GetSubscriptionRequest(
                business_id=scope_business_id,
                subscription_id=subscription_id,
            )
        )
        response = await self._call(
            self._s.GetSubscription(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.Subscription.from_protobuf(response)

    async def get_subscription_by_subject(
        self,
        request: _ent_model.GetSubscriptionBySubjectRequest
        | _ent_pb.GetSubscriptionBySubjectRequest
        | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.Subscription:
        message = (
            _coerce_protobuf_message(request, _ent_pb.GetSubscriptionBySubjectRequest)
            if request is not None
            else _ent_pb.GetSubscriptionBySubjectRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
            )
        )
        response = await self._call(
            self._s.GetSubscriptionBySubject(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.Subscription.from_protobuf(response)

    async def update_subscription(
        self,
        request: _ent_model.UpdateSubscriptionRequest | _ent_pb.UpdateSubscriptionRequest | None = None,
        *,
        scope_business_id: str = "",
        subscription_id: str = "",
        plan_id: str = "",
        status: str = "",
        billing_cycle: str = "",
        current_period_start: int = 0,
        current_period_end: int = 0,
        metadata: dict[str, str] | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.Subscription:
        message = (
            _coerce_protobuf_message(request, _ent_pb.UpdateSubscriptionRequest)
            if request is not None
            else _ent_pb.UpdateSubscriptionRequest(
                business_id=scope_business_id,
                subscription_id=subscription_id,
                plan_id=plan_id,
                status=status,
                billing_cycle=billing_cycle,
                current_period_start=current_period_start,
                current_period_end=current_period_end,
                metadata=metadata or {},
            )
        )
        response = await self._call(
            self._s.UpdateSubscription(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.Subscription.from_protobuf(response)

    async def cancel_subscription(
        self,
        request: _ent_model.CancelSubscriptionRequest | _ent_pb.CancelSubscriptionRequest | None = None,
        *,
        scope_business_id: str = "",
        subscription_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.Subscription:
        message = (
            _coerce_protobuf_message(request, _ent_pb.CancelSubscriptionRequest)
            if request is not None
            else _ent_pb.CancelSubscriptionRequest(
                business_id=scope_business_id,
                subscription_id=subscription_id,
            )
        )
        response = await self._call(
            self._s.CancelSubscription(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.Subscription.from_protobuf(response)

    async def delete_subscription(
        self,
        request: _ent_model.DeleteSubscriptionRequest | _ent_pb.DeleteSubscriptionRequest | None = None,
        *,
        scope_business_id: str = "",
        subscription_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> None:
        message = (
            _coerce_protobuf_message(request, _ent_pb.DeleteSubscriptionRequest)
            if request is not None
            else _ent_pb.DeleteSubscriptionRequest(
                business_id=scope_business_id,
                subscription_id=subscription_id,
            )
        )
        await self._call(
            self._s.DeleteSubscription(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )

    async def restore_subscription(
        self,
        request: _ent_model.RestoreSubscriptionRequest | _ent_pb.RestoreSubscriptionRequest | None = None,
        *,
        scope_business_id: str = "",
        subscription_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.Subscription:
        message = (
            _coerce_protobuf_message(request, _ent_pb.RestoreSubscriptionRequest)
            if request is not None
            else _ent_pb.RestoreSubscriptionRequest(
                business_id=scope_business_id,
                subscription_id=subscription_id,
            )
        )
        response = await self._call(
            self._s.RestoreSubscription(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.Subscription.from_protobuf(response)

    async def list_subscriptions(
        self,
        request: _ent_model.ListSubscriptionsRequest | _ent_pb.ListSubscriptionsRequest | None = None,
        *,
        scope_business_id: str = "",
        status: str = "",
        plan_id: str = "",
        page_size: int = 0,
        page_token: str = "",
        include_deleted: bool = False,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.ListSubscriptionsResponse:
        message = (
            _coerce_protobuf_message(request, _ent_pb.ListSubscriptionsRequest)
            if request is not None
            else _ent_pb.ListSubscriptionsRequest(
                business_id=scope_business_id,
                status=status,
                plan_id=plan_id,
                page_size=page_size,
                page_token=page_token,
                include_deleted=include_deleted,
            )
        )
        response = await self._call(
            self._s.ListSubscriptions(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.ListSubscriptionsResponse.from_protobuf(response)

    async def admin_renew_subscriptions(
        self,
        request: _ent_model.RenewSubscriptionsRequest | _ent_pb.RenewSubscriptionsRequest | None = None,
        *,
        subscription_ids: Sequence[str] = (),
        horizon_seconds: int = 0,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.RenewSubscriptionsResponse:
        message = (
            _coerce_protobuf_message(request, _ent_pb.RenewSubscriptionsRequest)
            if request is not None
            else _ent_pb.RenewSubscriptionsRequest(
                subscription_ids=list(subscription_ids),
                horizon_seconds=horizon_seconds,
            )
        )
        response = await self._call(
            self._s.AdminRenewSubscriptions(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.RenewSubscriptionsResponse.from_protobuf(response)

    async def internal_renew_subscriptions(
        self,
        request: _ent_model.RenewSubscriptionsRequest | _ent_pb.RenewSubscriptionsRequest | None = None,
        *,
        subscription_ids: Sequence[str] = (),
        horizon_seconds: int = 0,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.RenewSubscriptionsResponse:
        message = (
            _coerce_protobuf_message(request, _ent_pb.RenewSubscriptionsRequest)
            if request is not None
            else _ent_pb.RenewSubscriptionsRequest(
                subscription_ids=list(subscription_ids),
                horizon_seconds=horizon_seconds,
            )
        )
        response = await self._call(
            self._s.InternalRenewSubscriptions(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.RenewSubscriptionsResponse.from_protobuf(response)

    async def get_quota_usage(
        self,
        request: _ent_model.GetQuotaUsageRequest | _ent_pb.GetQuotaUsageRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        quota_key: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.QuotaUsage:
        message = (
            _coerce_protobuf_message(request, _ent_pb.GetQuotaUsageRequest)
            if request is not None
            else _ent_pb.GetQuotaUsageRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                quota_key=quota_key,
            )
        )
        response = await self._call(
            self._s.GetQuotaUsage(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.QuotaUsage.from_protobuf(response)

    async def increment_quota(
        self,
        request: _ent_model.IncrementQuotaRequest | _ent_pb.IncrementQuotaRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        quota_key: str = "",
        delta: int = 0,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.QuotaUsage:
        message = (
            _coerce_protobuf_message(request, _ent_pb.IncrementQuotaRequest)
            if request is not None
            else _ent_pb.IncrementQuotaRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                quota_key=quota_key,
                delta=delta,
            )
        )
        response = await self._call(
            self._s.IncrementQuota(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.QuotaUsage.from_protobuf(response)

    async def check_quota(
        self,
        request: _ent_model.CheckQuotaRequest | _ent_pb.CheckQuotaRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        quota_key: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.CheckQuotaResponse:
        message = (
            _coerce_protobuf_message(request, _ent_pb.CheckQuotaRequest)
            if request is not None
            else _ent_pb.CheckQuotaRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                quota_key=quota_key,
            )
        )
        response = await self._call(
            self._s.CheckQuota(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.CheckQuotaResponse.from_protobuf(response)

    async def get_my_entitlement(
        self,
        request: _ent_model.GetMyEntitlementRequest | _ent_pb.GetMyEntitlementRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.ResolvedEntitlementResponse:
        message = (
            _coerce_protobuf_message(request, _ent_pb.GetMyEntitlementRequest)
            if request is not None
            else _ent_pb.GetMyEntitlementRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
            )
        )
        response = await self._call(
            self._s.GetMyEntitlement(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.ResolvedEntitlementResponse.from_protobuf(response)

    async def check_feature(
        self,
        request: _ent_model.CheckFeatureRequest | _ent_pb.CheckFeatureRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        feature_key: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.CheckFeatureResponse:
        message = (
            _coerce_protobuf_message(request, _ent_pb.CheckFeatureRequest)
            if request is not None
            else _ent_pb.CheckFeatureRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                feature_key=feature_key,
            )
        )
        response = await self._call(
            self._s.CheckFeature(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.CheckFeatureResponse.from_protobuf(response)

    async def change_plan(
        self,
        request: _ent_model.ChangePlanRequest | _ent_pb.ChangePlanRequest | None = None,
        *,
        scope_business_id: str = "",
        subscription_id: str = "",
        subject_id: str = "",
        new_plan_id: str = "",
        change_mode: str = "",
        reset_quota: bool = False,
        metadata: dict[str, str] | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.ChangePlanResponse:
        message = (
            _coerce_protobuf_message(request, _ent_pb.ChangePlanRequest)
            if request is not None
            else _ent_pb.ChangePlanRequest(
                business_id=scope_business_id,
                subscription_id=subscription_id,
                subject_id=subject_id,
                new_plan_id=new_plan_id,
                change_mode=change_mode,
                reset_quota=reset_quota,
                metadata=metadata or {},
            )
        )
        response = await self._call(
            self._s.ChangePlan(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.ChangePlanResponse.from_protobuf(response)

    async def list_plan_changes(
        self,
        request: _ent_model.ListPlanChangesRequest | _ent_pb.ListPlanChangesRequest | None = None,
        *,
        scope_business_id: str = "",
        subscription_id: str = "",
        subject_id: str = "",
        page_size: int = 0,
        page_token: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.ListPlanChangesResponse:
        message = (
            _coerce_protobuf_message(request, _ent_pb.ListPlanChangesRequest)
            if request is not None
            else _ent_pb.ListPlanChangesRequest(
                business_id=scope_business_id,
                subscription_id=subscription_id,
                subject_id=subject_id,
                page_size=page_size,
                page_token=page_token,
            )
        )
        response = await self._call(
            self._s.ListPlanChanges(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.ListPlanChangesResponse.from_protobuf(response)

    async def cancel_plan_change(
        self,
        request: _ent_model.CancelPlanChangeRequest | _ent_pb.CancelPlanChangeRequest | None = None,
        *,
        scope_business_id: str = "",
        change_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _ent_model.PlanChangeRecord:
        message = (
            _coerce_protobuf_message(request, _ent_pb.CancelPlanChangeRequest)
            if request is not None
            else _ent_pb.CancelPlanChangeRequest(
                business_id=scope_business_id,
                change_id=change_id,
            )
        )
        response = await self._call(
            self._s.CancelPlanChange(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _ent_model.PlanChangeRecord.from_protobuf(response)


class SyncEntitlementClient(SyncGatewayClientBase[EntitlementClient]):
    """Synchronous facade over :class:`EntitlementClient`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(EntitlementClient, *args, **kwargs)

    def create_plan(self, *args: Any, **kwargs: Any) -> _ent_model.EntitlementPlan:
        return self._run(self._client.create_plan(*args, **kwargs))

    def get_plan(self, *args: Any, **kwargs: Any) -> _ent_model.EntitlementPlan:
        return self._run(self._client.get_plan(*args, **kwargs))

    def list_plans(self, *args: Any, **kwargs: Any) -> _ent_model.ListPlansResponse:
        return self._run(self._client.list_plans(*args, **kwargs))

    def update_plan(self, *args: Any, **kwargs: Any) -> _ent_model.EntitlementPlan:
        return self._run(self._client.update_plan(*args, **kwargs))

    def delete_plan(self, *args: Any, **kwargs: Any) -> None:
        self._run(self._client.delete_plan(*args, **kwargs))

    def upsert_plan_feature(self, *args: Any, **kwargs: Any) -> _ent_model.EntitlementPlan:
        return self._run(self._client.upsert_plan_feature(*args, **kwargs))

    def delete_plan_feature(self, *args: Any, **kwargs: Any) -> _ent_model.EntitlementPlan:
        return self._run(self._client.delete_plan_feature(*args, **kwargs))

    def upsert_plan_quota(self, *args: Any, **kwargs: Any) -> _ent_model.EntitlementPlan:
        return self._run(self._client.upsert_plan_quota(*args, **kwargs))

    def delete_plan_quota(self, *args: Any, **kwargs: Any) -> _ent_model.EntitlementPlan:
        return self._run(self._client.delete_plan_quota(*args, **kwargs))

    def create_subscription(self, *args: Any, **kwargs: Any) -> _ent_model.Subscription:
        return self._run(self._client.create_subscription(*args, **kwargs))

    def get_subscription(self, *args: Any, **kwargs: Any) -> _ent_model.Subscription:
        return self._run(self._client.get_subscription(*args, **kwargs))

    def get_subscription_by_subject(self, *args: Any, **kwargs: Any) -> _ent_model.Subscription:
        return self._run(self._client.get_subscription_by_subject(*args, **kwargs))

    def update_subscription(self, *args: Any, **kwargs: Any) -> _ent_model.Subscription:
        return self._run(self._client.update_subscription(*args, **kwargs))

    def cancel_subscription(self, *args: Any, **kwargs: Any) -> _ent_model.Subscription:
        return self._run(self._client.cancel_subscription(*args, **kwargs))

    def delete_subscription(self, *args: Any, **kwargs: Any) -> None:
        self._run(self._client.delete_subscription(*args, **kwargs))

    def restore_subscription(self, *args: Any, **kwargs: Any) -> _ent_model.Subscription:
        return self._run(self._client.restore_subscription(*args, **kwargs))

    def list_subscriptions(self, *args: Any, **kwargs: Any) -> _ent_model.ListSubscriptionsResponse:
        return self._run(self._client.list_subscriptions(*args, **kwargs))

    def admin_renew_subscriptions(
        self, *args: Any, **kwargs: Any
    ) -> _ent_model.RenewSubscriptionsResponse:
        return self._run(self._client.admin_renew_subscriptions(*args, **kwargs))

    def internal_renew_subscriptions(
        self, *args: Any, **kwargs: Any
    ) -> _ent_model.RenewSubscriptionsResponse:
        return self._run(self._client.internal_renew_subscriptions(*args, **kwargs))

    def get_quota_usage(self, *args: Any, **kwargs: Any) -> _ent_model.QuotaUsage:
        return self._run(self._client.get_quota_usage(*args, **kwargs))

    def increment_quota(self, *args: Any, **kwargs: Any) -> _ent_model.QuotaUsage:
        return self._run(self._client.increment_quota(*args, **kwargs))

    def check_quota(self, *args: Any, **kwargs: Any) -> _ent_model.CheckQuotaResponse:
        return self._run(self._client.check_quota(*args, **kwargs))

    def get_my_entitlement(
        self, *args: Any, **kwargs: Any
    ) -> _ent_model.ResolvedEntitlementResponse:
        return self._run(self._client.get_my_entitlement(*args, **kwargs))

    def check_feature(self, *args: Any, **kwargs: Any) -> _ent_model.CheckFeatureResponse:
        return self._run(self._client.check_feature(*args, **kwargs))

    def change_plan(self, *args: Any, **kwargs: Any) -> _ent_model.ChangePlanResponse:
        return self._run(self._client.change_plan(*args, **kwargs))

    def list_plan_changes(
        self, *args: Any, **kwargs: Any
    ) -> _ent_model.ListPlanChangesResponse:
        return self._run(self._client.list_plan_changes(*args, **kwargs))

    def cancel_plan_change(self, *args: Any, **kwargs: Any) -> _ent_model.PlanChangeRecord:
        return self._run(self._client.cancel_plan_change(*args, **kwargs))


__all__ = [
    "EntitlementClient",
    "EntitlementError",
    "SyncEntitlementClient",
]
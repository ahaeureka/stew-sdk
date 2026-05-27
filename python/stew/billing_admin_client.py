"""Stew Gateway billing admin gRPC clients."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from google.protobuf import empty_pb2 as _empty_pb2
import grpc.aio

from stew.api.v1 import billing_admin_pb2_grpc as _bill_admin_grpc

from ._billing_client_shared import (
    BillingAioClientBase,
    BillingError,
    _bill_model,
    _bill_pb,
    coerce_billing_policy_artifact_type,
    coerce_protobuf_message,
    enum_value,
)
from ._discovery.helpers import MetadataEntry, SyncGatewayClientBase


class BillingAdminClient(
    BillingAioClientBase[_bill_admin_grpc.BillingAdminServiceStub]
):
    """Async gRPC client for stew.api.v1.BillingAdminService."""

    def _create_stub(
        self,
        channel: grpc.aio.Channel,
    ) -> _bill_admin_grpc.BillingAdminServiceStub:
        return _bill_admin_grpc.BillingAdminServiceStub(channel)

    async def grant_credits(
        self,
        request: _bill_model.GrantCreditsRequest
        | _bill_pb.GrantCreditsRequest
        | None = None,
        *,
        scope_business_id: str = "",
        user_id: str = "",
        subject_id: str = "",
        subject_type: _bill_model.BillingSubjectType
        | int = _bill_model.BillingSubjectType(0),
        credit_type: str = "",
        amount: int = 0,
        expires_at_epoch_seconds: int = 0,
        idempotency_key: str = "",
        metadata: dict[str, str] | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.CreditGrant:
        message = (
            coerce_protobuf_message(request, _bill_pb.GrantCreditsRequest)
            if request is not None
            else _bill_pb.GrantCreditsRequest(
                business_id=scope_business_id,
                user_id=user_id,
                subject_id=subject_id,
                subject_type=enum_value(subject_type),
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
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.CreditGrant.from_protobuf(response)

    async def query_reservations(
        self,
        request: _bill_model.QueryBillingReservationsRequest
        | _bill_pb.QueryBillingReservationsRequest
        | None = None,
        *,
        scope_business_id: str = "",
        request_id: str = "",
        authorization_id: str = "",
        subject_id: str = "",
        subject_type: _bill_model.BillingSubjectType
        | int = _bill_model.BillingSubjectType(0),
        user_id: str = "",
        status: _bill_model.BillingReservationStatus
        | int = _bill_model.BillingReservationStatus(0),
        start_time_epoch_seconds: int = 0,
        end_time_epoch_seconds: int = 0,
        page_size: int = 0,
        page_token: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.QueryBillingReservationsResponse:
        message = (
            coerce_protobuf_message(request, _bill_pb.QueryBillingReservationsRequest)
            if request is not None
            else _bill_pb.QueryBillingReservationsRequest(
                business_id=scope_business_id,
                request_id=request_id,
                authorization_id=authorization_id,
                subject_id=subject_id,
                subject_type=enum_value(subject_type),
                user_id=user_id,
                status=enum_value(status),
                start_time_epoch_seconds=start_time_epoch_seconds,
                end_time_epoch_seconds=end_time_epoch_seconds,
                page_size=page_size,
                page_token=page_token,
            )
        )
        response = await self._call(
            self._s.QueryReservations(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.QueryBillingReservationsResponse.from_protobuf(response)

    async def get_reservation(
        self,
        request: _bill_model.GetBillingReservationRequest
        | _bill_pb.GetBillingReservationRequest
        | None = None,
        *,
        scope_business_id: str = "",
        authorization_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingReservation:
        message = (
            coerce_protobuf_message(request, _bill_pb.GetBillingReservationRequest)
            if request is not None
            else _bill_pb.GetBillingReservationRequest(
                business_id=scope_business_id,
                authorization_id=authorization_id,
            )
        )
        response = await self._call(
            self._s.GetReservation(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingReservation.from_protobuf(response)

    async def manual_reconcile(
        self,
        request: _bill_model.ManualReconcileRequest
        | _bill_pb.ManualReconcileRequest
        | None = None,
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
            coerce_protobuf_message(request, _bill_pb.ManualReconcileRequest)
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
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.ManualReconcileResponse.from_protobuf(response)

    async def create_policy(
        self,
        request: _bill_model.CreateBillingPolicyRequest
        | _bill_pb.CreateBillingPolicyRequest
        | None = None,
        *,
        scope_business_id: str = "",
        display_name: str = "",
        description: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingPolicy:
        message = (
            coerce_protobuf_message(request, _bill_pb.CreateBillingPolicyRequest)
            if request is not None
            else _bill_pb.CreateBillingPolicyRequest(
                business_id=scope_business_id,
                display_name=display_name,
                description=description,
            )
        )
        response = await self._call(
            self._s.CreatePolicy(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingPolicy.from_protobuf(response)

    async def get_policy(
        self,
        request: _bill_model.GetBillingPolicyRequest
        | _bill_pb.GetBillingPolicyRequest
        | None = None,
        *,
        scope_business_id: str = "",
        policy_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingPolicy:
        message = (
            coerce_protobuf_message(request, _bill_pb.GetBillingPolicyRequest)
            if request is not None
            else _bill_pb.GetBillingPolicyRequest(
                business_id=scope_business_id,
                policy_id=policy_id,
            )
        )
        response = await self._call(
            self._s.GetPolicy(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingPolicy.from_protobuf(response)

    async def list_policies(
        self,
        request: _bill_model.ListBillingPoliciesRequest
        | _bill_pb.ListBillingPoliciesRequest
        | None = None,
        *,
        scope_business_id: str = "",
        include_archived: bool = False,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.ListBillingPoliciesResponse:
        message = (
            coerce_protobuf_message(request, _bill_pb.ListBillingPoliciesRequest)
            if request is not None
            else _bill_pb.ListBillingPoliciesRequest(
                business_id=scope_business_id,
                include_archived=include_archived,
            )
        )
        response = await self._call(
            self._s.ListPolicies(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.ListBillingPoliciesResponse.from_protobuf(response)

    async def update_policy(
        self,
        request: _bill_model.UpdateBillingPolicyRequest
        | _bill_pb.UpdateBillingPolicyRequest
        | None = None,
        *,
        scope_business_id: str = "",
        policy_id: str = "",
        display_name: str | None = None,
        description: str | None = None,
        status: str | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingPolicy:
        if request is not None:
            message = coerce_protobuf_message(
                request, _bill_pb.UpdateBillingPolicyRequest
            )
        else:
            message = _bill_pb.UpdateBillingPolicyRequest(
                business_id=scope_business_id,
                policy_id=policy_id,
            )
            if display_name is not None:
                message.display_name = display_name
            if description is not None:
                message.description = description
            if status is not None:
                message.status = status

        response = await self._call(
            self._s.UpdatePolicy(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingPolicy.from_protobuf(response)

    async def archive_policy(
        self,
        request: _bill_model.ArchiveBillingPolicyRequest
        | _bill_pb.ArchiveBillingPolicyRequest
        | None = None,
        *,
        scope_business_id: str = "",
        policy_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingPolicy:
        message = (
            coerce_protobuf_message(request, _bill_pb.ArchiveBillingPolicyRequest)
            if request is not None
            else _bill_pb.ArchiveBillingPolicyRequest(
                business_id=scope_business_id,
                policy_id=policy_id,
            )
        )
        response = await self._call(
            self._s.ArchivePolicy(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingPolicy.from_protobuf(response)

    async def delete_policy(
        self,
        request: _bill_model.DeleteBillingPolicyRequest
        | _bill_pb.DeleteBillingPolicyRequest
        | None = None,
        *,
        scope_business_id: str = "",
        policy_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _empty_pb2.Empty:
        message = (
            coerce_protobuf_message(request, _bill_pb.DeleteBillingPolicyRequest)
            if request is not None
            else _bill_pb.DeleteBillingPolicyRequest(
                business_id=scope_business_id,
                policy_id=policy_id,
            )
        )
        return await self._call(
            self._s.DeletePolicy(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )

    async def create_policy_artifact(
        self,
        request: _bill_model.CreateBillingPolicyArtifactRequest
        | _bill_pb.CreateBillingPolicyArtifactRequest
        | None = None,
        *,
        scope_business_id: str = "",
        artifact_type: _bill_model.BillingPolicyArtifactType
        | int = _bill_model.BillingPolicyArtifactType(0),
        artifact_version: str = "",
        content: dict[str, Any] | None = None,
        policy_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingPolicyArtifact:
        message = (
            coerce_protobuf_message(
                request, _bill_pb.CreateBillingPolicyArtifactRequest
            )
            if request is not None
            else _bill_pb.CreateBillingPolicyArtifactRequest(
                business_id=scope_business_id,
                artifact_type=coerce_billing_policy_artifact_type(artifact_type),
                artifact_version=artifact_version,
                content=content or {},
                policy_id=policy_id,
            )
        )
        response = await self._call(
            self._s.CreatePolicyArtifact(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
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
            coerce_protobuf_message(request, _bill_pb.GetBillingPolicyArtifactRequest)
            if request is not None
            else _bill_pb.GetBillingPolicyArtifactRequest(artifact_id=artifact_id)
        )
        response = await self._call(
            self._s.GetPolicyArtifact(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
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
        artifact_type: _bill_model.BillingPolicyArtifactType
        | int = _bill_model.BillingPolicyArtifactType(0),
        policy_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.ListBillingPolicyArtifactsResponse:
        message = (
            coerce_protobuf_message(request, _bill_pb.ListBillingPolicyArtifactsRequest)
            if request is not None
            else _bill_pb.ListBillingPolicyArtifactsRequest(
                business_id=scope_business_id,
                artifact_type=coerce_billing_policy_artifact_type(artifact_type),
                policy_id=policy_id,
            )
        )
        response = await self._call(
            self._s.ListPolicyArtifacts(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
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
            coerce_protobuf_message(request, _bill_pb.PublishBillingPolicyBundleRequest)
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
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
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
            coerce_protobuf_message(request, _bill_pb.GetBillingPolicyBundleRequest)
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
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
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
            coerce_protobuf_message(request, _bill_pb.ListBillingPolicyBundlesRequest)
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
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.ListBillingPolicyBundlesResponse.from_protobuf(response)


class SyncBillingAdminClient(SyncGatewayClientBase[BillingAdminClient]):
    """Synchronous facade over :class:`BillingAdminClient`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(BillingAdminClient, *args, **kwargs)

    def grant_credits(self, *args: Any, **kwargs: Any) -> _bill_model.CreditGrant:
        return self._run(self._client.grant_credits(*args, **kwargs))

    def query_reservations(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.QueryBillingReservationsResponse:
        return self._run(self._client.query_reservations(*args, **kwargs))

    def get_reservation(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.BillingReservation:
        return self._run(self._client.get_reservation(*args, **kwargs))

    def manual_reconcile(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.ManualReconcileResponse:
        return self._run(self._client.manual_reconcile(*args, **kwargs))

    def create_policy(self, *args: Any, **kwargs: Any) -> _bill_model.BillingPolicy:
        return self._run(self._client.create_policy(*args, **kwargs))

    def get_policy(self, *args: Any, **kwargs: Any) -> _bill_model.BillingPolicy:
        return self._run(self._client.get_policy(*args, **kwargs))

    def list_policies(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.ListBillingPoliciesResponse:
        return self._run(self._client.list_policies(*args, **kwargs))

    def update_policy(self, *args: Any, **kwargs: Any) -> _bill_model.BillingPolicy:
        return self._run(self._client.update_policy(*args, **kwargs))

    def archive_policy(self, *args: Any, **kwargs: Any) -> _bill_model.BillingPolicy:
        return self._run(self._client.archive_policy(*args, **kwargs))

    def delete_policy(self, *args: Any, **kwargs: Any) -> _empty_pb2.Empty:
        return self._run(self._client.delete_policy(*args, **kwargs))

    def create_policy_artifact(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.BillingPolicyArtifact:
        return self._run(self._client.create_policy_artifact(*args, **kwargs))

    def get_policy_artifact(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.BillingPolicyArtifact:
        return self._run(self._client.get_policy_artifact(*args, **kwargs))

    def list_policy_artifacts(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.ListBillingPolicyArtifactsResponse:
        return self._run(self._client.list_policy_artifacts(*args, **kwargs))

    def publish_policy_bundle(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.BillingPolicyBundle:
        return self._run(self._client.publish_policy_bundle(*args, **kwargs))

    def get_policy_bundle(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.BillingPolicyBundle:
        return self._run(self._client.get_policy_bundle(*args, **kwargs))

    def list_policy_bundles(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.ListBillingPolicyBundlesResponse:
        return self._run(self._client.list_policy_bundles(*args, **kwargs))


__all__ = [
    "BillingAdminClient",
    "BillingError",
    "SyncBillingAdminClient",
]

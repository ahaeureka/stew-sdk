"""Stew Gateway billing internal gRPC clients."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import grpc
import grpc.aio

from stew.api.v1 import billing_internal_pb2_grpc as _bill_internal_grpc
from stew.api.v1 import billing_report_ingress_pb2_grpc as _bill_report_grpc

from ._billing_client_shared import (
    BillingAioClientBase,
    BillingError,
    _bill_model,
    _bill_pb,
    coerce_authorization_context,
    coerce_billing_report,
    coerce_protobuf_message,
)
from ._discovery.helpers import MetadataEntry, SyncGatewayClientBase


class BillingInternalClient(
    BillingAioClientBase[_bill_internal_grpc.BillingInternalServiceStub]
):
    """Async gRPC client for stew.api.v1.BillingInternalService."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._report_ingress_stub: (
            _bill_report_grpc.BillingReportIngressInternalServiceStub | None
        ) = None

    def _create_stub(
        self,
        channel: grpc.aio.Channel,
    ) -> _bill_internal_grpc.BillingInternalServiceStub:
        return _bill_internal_grpc.BillingInternalServiceStub(channel)

    async def connect(self) -> None:
        await super().connect()
        if self._channel is None:
            raise RuntimeError("Client channel was not initialized")
        self._report_ingress_stub = (
            _bill_report_grpc.BillingReportIngressInternalServiceStub(self._channel)
        )

    async def close(self) -> None:
        self._report_ingress_stub = None
        await super().close()

    @property
    def _report_s(self) -> _bill_report_grpc.BillingReportIngressInternalServiceStub:
        if self._report_ingress_stub is None:
            raise RuntimeError(
                "Client is not connected. Call connect() or use async with."
            )
        return self._report_ingress_stub

    async def estimate_charge(
        self,
        request: _bill_model.EstimateChargeRequest
        | _bill_pb.EstimateChargeRequest
        | None = None,
        *,
        context: _bill_model.AuthorizationContext
        | _bill_pb.AuthorizationContext
        | None = None,
        request_factors: dict[str, Any] | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.EstimateChargeResponse:
        if request is not None:
            message = coerce_protobuf_message(request, _bill_pb.EstimateChargeRequest)
        else:
            message = _bill_pb.EstimateChargeRequest()
            if context is not None:
                message.context.CopyFrom(coerce_authorization_context(context))
            if request_factors is not None:
                message.request_factors.update(request_factors)

        response = await self._call(
            self._s.EstimateCharge(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.EstimateChargeResponse.from_protobuf(response)

    async def authorize(
        self,
        request: _bill_model.AuthorizeRequest | _bill_pb.AuthorizeRequest | None = None,
        *,
        context: _bill_model.AuthorizationContext
        | _bill_pb.AuthorizationContext
        | None = None,
        estimated_points: int = 0,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingAuthorizationResponse:
        if request is not None:
            message = coerce_protobuf_message(request, _bill_pb.AuthorizeRequest)
        else:
            message = _bill_pb.AuthorizeRequest(estimated_points=estimated_points)
            if context is not None:
                message.context.CopyFrom(coerce_authorization_context(context))

        response = await self._call(
            self._s.Authorize(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingAuthorizationResponse.from_protobuf(response)

    async def finalize(
        self,
        request: _bill_model.FinalizeRequest | _bill_pb.FinalizeRequest | None = None,
        *,
        context: _bill_model.AuthorizationContext
        | _bill_pb.AuthorizationContext
        | None = None,
        report: _bill_model.BillingReport | _bill_pb.BillingReport | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.SettlementDecision:
        if request is not None:
            message = coerce_protobuf_message(request, _bill_pb.FinalizeRequest)
        else:
            message = _bill_pb.FinalizeRequest()
            if context is not None:
                message.context.CopyFrom(coerce_authorization_context(context))
            if report is not None:
                message.report.CopyFrom(coerce_billing_report(report))

        response = await self._call(
            self._s.Finalize(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
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
            coerce_protobuf_message(request, _bill_pb.ReleaseRequest)
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
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
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
            coerce_protobuf_message(request, _bill_pb.RefundRequest)
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
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.SettlementDecision.from_protobuf(response)

    async def submit_billing_report(
        self,
        request: _bill_model.SubmitBillingReportRequest
        | _bill_pb.SubmitBillingReportRequest
        | None = None,
        *,
        report: _bill_model.BillingReport | _bill_pb.BillingReport | None = None,
        delivery_request_id: str = "",
        source_service: str = "",
        labels: dict[str, str] | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.SubmitBillingReportResponse:
        if request is not None:
            message = coerce_protobuf_message(
                request, _bill_pb.SubmitBillingReportRequest
            )
        else:
            message = _bill_pb.SubmitBillingReportRequest(
                delivery_request_id=delivery_request_id,
                source_service=source_service,
                labels=labels or {},
            )
            if report is not None:
                message.report.CopyFrom(coerce_billing_report(report))

        response = await self._call(
            self._report_s.SubmitBillingReport(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.SubmitBillingReportResponse.from_protobuf(response)


class SyncBillingInternalClient(SyncGatewayClientBase[BillingInternalClient]):
    """Synchronous facade over :class:`BillingInternalClient`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(BillingInternalClient, *args, **kwargs)

    def estimate_charge(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.EstimateChargeResponse:
        return self._run(self._client.estimate_charge(*args, **kwargs))

    def authorize(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.BillingAuthorizationResponse:
        return self._run(self._client.authorize(*args, **kwargs))

    def finalize(self, *args: Any, **kwargs: Any) -> _bill_model.SettlementDecision:
        return self._run(self._client.finalize(*args, **kwargs))

    def release(self, *args: Any, **kwargs: Any) -> _bill_model.SettlementDecision:
        return self._run(self._client.release(*args, **kwargs))

    def refund(self, *args: Any, **kwargs: Any) -> _bill_model.SettlementDecision:
        return self._run(self._client.refund(*args, **kwargs))

    def submit_billing_report(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.SubmitBillingReportResponse:
        return self._run(self._client.submit_billing_report(*args, **kwargs))


__all__ = [
    "BillingError",
    "BillingInternalClient",
    "SyncBillingInternalClient",
]

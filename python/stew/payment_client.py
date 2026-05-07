"""Stew Gateway payment gRPC clients."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import grpc
import grpc.aio

from stew.api.v1 import payment_model as _payment_model
from stew.api.v1 import payment_pb2 as _payment_pb
from stew.api.v1 import payment_pb2_grpc as _payment_grpc

from ._discovery.errors import DiscoveryError
from ._discovery.helpers import (
    AioGatewayClientBase,
    MetadataEntry,
    SyncGatewayClientBase,
    wrap_rpc_error,
)

PaymentError = DiscoveryError


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


def _coerce_checkout_line_item(
    value: _payment_model.CheckoutLineItem | _payment_pb.CheckoutLineItem,
) -> _payment_pb.CheckoutLineItem:
    return _coerce_protobuf_message(value, _payment_pb.CheckoutLineItem)


class PaymentClient(AioGatewayClientBase[_payment_grpc.PaymentGatewayServiceStub]):
    """Async gRPC client for stew.api.v1.PaymentGatewayService."""

    def _create_stub(
        self,
        channel: grpc.aio.Channel,
    ) -> _payment_grpc.PaymentGatewayServiceStub:
        return _payment_grpc.PaymentGatewayServiceStub(channel)

    async def _call(self, coro: Any) -> Any:
        try:
            return await coro
        except grpc.RpcError as exc:
            raise wrap_rpc_error(exc) from exc

    async def create_checkout(
        self,
        request: _payment_model.CreateCheckoutRequest | _payment_pb.CreateCheckoutRequest | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        provider: _payment_model.PaymentProviderKind | int = _payment_model.PaymentProviderKind(0),
        customer_email: str = "",
        currency: str = "",
        line_items: Sequence[_payment_model.CheckoutLineItem | _payment_pb.CheckoutLineItem] = (),
        billing_interval: _payment_model.PaymentBillingInterval | int = _payment_model.PaymentBillingInterval(0),
        success_url: str = "",
        cancel_url: str = "",
        plan_id: str = "",
        metadata: dict[str, str] | None = None,
        idempotency_key: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _payment_model.CreateCheckoutResponse:
        if request is not None:
            message = _coerce_protobuf_message(request, _payment_pb.CreateCheckoutRequest)
        else:
            message = _payment_pb.CreateCheckoutRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                provider=_enum_value(provider),
                customer_email=customer_email,
                currency=currency,
                billing_interval=_enum_value(billing_interval),
                success_url=success_url,
                cancel_url=cancel_url,
                plan_id=plan_id,
                metadata=metadata or {},
                idempotency_key=idempotency_key,
            )
            message.line_items.extend(_coerce_checkout_line_item(item) for item in line_items)

        response = await self._call(
            self._s.CreateCheckout(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _payment_model.CreateCheckoutResponse.from_protobuf(response)

    async def get_payment_order(
        self,
        request: _payment_model.GetPaymentOrderRequest | _payment_pb.GetPaymentOrderRequest | None = None,
        *,
        order_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _payment_model.PaymentOrderResponse:
        message = (
            _coerce_protobuf_message(request, _payment_pb.GetPaymentOrderRequest)
            if request is not None
            else _payment_pb.GetPaymentOrderRequest(order_id=order_id)
        )
        response = await self._call(
            self._s.GetPaymentOrder(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _payment_model.PaymentOrderResponse.from_protobuf(response)

    async def list_payment_orders(
        self,
        request: _payment_model.ListPaymentOrdersRequest
        | _payment_pb.ListPaymentOrdersRequest
        | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        status: _payment_model.PaymentOrderStatus | int = _payment_model.PaymentOrderStatus(0),
        page_size: int = 0,
        page_token: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _payment_model.ListPaymentOrdersResponse:
        message = (
            _coerce_protobuf_message(request, _payment_pb.ListPaymentOrdersRequest)
            if request is not None
            else _payment_pb.ListPaymentOrdersRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                status=_enum_value(status),
                page_size=page_size,
                page_token=page_token,
            )
        )
        response = await self._call(
            self._s.ListPaymentOrders(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _payment_model.ListPaymentOrdersResponse.from_protobuf(response)

    async def refund_payment(
        self,
        request: _payment_model.RefundPaymentRequest | _payment_pb.RefundPaymentRequest | None = None,
        *,
        order_id: str = "",
        amount_minor: int = 0,
        reason: str = "",
        idempotency_key: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _payment_model.RefundPaymentResponse:
        message = (
            _coerce_protobuf_message(request, _payment_pb.RefundPaymentRequest)
            if request is not None
            else _payment_pb.RefundPaymentRequest(
                order_id=order_id,
                amount_minor=amount_minor,
                reason=reason,
                idempotency_key=idempotency_key,
            )
        )
        response = await self._call(
            self._s.RefundPayment(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _payment_model.RefundPaymentResponse.from_protobuf(response)

    async def submit_refund_request(
        self,
        request: _payment_model.SubmitRefundRequestRequest
        | _payment_pb.SubmitRefundRequestRequest
        | None = None,
        *,
        order_id: str = "",
        amount_minor: int = 0,
        reason: str = "",
        request_channel: str = "",
        requested_by: str = "",
        requested_by_display_name: str = "",
        metadata: dict[str, str] | None = None,
        idempotency_key: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _payment_model.RefundRequestRecord:
        message = (
            _coerce_protobuf_message(request, _payment_pb.SubmitRefundRequestRequest)
            if request is not None
            else _payment_pb.SubmitRefundRequestRequest(
                order_id=order_id,
                amount_minor=amount_minor,
                reason=reason,
                request_channel=request_channel,
                requested_by=requested_by,
                requested_by_display_name=requested_by_display_name,
                metadata=metadata or {},
                idempotency_key=idempotency_key,
            )
        )
        response = await self._call(
            self._s.SubmitRefundRequest(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _payment_model.RefundRequestRecord.from_protobuf(response)

    async def get_refund_request(
        self,
        request: _payment_model.GetRefundRequestRequest
        | _payment_pb.GetRefundRequestRequest
        | None = None,
        *,
        refund_request_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _payment_model.RefundRequestRecord:
        message = (
            _coerce_protobuf_message(request, _payment_pb.GetRefundRequestRequest)
            if request is not None
            else _payment_pb.GetRefundRequestRequest(refund_request_id=refund_request_id)
        )
        response = await self._call(
            self._s.GetRefundRequest(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _payment_model.RefundRequestRecord.from_protobuf(response)

    async def list_refund_review_logs(
        self,
        request: _payment_model.ListRefundReviewLogsRequest
        | _payment_pb.ListRefundReviewLogsRequest
        | None = None,
        *,
        refund_request_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _payment_model.ListRefundReviewLogsResponse:
        message = (
            _coerce_protobuf_message(request, _payment_pb.ListRefundReviewLogsRequest)
            if request is not None
            else _payment_pb.ListRefundReviewLogsRequest(refund_request_id=refund_request_id)
        )
        response = await self._call(
            self._s.ListRefundReviewLogs(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _payment_model.ListRefundReviewLogsResponse.from_protobuf(response)

    async def list_refund_requests(
        self,
        request: _payment_model.ListRefundRequestsRequest
        | _payment_pb.ListRefundRequestsRequest
        | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        order_id: str = "",
        status: _payment_model.RefundRequestStatus | int = _payment_model.RefundRequestStatus(0),
        page_size: int = 0,
        page_token: str = "",
        business_ids: Sequence[str] = (),
        subject_ids: Sequence[str] = (),
        order_ids: Sequence[str] = (),
        statuses: Sequence[_payment_model.RefundRequestStatus | int] = (),
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _payment_model.ListRefundRequestsResponse:
        message = (
            _coerce_protobuf_message(request, _payment_pb.ListRefundRequestsRequest)
            if request is not None
            else _payment_pb.ListRefundRequestsRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                order_id=order_id,
                status=_enum_value(status),
                page_size=page_size,
                page_token=page_token,
                business_ids=list(business_ids),
                subject_ids=list(subject_ids),
                order_ids=list(order_ids),
                statuses=[_enum_value(item) for item in statuses],
            )
        )
        response = await self._call(
            self._s.ListRefundRequests(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _payment_model.ListRefundRequestsResponse.from_protobuf(response)

    async def cancel_refund_request(
        self,
        request: _payment_model.CancelRefundRequestRequest
        | _payment_pb.CancelRefundRequestRequest
        | None = None,
        *,
        refund_request_id: str = "",
        canceled_by: str = "",
        cancel_comment: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _payment_model.RefundRequestRecord:
        message = (
            _coerce_protobuf_message(request, _payment_pb.CancelRefundRequestRequest)
            if request is not None
            else _payment_pb.CancelRefundRequestRequest(
                refund_request_id=refund_request_id,
                canceled_by=canceled_by,
                cancel_comment=cancel_comment,
            )
        )
        response = await self._call(
            self._s.CancelRefundRequest(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _payment_model.RefundRequestRecord.from_protobuf(response)

    async def approve_refund_request(
        self,
        request: _payment_model.ApproveRefundRequestRequest
        | _payment_pb.ApproveRefundRequestRequest
        | None = None,
        *,
        refund_request_id: str = "",
        approved_amount_minor: int = 0,
        reviewer_id: str = "",
        reviewer_display_name: str = "",
        review_comment: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _payment_model.RefundRequestRecord:
        message = (
            _coerce_protobuf_message(request, _payment_pb.ApproveRefundRequestRequest)
            if request is not None
            else _payment_pb.ApproveRefundRequestRequest(
                refund_request_id=refund_request_id,
                approved_amount_minor=approved_amount_minor,
                reviewer_id=reviewer_id,
                reviewer_display_name=reviewer_display_name,
                review_comment=review_comment,
            )
        )
        response = await self._call(
            self._s.ApproveRefundRequest(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _payment_model.RefundRequestRecord.from_protobuf(response)

    async def reject_refund_request(
        self,
        request: _payment_model.RejectRefundRequestRequest
        | _payment_pb.RejectRefundRequestRequest
        | None = None,
        *,
        refund_request_id: str = "",
        reviewer_id: str = "",
        reviewer_display_name: str = "",
        review_comment: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _payment_model.RefundRequestRecord:
        message = (
            _coerce_protobuf_message(request, _payment_pb.RejectRefundRequestRequest)
            if request is not None
            else _payment_pb.RejectRefundRequestRequest(
                refund_request_id=refund_request_id,
                reviewer_id=reviewer_id,
                reviewer_display_name=reviewer_display_name,
                review_comment=review_comment,
            )
        )
        response = await self._call(
            self._s.RejectRefundRequest(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _payment_model.RefundRequestRecord.from_protobuf(response)


class SyncPaymentClient(SyncGatewayClientBase[PaymentClient]):
    """Synchronous facade over :class:`PaymentClient`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(PaymentClient, *args, **kwargs)

    def create_checkout(self, *args: Any, **kwargs: Any) -> _payment_model.CreateCheckoutResponse:
        return self._run(self._client.create_checkout(*args, **kwargs))

    def get_payment_order(self, *args: Any, **kwargs: Any) -> _payment_model.PaymentOrderResponse:
        return self._run(self._client.get_payment_order(*args, **kwargs))

    def list_payment_orders(
        self, *args: Any, **kwargs: Any
    ) -> _payment_model.ListPaymentOrdersResponse:
        return self._run(self._client.list_payment_orders(*args, **kwargs))

    def refund_payment(self, *args: Any, **kwargs: Any) -> _payment_model.RefundPaymentResponse:
        return self._run(self._client.refund_payment(*args, **kwargs))

    def submit_refund_request(
        self, *args: Any, **kwargs: Any
    ) -> _payment_model.RefundRequestRecord:
        return self._run(self._client.submit_refund_request(*args, **kwargs))

    def get_refund_request(self, *args: Any, **kwargs: Any) -> _payment_model.RefundRequestRecord:
        return self._run(self._client.get_refund_request(*args, **kwargs))

    def list_refund_review_logs(
        self, *args: Any, **kwargs: Any
    ) -> _payment_model.ListRefundReviewLogsResponse:
        return self._run(self._client.list_refund_review_logs(*args, **kwargs))

    def list_refund_requests(
        self, *args: Any, **kwargs: Any
    ) -> _payment_model.ListRefundRequestsResponse:
        return self._run(self._client.list_refund_requests(*args, **kwargs))

    def cancel_refund_request(
        self, *args: Any, **kwargs: Any
    ) -> _payment_model.RefundRequestRecord:
        return self._run(self._client.cancel_refund_request(*args, **kwargs))

    def approve_refund_request(
        self, *args: Any, **kwargs: Any
    ) -> _payment_model.RefundRequestRecord:
        return self._run(self._client.approve_refund_request(*args, **kwargs))

    def reject_refund_request(
        self, *args: Any, **kwargs: Any
    ) -> _payment_model.RefundRequestRecord:
        return self._run(self._client.reject_refund_request(*args, **kwargs))


__all__ = [
    "PaymentClient",
    "PaymentError",
    "SyncPaymentClient",
]
"""Stew Gateway billing public gRPC clients."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import grpc.aio

from stew.api.v1 import billing_public_pb2_grpc as _bill_public_grpc

from ._billing_client_shared import (
    BillingAioClientBase,
    BillingError,
    _bill_model,
    _bill_pb,
    coerce_authorization_context,
    coerce_protobuf_message,
    enum_value,
)
from ._discovery.helpers import MetadataEntry, SyncGatewayClientBase


class BillingPublicClient(
    BillingAioClientBase[_bill_public_grpc.BillingPublicServiceStub]
):
    """Async gRPC client for stew.api.v1.BillingPublicService."""

    def _create_stub(
        self,
        channel: grpc.aio.Channel,
    ) -> _bill_public_grpc.BillingPublicServiceStub:
        return _bill_public_grpc.BillingPublicServiceStub(channel)

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

    async def query_balance(
        self,
        request: _bill_model.QueryBalanceRequest
        | _bill_pb.QueryBalanceRequest
        | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        subject_type: _bill_model.BillingSubjectType
        | int = _bill_model.BillingSubjectType(0),
        user_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BalanceSnapshot:
        message = (
            coerce_protobuf_message(request, _bill_pb.QueryBalanceRequest)
            if request is not None
            else _bill_pb.QueryBalanceRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                subject_type=enum_value(subject_type),
                user_id=user_id,
            )
        )
        response = await self._call(
            self._s.QueryBalance(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.BalanceSnapshot.from_protobuf(response)

    async def list_grants(
        self,
        request: _bill_model.ListGrantsRequest
        | _bill_pb.ListGrantsRequest
        | None = None,
        *,
        scope_business_id: str = "",
        subject_id: str = "",
        subject_type: _bill_model.BillingSubjectType
        | int = _bill_model.BillingSubjectType(0),
        user_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.ListGrantsResponse:
        message = (
            coerce_protobuf_message(request, _bill_pb.ListGrantsRequest)
            if request is not None
            else _bill_pb.ListGrantsRequest(
                business_id=scope_business_id,
                subject_id=subject_id,
                subject_type=enum_value(subject_type),
                user_id=user_id,
            )
        )
        response = await self._call(
            self._s.ListGrants(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
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
            coerce_protobuf_message(request, _bill_pb.GetBillingTransactionRequest)
            if request is not None
            else _bill_pb.GetBillingTransactionRequest(
                business_id=scope_business_id,
                request_id=request_id,
            )
        )
        response = await self._call(
            self._s.GetTransaction(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
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
        subject_type: _bill_model.BillingSubjectType
        | int = _bill_model.BillingSubjectType(0),
        user_id: str = "",
        start_time_epoch_seconds: int = 0,
        end_time_epoch_seconds: int = 0,
        page_size: int = 0,
        page_token: str = "",
        transaction_type: _bill_model.BillingTransactionType
        | int = _bill_model.BillingTransactionType(0),
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.QueryTransactionsResponse:
        message = (
            coerce_protobuf_message(request, _bill_pb.QueryTransactionsRequest)
            if request is not None
            else _bill_pb.QueryTransactionsRequest(
                business_id=scope_business_id,
                request_id=request_id,
                authorization_id=authorization_id,
                subject_id=subject_id,
                subject_type=enum_value(subject_type),
                user_id=user_id,
                start_time_epoch_seconds=start_time_epoch_seconds,
                end_time_epoch_seconds=end_time_epoch_seconds,
                page_size=page_size,
                page_token=page_token,
                transaction_type=enum_value(transaction_type),
            )
        )
        response = await self._call(
            self._s.QueryTransactions(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.QueryTransactionsResponse.from_protobuf(response)

    async def query_snapshot(
        self,
        request: _bill_model.QuerySnapshotRequest
        | _bill_pb.QuerySnapshotRequest
        | None = None,
        *,
        scope_business_id: str = "",
        request_id: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _bill_model.BillingSettlementSnapshot:
        message = (
            coerce_protobuf_message(request, _bill_pb.QuerySnapshotRequest)
            if request is not None
            else _bill_pb.QuerySnapshotRequest(
                business_id=scope_business_id,
                request_id=request_id,
            )
        )
        response = await self._call(
            self._s.QuerySnapshot(
                message,
                metadata=self._meta(
                    extra_metadata=extra_metadata, business_id=business_id
                ),
                timeout=self._timeout,
            )
        )
        return _bill_model.BillingSettlementSnapshot.from_protobuf(response)


class SyncBillingPublicClient(SyncGatewayClientBase[BillingPublicClient]):
    """Synchronous facade over :class:`BillingPublicClient`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(BillingPublicClient, *args, **kwargs)

    def estimate_charge(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.EstimateChargeResponse:
        return self._run(self._client.estimate_charge(*args, **kwargs))

    def query_balance(self, *args: Any, **kwargs: Any) -> _bill_model.BalanceSnapshot:
        return self._run(self._client.query_balance(*args, **kwargs))

    def list_grants(self, *args: Any, **kwargs: Any) -> _bill_model.ListGrantsResponse:
        return self._run(self._client.list_grants(*args, **kwargs))

    def get_transaction(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.BillingTransaction:
        return self._run(self._client.get_transaction(*args, **kwargs))

    def query_transactions(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.QueryTransactionsResponse:
        return self._run(self._client.query_transactions(*args, **kwargs))

    def query_snapshot(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.BillingSettlementSnapshot:
        return self._run(self._client.query_snapshot(*args, **kwargs))


__all__ = [
    "BillingError",
    "BillingPublicClient",
    "SyncBillingPublicClient",
]

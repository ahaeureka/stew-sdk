"""Shared helpers for Stew billing gateway clients."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

import grpc

from stew.api.v1 import billing_model as _bill_model
from stew.api.v1 import billing_pb2 as _bill_pb

from ._discovery.errors import DiscoveryError
from ._discovery.helpers import AioGatewayClientBase, wrap_rpc_error

BillingError = DiscoveryError

StubT = TypeVar("StubT")


def coerce_protobuf_message(value: Any, message_type: type[Any]) -> Any:
    if isinstance(value, message_type):
        return value
    if hasattr(value, "to_protobuf"):
        message = value.to_protobuf()
        if isinstance(message, message_type):
            return message
    raise TypeError(f"Expected {message_type.__name__}, got {type(value).__name__}")


def enum_value(value: Any) -> int:
    return int(getattr(value, "value", value))


def coerce_authorization_context(
    value: _bill_model.AuthorizationContext | _bill_pb.AuthorizationContext,
) -> _bill_pb.AuthorizationContext:
    return coerce_protobuf_message(value, _bill_pb.AuthorizationContext)


def coerce_billing_report(
    value: _bill_model.BillingReport | _bill_pb.BillingReport,
) -> _bill_pb.BillingReport:
    return coerce_protobuf_message(value, _bill_pb.BillingReport)


def coerce_billing_policy_artifact_type(value: Any) -> int:
    return enum_value(value)


class BillingAioClientBase(AioGatewayClientBase[StubT], Generic[StubT]):
    async def _call(self, coro: Any) -> Any:
        try:
            return await coro
        except grpc.RpcError as exc:
            raise wrap_rpc_error(exc) from exc


__all__ = [
    "BillingAioClientBase",
    "BillingError",
    "_bill_model",
    "_bill_pb",
    "coerce_authorization_context",
    "coerce_billing_policy_artifact_type",
    "coerce_billing_report",
    "coerce_protobuf_message",
    "enum_value",
]

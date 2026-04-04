import asyncio

import grpc

from stew import (
    AioGrpcContextPassthroughInterceptor,
    GrpcContextPassthroughInterceptor,
    grpc_context_passthrough_handler,
)
from stew._discovery.helpers import make_metadata


def _expected_metadata() -> list[tuple[str, str]]:
    return [
        ("authorization", "Bearer token-123"),
        ("x-user-id", "user-1"),
        ("x-request-id", "req-1"),
        ("x-api-key", "ak_xxx"),
    ]


class FakeContext:
    def invocation_metadata(self):
        return [
            ("authorization", "Bearer token-123"),
            ("x-user-id", "user-1"),
            ("x-request-id", "req-1"),
            ("x-api-key", "inbound-secret"),
        ]


class FakeHandlerCallDetails:
    def __init__(self, invocation_metadata):
        self.invocation_metadata = invocation_metadata


def test_grpc_context_passthrough_handler_wraps_sync_handler() -> None:
    class Service:
        @grpc_context_passthrough_handler
        def get_order(self, request, context):
            return make_metadata("ak_xxx")

    service = Service()

    assert service.get_order(object(), FakeContext()) == _expected_metadata()


def test_grpc_context_passthrough_handler_wraps_async_handler() -> None:
    class Service:
        @grpc_context_passthrough_handler()
        async def get_order(self, request, context):
            return make_metadata("ak_xxx")

    service = Service()

    assert asyncio.run(service.get_order(object(), FakeContext())) == _expected_metadata()


def test_grpc_context_passthrough_interceptor_wraps_sync_handler() -> None:
    interceptor = GrpcContextPassthroughInterceptor()

    def continuation(_details):
        def handler(request, context):
            return make_metadata("ak_xxx")

        return grpc.unary_unary_rpc_method_handler(handler)

    wrapped = interceptor.intercept_service(
        continuation,
        FakeHandlerCallDetails(FakeContext().invocation_metadata()),
    )

    assert wrapped is not None
    assert wrapped.unary_unary(object(), object()) == _expected_metadata()


def test_aio_grpc_context_passthrough_interceptor_wraps_async_handler() -> None:
    interceptor = AioGrpcContextPassthroughInterceptor()

    async def continuation(_details):
        async def handler(request, context):
            return make_metadata("ak_xxx")

        return grpc.unary_unary_rpc_method_handler(handler)

    wrapped = asyncio.run(
        interceptor.intercept_service(
            continuation,
            FakeHandlerCallDetails(FakeContext().invocation_metadata()),
        )
    )

    assert wrapped is not None
    assert asyncio.run(wrapped.unary_unary(object(), object())) == _expected_metadata()
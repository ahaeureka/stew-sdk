import asyncio
import contextvars

import grpc

from stew import (
    AioGrpcContextPassthroughInterceptor,
    GrpcContextPassthroughInterceptor,
    grpc_context_passthrough_handler,
)
from stew._discovery.helpers import (
    _PASSTHROUGH_METADATA,
    grpc_context_passthrough,
    make_metadata,
)


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


def test_grpc_context_passthrough_foreign_context_cleanup() -> None:
    """Regression: grpc_context_passthrough must not raise ValueError when
    the finally block runs in a different contextvars.Context.

    This reproduces the async-generator cleanup scenario where GeneratorExit
    triggers __exit__ in a foreign context after a client disconnects.
    """
    metadata = [("authorization", "Bearer test-123")]

    cm = grpc_context_passthrough(metadata)
    value = cm.__enter__()
    assert value == [("authorization", "Bearer test-123")]

    # Simulate cleanup in a foreign context — exactly what happens when
    # Python finalizes an async generator whose gRPC client has disconnected.
    foreign = contextvars.copy_context()
    foreign.run(cm.__exit__, None, None, None)


def test_asyncgen_cleanup_via_handler_decorator() -> None:
    """grpc_context_passthrough_handler async generator must survive
    aclose() from a foreign context (client disconnect scenario)."""

    @grpc_context_passthrough_handler
    async def watch_items(request, context):
        yield {"id": 1}
        yield {"id": 2}

    async def _run():
        gen = watch_items(object(), FakeContext())
        result = await gen.__anext__()

        # Close from a foreign context to simulate client-disconnect cleanup.
        foreign = contextvars.copy_context()
        foreign.run(lambda: None)  # ensure context is independent

        # aclose() triggers the context manager finally block.
        # In a real scenario, asyncio may run this in a different task context.
        await gen.aclose()

        assert result == {"id": 1}

    asyncio.run(_run())


def test_asyncgen_cleanup_via_interceptor() -> None:
    """AioGrpcContextPassthroughInterceptor async-stream handler must survive
    aclose() from a foreign context."""

    async def _run():
        invocation_metadata = [("authorization", "Bearer token-123")]

        async def handler(request, context):
            yield {"id": 1}

        interceptor = AioGrpcContextPassthroughInterceptor()

        async def continuation(_details):
            return grpc.unary_stream_rpc_method_handler(handler)

        wrapped = await interceptor.intercept_service(
            continuation,
            FakeHandlerCallDetails(invocation_metadata),
        )

        gen = wrapped.unary_stream(object(), object())
        result = await gen.__anext__()
        await gen.aclose()

        assert result == {"id": 1}

    asyncio.run(_run())
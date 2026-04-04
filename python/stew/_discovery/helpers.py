from __future__ import annotations

import functools
import hashlib
import inspect
from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import Any, Callable, Iterator, Sequence, TypeVar

import grpc

from stew.api.v1 import service_discovery_pb2 as _pb

from .errors import ConflictError, DiscoveryError, NotFoundError
from .types import BalanceType, Endpoint, EndpointBinding, HealthCheckConfig, MiddlewareConfig


MetadataEntry = tuple[str, str]
HandlerFunc = TypeVar("HandlerFunc", bound=Callable[..., Any])

_PASSTHROUGH_METADATA: ContextVar[tuple[MetadataEntry, ...]] = ContextVar(
    "stew_passthrough_grpc_metadata",
    default=(),
)

_PASSTHROUGH_HEADERS = frozenset(
    {
        "authorization",
        "baggage",
        "traceparent",
        "tracestate",
        "x-client-context",
        "x-request-id",
        "x-b3-traceid",
        "x-b3-spanid",
        "x-b3-parentspanid",
        "x-b3-sampled",
        "x-b3-flags",
    }
)

_PASSTHROUGH_PREFIXES = (
    "x-user-",
    "x-token-",
)

_BLOCKED_INBOUND_HEADERS = frozenset(
    {
        "content-type",
        "grpc-accept-encoding",
        "grpc-timeout",
        "te",
        "user-agent",
        "x-api-key",
        "x-api-key-id",
        "x-api-key-name",
        "x-api-key-scopes",
    }
)


def _coerce_metadata_value(value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def _normalize_metadata_entry(item: Any) -> MetadataEntry | None:
    if hasattr(item, "key") and hasattr(item, "value"):
        key = getattr(item, "key")
        value = getattr(item, "value")
    elif isinstance(item, Sequence) and not isinstance(item, (str, bytes)) and len(item) == 2:
        key, value = item
    else:
        return None

    key_str = _coerce_metadata_value(key).strip().lower()
    if not key_str or key_str.endswith("-bin"):
        return None

    return key_str, _coerce_metadata_value(value)


def _should_passthrough_header(header: str) -> bool:
    return header in _PASSTHROUGH_HEADERS or any(
        header.startswith(prefix) for prefix in _PASSTHROUGH_PREFIXES
    )


def _upsert_metadata(metadata: list[MetadataEntry], entry: MetadataEntry) -> None:
    key, value = entry
    for index, (existing_key, _) in enumerate(metadata):
        if existing_key == key:
            metadata[index] = (key, value)
            return
    metadata.append((key, value))


def collect_grpc_context_metadata(context_or_metadata: Any) -> list[MetadataEntry]:
    metadata_source = context_or_metadata
    if hasattr(context_or_metadata, "invocation_metadata"):
        metadata_source = context_or_metadata.invocation_metadata()

    collected: list[MetadataEntry] = []
    for item in metadata_source or ():
        normalized = _normalize_metadata_entry(item)
        if normalized is None:
            continue

        key, value = normalized
        if key in _BLOCKED_INBOUND_HEADERS or not _should_passthrough_header(key):
            continue

        _upsert_metadata(collected, (key, value))

    return collected


def set_grpc_context_metadata(context_or_metadata: Any) -> Token[tuple[MetadataEntry, ...]]:
    metadata = tuple(collect_grpc_context_metadata(context_or_metadata))
    return _PASSTHROUGH_METADATA.set(metadata)


def reset_grpc_context_metadata(token: Token[tuple[MetadataEntry, ...]]) -> None:
    _PASSTHROUGH_METADATA.reset(token)


@contextmanager
def grpc_context_passthrough(context_or_metadata: Any) -> Iterator[list[MetadataEntry]]:
    token = set_grpc_context_metadata(context_or_metadata)
    try:
        yield list(_PASSTHROUGH_METADATA.get())
    finally:
        reset_grpc_context_metadata(token)


def _resolve_context_argument(
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    context_arg: str,
) -> Any:
    bound = inspect.signature(func).bind_partial(*args, **kwargs)
    if context_arg not in bound.arguments:
        raise TypeError(
            f"Context argument '{context_arg}' was not provided to {func.__qualname__}"
        )
    return bound.arguments[context_arg]


async def _await_if_needed(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


def _iter_stream_items(value: Any) -> Iterator[Any]:
    if value is None:
        return iter(())
    return iter(value)


async def _aiter_stream_items(value: Any):
    if inspect.isawaitable(value):
        value = await value

    if hasattr(value, "__aiter__"):
        async for item in value:
            yield item
        return

    for item in _iter_stream_items(value):
        yield item


def grpc_context_passthrough_handler(
    func: HandlerFunc | None = None,
    *,
    context_arg: str = "context",
) -> HandlerFunc | Callable[[HandlerFunc], HandlerFunc]:
    def decorator(inner: HandlerFunc) -> HandlerFunc:
        if inspect.isasyncgenfunction(inner):

            @functools.wraps(inner)
            async def asyncgen_wrapper(*args: Any, **kwargs: Any):
                context = _resolve_context_argument(inner, args, kwargs, context_arg)
                with grpc_context_passthrough(context):
                    async for item in inner(*args, **kwargs):
                        yield item

            return asyncgen_wrapper  # type: ignore[return-value]

        if inspect.iscoroutinefunction(inner):

            @functools.wraps(inner)
            async def async_wrapper(*args: Any, **kwargs: Any):
                context = _resolve_context_argument(inner, args, kwargs, context_arg)
                with grpc_context_passthrough(context):
                    return await inner(*args, **kwargs)

            return async_wrapper  # type: ignore[return-value]

        if inspect.isgeneratorfunction(inner):

            @functools.wraps(inner)
            def generator_wrapper(*args: Any, **kwargs: Any):
                context = _resolve_context_argument(inner, args, kwargs, context_arg)
                with grpc_context_passthrough(context):
                    yield from inner(*args, **kwargs)

            return generator_wrapper  # type: ignore[return-value]

        @functools.wraps(inner)
        def wrapper(*args: Any, **kwargs: Any):
            context = _resolve_context_argument(inner, args, kwargs, context_arg)
            with grpc_context_passthrough(context):
                return inner(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    if func is not None:
        return decorator(func)
    return decorator


def _wrap_sync_rpc_method_handler(
    handler: grpc.RpcMethodHandler,
    invocation_metadata: Any,
) -> grpc.RpcMethodHandler:
    if handler.request_streaming and handler.response_streaming:

        def stream_stream(request_iterator: Any, context: Any):
            with grpc_context_passthrough(invocation_metadata):
                yield from _iter_stream_items(handler.stream_stream(request_iterator, context))

        return grpc.stream_stream_rpc_method_handler(
            stream_stream,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )

    if handler.request_streaming:

        def stream_unary(request_iterator: Any, context: Any):
            with grpc_context_passthrough(invocation_metadata):
                return handler.stream_unary(request_iterator, context)

        return grpc.stream_unary_rpc_method_handler(
            stream_unary,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )

    if handler.response_streaming:

        def unary_stream(request: Any, context: Any):
            with grpc_context_passthrough(invocation_metadata):
                yield from _iter_stream_items(handler.unary_stream(request, context))

        return grpc.unary_stream_rpc_method_handler(
            unary_stream,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )

    def unary_unary(request: Any, context: Any):
        with grpc_context_passthrough(invocation_metadata):
            return handler.unary_unary(request, context)

    return grpc.unary_unary_rpc_method_handler(
        unary_unary,
        request_deserializer=handler.request_deserializer,
        response_serializer=handler.response_serializer,
    )


def _wrap_async_rpc_method_handler(
    handler: grpc.RpcMethodHandler,
    invocation_metadata: Any,
) -> grpc.RpcMethodHandler:
    if handler.request_streaming and handler.response_streaming:

        async def stream_stream(request_iterator: Any, context: Any):
            with grpc_context_passthrough(invocation_metadata):
                async for item in _aiter_stream_items(handler.stream_stream(request_iterator, context)):
                    yield item

        return grpc.stream_stream_rpc_method_handler(
            stream_stream,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )

    if handler.request_streaming:

        async def stream_unary(request_iterator: Any, context: Any):
            with grpc_context_passthrough(invocation_metadata):
                return await _await_if_needed(handler.stream_unary(request_iterator, context))

        return grpc.stream_unary_rpc_method_handler(
            stream_unary,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )

    if handler.response_streaming:

        async def unary_stream(request: Any, context: Any):
            with grpc_context_passthrough(invocation_metadata):
                async for item in _aiter_stream_items(handler.unary_stream(request, context)):
                    yield item

        return grpc.unary_stream_rpc_method_handler(
            unary_stream,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )

    async def unary_unary(request: Any, context: Any):
        with grpc_context_passthrough(invocation_metadata):
            return await _await_if_needed(handler.unary_unary(request, context))

    return grpc.unary_unary_rpc_method_handler(
        unary_unary,
        request_deserializer=handler.request_deserializer,
        response_serializer=handler.response_serializer,
    )


class GrpcContextPassthroughInterceptor(grpc.ServerInterceptor):
    """Bind inbound gRPC metadata to the SDK context for synchronous handlers."""

    def intercept_service(self, continuation: Any, handler_call_details: Any):
        handler = continuation(handler_call_details)
        if handler is None:
            return None
        return _wrap_sync_rpc_method_handler(handler, handler_call_details.invocation_metadata)


class AioGrpcContextPassthroughInterceptor(grpc.aio.ServerInterceptor):
    """Bind inbound gRPC metadata to the SDK context for asyncio handlers."""

    async def intercept_service(self, continuation: Any, handler_call_details: Any):
        handler = await continuation(handler_call_details)
        if handler is None:
            return None
        return _wrap_async_rpc_method_handler(handler, handler_call_details.invocation_metadata)


def make_metadata(
    api_key: str,
    *,
    extra_metadata: Sequence[MetadataEntry] = (),
) -> list[MetadataEntry]:
    metadata = list(_PASSTHROUGH_METADATA.get())

    if api_key:
        _upsert_metadata(metadata, ("x-api-key", api_key))

    for item in extra_metadata:
        normalized = _normalize_metadata_entry(item)
        if normalized is None:
            continue
        key, value = normalized
        if key == "x-api-key":
            continue
        _upsert_metadata(metadata, (key, value))

    return metadata


def to_proto_lb(
    endpoints: Sequence[Endpoint],
    balance_type: BalanceType,
) -> _pb.LoadBalancer:
    return _pb.LoadBalancer(
        type=f"BALANCE_TYPE_{balance_type.name}",
        endpoints=[
            _pb.Endpoint(address=ep.address, port=ep.port, weight=ep.weight)
            for ep in endpoints
        ],
    )


def to_proto_hc(cfg: HealthCheckConfig | None) -> _pb.HealthCheckConfig | None:
    if cfg is None:
        return None
    return _pb.HealthCheckConfig(
        enabled=cfg.enabled,
        grpc_method=cfg.grpc_method,
        http_path=cfg.http_path,
        interval_seconds=cfg.interval_seconds,
        timeout_seconds=cfg.timeout_seconds,
        healthy_threshold=cfg.healthy_threshold,
        unhealthy_threshold=cfg.unhealthy_threshold,
    )


def to_proto_mw(cfg: MiddlewareConfig | None) -> _pb.ServiceMiddlewareConfig | None:
    if cfg is None:
        return None
    kwargs: dict = dict(
        rate_limit_enabled=cfg.rate_limit_enabled,
        rate_limit_rpm=cfg.rate_limit_rpm,
        rate_limit_user_rpm=cfg.rate_limit_user_rpm,
        cors_enabled=cfg.cors_enabled,
        risk_enabled=cfg.risk_enabled,
        turnstile_enabled=cfg.turnstile_enabled,
    )
    if cfg.cors is not None:
        kwargs["cors"] = cfg.cors
    if cfg.risk is not None:
        kwargs["risk"] = cfg.risk
    if cfg.turnstile is not None:
        kwargs["turnstile"] = cfg.turnstile
    return _pb.ServiceMiddlewareConfig(**kwargs)


def as_discovery_error(exc: Exception) -> DiscoveryError:
    if isinstance(exc, DiscoveryError):
        return exc
    return DiscoveryError(f"Unexpected client error: {exc}")


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def endpoint_matches_binding(
    binding: EndpointBinding,
    *,
    service_name: str,
    endpoint: Endpoint,
    protocol: str,
    tls_enabled: bool,
) -> bool:
    return (
        binding.service_name == service_name
        and binding.address == endpoint.address
        and binding.port == endpoint.port
        and binding.protocol == protocol
        and binding.tls_enabled == tls_enabled
    )


def wrap_rpc_error(exc: grpc.RpcError) -> DiscoveryError:
    code: grpc.StatusCode = exc.code()  # type: ignore[attr-defined]
    detail: str = exc.details() or ""  # type: ignore[attr-defined]
    if code == grpc.StatusCode.NOT_FOUND:
        return NotFoundError(detail, code=code)
    if code == grpc.StatusCode.FAILED_PRECONDITION:
        return ConflictError(detail, code=code)
    return DiscoveryError(f"[{code.name}] {detail}", code=code)


__all__ = [
    "AioGrpcContextPassthroughInterceptor",
    "GrpcContextPassthroughInterceptor",
    "as_discovery_error",
    "collect_grpc_context_metadata",
    "endpoint_matches_binding",
    "grpc_context_passthrough",
    "grpc_context_passthrough_handler",
    "hash_bytes",
    "make_metadata",
    "reset_grpc_context_metadata",
    "set_grpc_context_metadata",
    "to_proto_hc",
    "to_proto_lb",
    "to_proto_mw",
    "wrap_rpc_error",
]
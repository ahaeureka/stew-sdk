"""Entitlement guard — one-click feature and quota checks for gRPC service handlers.

Usage (class-based, imperative)::

    from stew.entitlement_guard import EntitlementGuard
    from stew.api.v1.entitlement_pb2_grpc import EntitlementServiceStub

    stub = EntitlementServiceStub(channel)
    guard = EntitlementGuard(stub, business_id="skillforge")

    class MyService(MyServiceServicer):
        async def ExtractText(self, request, context):
            # Fail-closed: aborts with PERMISSION_DENIED / RESOURCE_EXHAUSTED
            await guard.require_feature(context, "extraction.mode.standard")
            await guard.require_quota(context, "credits.monthly", estimated_points)
            # ... business logic ...

Usage (decorator, declarative)::

    from stew.entitlement_guard import require_feature, require_quota

    class MyService(MyServiceServicer):
        # Set by the application during service initialization
        entitlement_guard: EntitlementGuard

        @require_feature("extraction.mode.standard")
        @require_quota("credits.monthly", "estimated_points")
        async def ExtractText(self, request, context):
            # Guard checks run before the handler body
            ...
"""

from __future__ import annotations

import functools
import inspect
import logging
from typing import Any, Callable, TypeVar, Union

import grpc

from stew.api.v1 import entitlement_pb2 as _pb
from stew.api.v1 import entitlement_pb2_grpc

HandlerFunc = TypeVar("HandlerFunc", bound=Callable[..., Any])

_logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Error types (for non-gRPC / imperative use)
# ---------------------------------------------------------------------------


class EntitlementGuardError(Exception):
    """Base error raised when entitlement checks fail outside a gRPC context."""


class FeatureDeniedError(EntitlementGuardError):
    """Feature gate check failed."""

    def __init__(self, feature_key: str, plan_id: str = "", message: str = ""):
        self.feature_key = feature_key
        self.plan_id = plan_id
        super().__init__(message or f"Feature '{feature_key}' is not enabled")


class QuotaExceededError(EntitlementGuardError):
    """Quota check failed."""

    def __init__(self, quota_key: str, used: int, limit: int, requested: int):
        self.quota_key = quota_key
        self.used = used
        self.limit = limit
        self.requested = requested
        super().__init__(
            f"Quota '{quota_key}' exceeded: used {used}/{limit}, requested {requested}"
        )


# ---------------------------------------------------------------------------
# EntitlementGuard
# ---------------------------------------------------------------------------


class EntitlementGuard:
    """One-click feature and quota guard for gRPC service handlers.

    Wraps an ``EntitlementServiceStub`` and provides ergonomic methods that
    extract the caller identity from gRPC metadata, call the gateway's
    entitlement service, and either return or abort.

    All ``require_*`` methods are **fail-closed**: if the entitlement service
    is unreachable the request is rejected rather than silently allowed.
    """

    def __init__(
        self,
        stub: entitlement_pb2_grpc.EntitlementServiceStub,
        business_id: str,
        *,
        timeout: float | None = None,
    ):
        self._stub = stub
        self._business_id = business_id
        self._timeout = timeout

    # -- identity -----------------------------------------------------------

    def _resolve_context(
        self,
        context_or_subject_id: Union[grpc.aio.ServicerContext, str],
    ) -> "tuple[str, grpc.aio.ServicerContext | None]":
        """Return ``(subject_id, context)`` from either a context or raw string."""
        if isinstance(context_or_subject_id, str):
            return context_or_subject_id, None
        subject_id = self._extract_subject_id(context_or_subject_id)
        return subject_id, context_or_subject_id

    @staticmethod
    def _extract_subject_id(context: grpc.aio.ServicerContext) -> str:
        metadata = dict(context.invocation_metadata())
        subject_id = (
            metadata.get("x-user-id")
            or metadata.get("x-subject-id")
            or metadata.get("x-billing-subject-id")
            or ""
        )
        if not subject_id:
            _logger.warning("No subject identity found in gRPC metadata")
        return subject_id

    # -- feature checks -----------------------------------------------------

    async def require_feature(
        self,
        context_or_subject_id: Union[grpc.aio.ServicerContext, str],
        feature_key: str,
    ) -> None:
        """Assert that *feature_key* is enabled for the caller.

        Aborts with ``PERMISSION_DENIED`` when the feature is disabled or the
        entitlement service is unreachable.
        """
        subject_id, context = self._resolve_context(context_or_subject_id)

        request = _pb.CheckFeatureRequest(
            business_id=self._business_id,
            subject_id=subject_id,
            feature_key=feature_key,
        )
        try:
            response = await self._stub.CheckFeature(request, timeout=self._timeout)
        except grpc.RpcError as exc:
            _logger.error(
                "CheckFeature RPC failed: feature=%s subject=%s error=%s",
                feature_key, subject_id, exc,
            )
            if context is not None:
                await context.abort(exc.code(), exc.details())
            raise

        if not response.enabled:
            plan_hint = f" (current plan: {response.plan_id})" if response.plan_id else ""
            msg = f"Feature '{feature_key}' is not enabled{plan_hint}"
            _logger.warning("Feature denied: %s subject=%s", feature_key, subject_id)
            if context is not None:
                await context.abort(grpc.StatusCode.PERMISSION_DENIED, msg)
            raise FeatureDeniedError(feature_key, plan_id=response.plan_id or "", message=msg)

    async def check_feature(
        self,
        context_or_subject_id: Union[grpc.aio.ServicerContext, str],
        feature_key: str,
    ) -> bool:
        """Return whether *feature_key* is enabled.  Never aborts.

        Raises ``grpc.RpcError`` if the entitlement service is unreachable.
        """
        subject_id, _ = self._resolve_context(context_or_subject_id)

        request = _pb.CheckFeatureRequest(
            business_id=self._business_id,
            subject_id=subject_id,
            feature_key=feature_key,
        )
        response = await self._stub.CheckFeature(request, timeout=self._timeout)
        return response.enabled

    # -- quota checks -------------------------------------------------------

    async def require_quota(
        self,
        context_or_subject_id: Union[grpc.aio.ServicerContext, str],
        quota_key: str,
        requested: int = 1,
    ) -> None:
        """Assert that *quota_key* has at least *requested* units remaining.

        Aborts with ``RESOURCE_EXHAUSTED`` when the quota is exhausted or the
        entitlement service is unreachable.
        """
        subject_id, context = self._resolve_context(context_or_subject_id)

        request = _pb.CheckQuotaRequest(
            business_id=self._business_id,
            subject_id=subject_id,
            quota_key=quota_key,
        )
        try:
            response = await self._stub.CheckQuota(request, timeout=self._timeout)
        except grpc.RpcError as exc:
            _logger.error(
                "CheckQuota RPC failed: quota=%s subject=%s error=%s",
                quota_key, subject_id, exc,
            )
            if context is not None:
                await context.abort(exc.code(), exc.details())
            raise

        if response.used + requested > response.limit:
            msg = (
                f"Quota '{quota_key}' exceeded: "
                f"used {response.used}/{response.limit}, requested {requested}"
            )
            _logger.warning(
                "Quota exceeded: %s used=%s/%s requested=%s subject=%s",
                quota_key, response.used, response.limit, requested, subject_id,
            )
            if context is not None:
                await context.abort(grpc.StatusCode.RESOURCE_EXHAUSTED, msg)
            raise QuotaExceededError(quota_key, response.used, response.limit, requested)

    async def check_quota(
        self,
        context_or_subject_id: Union[grpc.aio.ServicerContext, str],
        quota_key: str,
        requested: int = 1,
    ) -> "tuple[bool, int, int]":
        """Return ``(allowed, used, limit)``.  Never aborts.

        Raises ``grpc.RpcError`` if the entitlement service is unreachable.
        """
        subject_id, _ = self._resolve_context(context_or_subject_id)

        request = _pb.CheckQuotaRequest(
            business_id=self._business_id,
            subject_id=subject_id,
            quota_key=quota_key,
        )
        response = await self._stub.CheckQuota(request, timeout=self._timeout)
        allowed = response.used + requested <= response.limit
        return allowed, response.used, response.limit

    async def consume_quota(
        self,
        context_or_subject_id: Union[grpc.aio.ServicerContext, str],
        quota_key: str,
        amount: int = 1,
    ) -> None:
        """Atomically increment quota usage by *amount*.

        Callers should check availability with ``require_quota`` or
        ``check_quota`` before consuming.  This method only performs the
        atomic increment — it does not re-check limits.

        Aborts with the upstream error code if the entitlement service
        is unreachable.
        """
        subject_id, context = self._resolve_context(context_or_subject_id)

        request = _pb.IncrementQuotaRequest(
            business_id=self._business_id,
            subject_id=subject_id,
            quota_key=quota_key,
            delta=amount,
        )
        try:
            await self._stub.IncrementQuota(request, timeout=self._timeout)
        except grpc.RpcError as exc:
            _logger.error(
                "IncrementQuota RPC failed: quota=%s amount=%s subject=%s error=%s",
                quota_key, amount, subject_id, exc,
            )
            if context is not None:
                await context.abort(exc.code(), exc.details())
            raise


# ---------------------------------------------------------------------------
# Decorator helpers
# ---------------------------------------------------------------------------


def _resolve_arg(
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    arg_name: str,
) -> Any:
    """Resolve a named argument from positional or keyword args."""
    sig = inspect.signature(func)
    bound = sig.bind_partial(*args, **kwargs)
    if arg_name not in bound.arguments:
        raise TypeError(
            f"Argument '{arg_name}' was not provided to {func.__qualname__}"
        )
    return bound.arguments[arg_name]


def _resolve_guard(self_obj: Any, guard_attr: str) -> EntitlementGuard:
    guard = getattr(self_obj, guard_attr, None)
    if not isinstance(guard, EntitlementGuard):
        raise TypeError(
            f"self.{guard_attr} is not an EntitlementGuard instance. "
            f"Set: self.{guard_attr} = EntitlementGuard(stub, business_id='...')"
        )
    return guard


def _resolve_amount(amount_spec: Any, request: Any) -> int:
    """Resolve the requested amount for a quota check.

    * ``int`` → used directly.
    * ``str`` → ``getattr(request, amount_spec)``.
    * ``callable`` → ``amount_spec(request)`` (must be sync).

    Raises ``ValueError`` if the amount cannot be resolved.
    """
    if isinstance(amount_spec, int):
        return amount_spec
    if callable(amount_spec):
        return int(amount_spec(request))
    if isinstance(amount_spec, str):
        if request is None:
            raise ValueError(
                f"Cannot resolve amount from {amount_spec!r}: request is None"
            )
        value = getattr(request, amount_spec, None)
        if value is not None:
            return int(value)
        raise ValueError(
            f"Cannot resolve amount: {type(request).__name__!r} has no "
            f"attribute {amount_spec!r}"
        )
    raise ValueError(
        f"Cannot resolve amount from {amount_spec!r} "
        f"(expected int, str, or callable)"
    )


# ---------------------------------------------------------------------------
# Decorators
# ---------------------------------------------------------------------------


def require_feature(
    feature_key: str,
    *,
    guard_attr: str = "entitlement_guard",
    context_arg: str = "context",
) -> Callable[[HandlerFunc], HandlerFunc]:
    """Decorator: require a feature to be enabled before the handler runs.

    Example::

        class MyService:
            entitlement_guard = EntitlementGuard(stub, business_id="skillforge")

            @require_feature("extraction.mode.professional")
            async def ExtractText(self, request, context):
                ...

    The guard is read from ``self.<guard_attr>`` (default ``entitlement_guard``).
    Supports async functions and async generators.
    """

    def decorator(func: HandlerFunc) -> HandlerFunc:
        if inspect.isasyncgenfunction(func):

            @functools.wraps(func)
            async def asyncgen_wrapper(*args: Any, **kwargs: Any):
                self_obj = args[0] if args else None
                context = _resolve_arg(func, args, kwargs, context_arg)
                guard = _resolve_guard(self_obj, guard_attr)
                await guard.require_feature(context, feature_key)
                async for item in func(*args, **kwargs):
                    yield item

            return asyncgen_wrapper  # type: ignore[return-value]

        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any):
                self_obj = args[0] if args else None
                context = _resolve_arg(func, args, kwargs, context_arg)
                guard = _resolve_guard(self_obj, guard_attr)
                await guard.require_feature(context, feature_key)
                return await func(*args, **kwargs)

            return async_wrapper  # type: ignore[return-value]

        # Sync functions: wrap in a helper that creates a fresh event loop
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            self_obj = args[0] if args else None
            context = _resolve_arg(func, args, kwargs, context_arg)
            guard = _resolve_guard(self_obj, guard_attr)
            import asyncio

            asyncio.run(guard.require_feature(context, feature_key))
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def require_quota(
    quota_key: str,
    amount: "Union[int, str, Callable[[Any], int]]" = 1,
    *,
    guard_attr: str = "entitlement_guard",
    context_arg: str = "context",
    request_arg: str = "request",
) -> Callable[[HandlerFunc], HandlerFunc]:
    """Decorator: require quota availability before the handler runs.

    Example::

        class MyService:
            entitlement_guard = EntitlementGuard(stub, business_id="skillforge")

            # Fixed amount:
            @require_quota("credits.monthly", 5)
            async def HandlerA(self, request, context):
                ...

            # Amount read from a request field:
            @require_quota("credits.monthly", "estimated_points")
            async def HandlerB(self, request, context):
                ...

    Args:
        quota_key: The quota key to check.
        amount: Fixed ``int``, request field name (``str``), or
                ``Callable[[request], int]``.  Default 1.
        guard_attr: Attribute name on ``self`` holding the ``EntitlementGuard``.
        context_arg: Name of the gRPC context parameter.
        request_arg: Name of the request parameter.
    """

    def decorator(func: HandlerFunc) -> HandlerFunc:
        if inspect.isasyncgenfunction(func):

            @functools.wraps(func)
            async def asyncgen_wrapper(*args: Any, **kwargs: Any):
                self_obj = args[0] if args else None
                context = _resolve_arg(func, args, kwargs, context_arg)
                guard = _resolve_guard(self_obj, guard_attr)
                request = kwargs.get(request_arg, args[1] if len(args) > 1 else None)
                req = _resolve_amount(amount, request)
                await guard.require_quota(context, quota_key, req)
                async for item in func(*args, **kwargs):
                    yield item

            return asyncgen_wrapper  # type: ignore[return-value]

        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any):
                self_obj = args[0] if args else None
                context = _resolve_arg(func, args, kwargs, context_arg)
                guard = _resolve_guard(self_obj, guard_attr)
                request = kwargs.get(request_arg, args[1] if len(args) > 1 else None)
                req = _resolve_amount(amount, request)
                await guard.require_quota(context, quota_key, req)
                return await func(*args, **kwargs)

            return async_wrapper  # type: ignore[return-value]

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            self_obj = args[0] if args else None
            context = _resolve_arg(func, args, kwargs, context_arg)
            guard = _resolve_guard(self_obj, guard_attr)
            request = kwargs.get(request_arg, args[1] if len(args) > 1 else None)
            req = _resolve_amount(amount, request)
            import asyncio

            asyncio.run(guard.require_quota(context, quota_key, req))
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator

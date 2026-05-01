"""Gateway identity context — read user identity from gRPC metadata injected by the Stew gateway.

Usage (gRPC server handler)::

    from stew.identity import GatewayIdentity

    def get_order(self, request, context):
        identity = GatewayIdentity.from_grpc_context(context)

        if identity.is_anonymous:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "login required")

        # Snowflake UID — primary user identifier for DB / billing / entitlements
        print(identity.user_id)         # "7234567890123456789"
        print(identity.local_user_id)   # 7234567890123456789 (int)

        # OIDC Subject — only for debugging / external IdP interaction
        print(identity.oidc_sub)        # "google-oauth2|112500596056966856512"

Usage (gRPC interceptor)::

    from stew.identity import GatewayIdentity

    class AuthInterceptor(grpc.aio.ServerInterceptor):
        async def intercept_service(self, continuation, handler_call_details):
            identity = GatewayIdentity.from_metadata(dict(handler_call_details.invocation_metadata))
            # attach to context or check permissions ...
            return await continuation(handler_call_details)
"""

from __future__ import annotations

import json
import enum
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Optional, Sequence, Tuple, Union

import grpc


# ---------------------------------------------------------------------------
# Metadata key constants
# ---------------------------------------------------------------------------

# Primary identity (Snowflake UID)
X_USER_ID = "x-user-id"
X_OIDC_SUB = "x-oidc-sub"

# Supplementary user info
X_USER_EMAIL = "x-user-email"
X_USER_NAME = "x-user-name"
X_TOKEN_ISSUER = "x-token-issuer"

# API Key identity
X_API_KEY_ID = "x-api-key-id"
X_API_KEY_NAME = "x-api-key-name"
X_API_KEY_SCOPES = "x-api-key-scopes"

# Request context
X_REQUEST_ID = "x-request-id"
X_CLIENT_CONTEXT = "x-client-context"

# Subscription / entitlement (injected by SubscriptionMiddleware)
X_PLAN_ID = "x-plan-id"
X_PLAN_NAME = "x-plan-name"
X_PLAN_STATUS = "x-plan-status"
X_PLAN_FEATURES = "x-plan-features"
X_PLAN_QUOTAS = "x-plan-quotas"

# Billing (injected by BillingMiddleware)
X_BILLING_AUTHORIZATION_ID = "x-billing-authorization-id"


# ---------------------------------------------------------------------------
# Auth mode enum
# ---------------------------------------------------------------------------

class AuthMode(enum.Enum):
    """How the caller authenticated."""

    JWT_OR_SESSION = "jwt_or_session"
    API_KEY = "api_key"
    ANONYMOUS = "anonymous"


# ---------------------------------------------------------------------------
# Core dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GatewayIdentity:
    """Parsed gateway identity extracted from gRPC metadata / HTTP headers.

    Attributes:
        user_id:          Snowflake UID string (primary identifier).
        local_user_id:    Snowflake UID as ``int``, or ``None`` if user_id is not numeric.
        oidc_sub:         Original OIDC Subject (e.g. ``"google-oauth2|xxx"``).
        email:            User email (may be empty).
        display_name:     User display name (may be empty).
        token_issuer:     JWT issuer URL.
        auth_mode:        How the request was authenticated.
        api_key_id:       API Key UUID (only when ``auth_mode == API_KEY``).
        api_key_name:     API Key display name.
        api_key_scopes:   API Key permission scopes.
        request_id:       Gateway-assigned request ID.
        plan_id:          Subscription plan ID (if injected).
        plan_name:        Subscription plan name (if injected).
        plan_status:      Subscription status (if injected).
        plan_features:    Enabled feature keys (comma-separated).
        plan_quotas:      Quota summary (comma-separated).
        client_context:   Raw ``x-client-context`` JSON string.
        raw_metadata:     Full metadata dict for advanced use.
    """

    user_id: str = ""
    oidc_sub: str = ""
    email: str = ""
    display_name: str = ""
    token_issuer: str = ""
    auth_mode: AuthMode = AuthMode.ANONYMOUS

    api_key_id: str = ""
    api_key_name: str = ""
    api_key_scopes: Tuple[str, ...] = ()

    request_id: str = ""

    plan_id: str = ""
    plan_name: str = ""
    plan_status: str = ""
    plan_features: str = ""
    plan_quotas: str = ""

    client_context: str = ""
    raw_metadata: Dict[str, str] = field(default_factory=dict, repr=False)

    # -- derived helpers -----------------------------------------------------

    @property
    def local_user_id(self) -> Optional[int]:
        """Parse ``user_id`` as a Snowflake integer.

        Returns ``None`` when ``user_id`` is empty or not a valid integer
        (e.g. fallback OIDC sub in legacy mode).
        """
        if not self.user_id:
            return None
        try:
            return int(self.user_id)
        except ValueError:
            return None

    @property
    def is_anonymous(self) -> bool:
        """True when no authenticated user identity is present."""
        return self.auth_mode == AuthMode.ANONYMOUS

    @property
    def is_api_key(self) -> bool:
        """True when the request was authenticated via API Key."""
        return self.auth_mode == AuthMode.API_KEY

    @property
    def is_jwt_or_session(self) -> bool:
        """True when the request was authenticated via JWT or session cookie."""
        return self.auth_mode == AuthMode.JWT_OR_SESSION

    @property
    def feature_keys(self) -> Tuple[str, ...]:
        """Parse ``plan_features`` into a tuple of individual feature keys."""
        if not self.plan_features:
            return ()
        return tuple(f.strip() for f in self.plan_features.split(",") if f.strip())

    @property
    def has_plan(self) -> bool:
        """True when subscription plan info is available."""
        return bool(self.plan_id)

    def parsed_client_context(self) -> Dict[str, Any]:
        """Parse the ``x-client-context`` JSON into a dict.

        Returns an empty dict on parse failure.
        """
        if not self.client_context:
            return {}
        try:
            return json.loads(self.client_context)
        except (json.JSONDecodeError, TypeError):
            return {}

    def require_user_id(self) -> str:
        """Return ``user_id`` or raise an error suitable for ``context.abort()``.

        Usage::

            identity = GatewayIdentity.from_grpc_context(context)
            user_id = identity.require_user_id()  # raises on anonymous
        """
        if self.user_id:
            return self.user_id
        raise ValueError("missing x-user-id: request is not authenticated")

    def require_local_user_id(self) -> int:
        """Return ``local_user_id`` as int or raise.

        Useful when the database expects a BIGINT snowflake ID.
        """
        uid = self.local_user_id
        if uid is not None:
            return uid
        raise ValueError(
            f"x-user-id is not a valid Snowflake UID: {self.user_id!r}"
        )

    # -- factory methods -----------------------------------------------------

    @classmethod
    def from_grpc_context(
        cls,
        context: Union[grpc.aio.ServicerContext, grpc.ServicerContext],
    ) -> "GatewayIdentity":
        """Create from a gRPC servicer context.

        Example::

            def MyRPC(self, request, context):
                identity = GatewayIdentity.from_grpc_context(context)
        """
        md = {k: v for k, v in context.invocation_metadata()}
        return cls.from_metadata(md)

    @classmethod
    def from_metadata(cls, metadata: Dict[str, str]) -> "GatewayIdentity":
        """Create from a metadata dict.

        Accepts any ``{key: value}`` mapping — works for both
        ``context.invocation_metadata()`` (list of tuples) already converted to
        dict, and raw HTTP header dicts.
        """
        def _get(key: str) -> str:
            return metadata.get(key, "").strip()

        user_id = _get(X_USER_ID)
        api_key_id = _get(X_API_KEY_ID)
        token_issuer = _get(X_TOKEN_ISSUER)

        # Determine auth mode
        if api_key_id:
            auth_mode = AuthMode.API_KEY
        elif user_id and token_issuer:
            auth_mode = AuthMode.JWT_OR_SESSION
        elif user_id:
            # Has user_id but no explicit token_issuer — still authenticated
            # (e.g. API Key path may not set token_issuer)
            auth_mode = AuthMode.API_KEY if api_key_id else AuthMode.JWT_OR_SESSION
        else:
            auth_mode = AuthMode.ANONYMOUS

        scopes_raw = _get(X_API_KEY_SCOPES)
        scopes = tuple(s.strip() for s in scopes_raw.split(",") if s.strip()) if scopes_raw else ()

        return cls(
            user_id=user_id,
            oidc_sub=_get(X_OIDC_SUB),
            email=_get(X_USER_EMAIL),
            display_name=_get(X_USER_NAME),
            token_issuer=token_issuer,
            auth_mode=auth_mode,
            api_key_id=api_key_id,
            api_key_name=_get(X_API_KEY_NAME),
            api_key_scopes=scopes,
            request_id=_get(X_REQUEST_ID),
            plan_id=_get(X_PLAN_ID),
            plan_name=_get(X_PLAN_NAME),
            plan_status=_get(X_PLAN_STATUS),
            plan_features=_get(X_PLAN_FEATURES),
            plan_quotas=_get(X_PLAN_QUOTAS),
            client_context=_get(X_CLIENT_CONTEXT),
            raw_metadata=metadata,
        )

    @classmethod
    def from_http_headers(cls, headers: Dict[str, str]) -> "GatewayIdentity":
        """Create from HTTP request headers (identical to ``from_metadata``)."""
        return cls.from_metadata(headers)

    # -- repr ----------------------------------------------------------------

    def __repr__(self) -> str:
        mode = self.auth_mode.value
        uid = self.user_id or "<anonymous>"
        return f"GatewayIdentity(user_id={uid!r}, mode={mode!r})"


# ---------------------------------------------------------------------------
# Convenience interceptor
# ---------------------------------------------------------------------------

class IdentityInterceptor(grpc.aio.ServerInterceptor):
    """gRPC server interceptor that attaches a :class:`GatewayIdentity` to every call.

    Usage::

        identity_interceptor = IdentityInterceptor()

        async def serve():
            server = grpc.aio.server(interceptors=[identity_interceptor])
            # ... register services ...
            await server.start()

    Inside a handler, retrieve the identity::

        from stew.identity import GatewayIdentity

        def MyRPC(self, request, context):
            identity = GatewayIdentity.from_grpc_context(context)
    """

    async def intercept_service(
        self,
        continuation: Callable,
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        return await continuation(handler_call_details)

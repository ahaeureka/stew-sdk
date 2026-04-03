from __future__ import annotations

import grpc


class DiscoveryError(Exception):
    """Base exception for SDK gRPC client errors."""

    def __init__(self, message: str, code: grpc.StatusCode | None = None) -> None:
        super().__init__(message)
        self.code = code


class ConflictError(DiscoveryError):
    """Raised when an optimistic lock check fails (FAILED_PRECONDITION)."""


class NotFoundError(DiscoveryError):
    """Raised when a resource is not found (NOT_FOUND)."""


__all__ = ["DiscoveryError", "ConflictError", "NotFoundError"]
#!/usr/bin/env python3
"""
Descriptor auto-submit example for Stew gateway.

This script demonstrates how a business service should submit its compiled
.pb descriptor file to the Stew gateway on startup or restart.

Usage:
    python3 descriptor_submit.py \
        --gateway 127.0.0.1:3012 \
        --service my-service \
        --descriptor /app/proto/my_service.pb \
        --api-key <service-api-key>
"""

import argparse
import hashlib
import logging
import os
import sys
import time

import grpc

# Add the sdk/python directory to path if running directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stew.api.v1 import service_discovery_pb2 as sd_pb2
from stew.api.v1 import service_discovery_pb2_grpc as sd_grpc

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("descriptor_submit")


def build_channel(gateway_addr: str, api_key: str) -> grpc.Channel:
    credentials = grpc.ssl_channel_credentials() if gateway_addr.startswith("ssl:") else None
    addr = gateway_addr.lstrip("ssl:")
    call_credentials = grpc.metadata_call_credentials(
        lambda context, callback: callback([("x-api-key", api_key)], None)
    )
    if credentials:
        combined = grpc.composite_channel_credentials(credentials, call_credentials)
        return grpc.secure_channel(addr, combined)
    # Insecure channel with per-call metadata injected via interceptor
    return grpc.insecure_channel(addr)


def make_metadata(api_key: str) -> list:
    return [("x-api-key", api_key)]


def upload_descriptor(
    stub: sd_grpc.ServiceDiscoveryServiceStub,
    metadata: list,
    service_name: str,
    descriptor_data: bytes,
    descriptor_version: str,
    description: str,
    previous_version: str | None,
    force: bool,
) -> sd_pb2.UploadProtobufDescriptorResponse:
    req = sd_pb2.UploadProtobufDescriptorRequest(
        service_name=service_name,
        descriptor_data=descriptor_data,
        descriptor_version=descriptor_version,
        description=description,
        force=force,
        previous_version=previous_version or "",
    )
    return stub.UploadProtobufDescriptor(req, metadata=metadata)


def get_active_version(
    stub: sd_grpc.ServiceDiscoveryServiceStub,
    metadata: list,
    service_name: str,
) -> str | None:
    """Return the currently active descriptor version, or None if not found."""
    try:
        req = sd_pb2.ListDescriptorVersionsRequest(service_name=service_name)
        resp: sd_pb2.ListDescriptorVersionsResponse = stub.ListDescriptorVersions(
            req, metadata=metadata
        )
        for v in resp.versions:
            if v.is_active:
                return v.version
    except grpc.RpcError as exc:
        if exc.code() == grpc.StatusCode.NOT_FOUND:
            return None
        raise
    return None


def rollback_descriptor(
    stub: sd_grpc.ServiceDiscoveryServiceStub,
    metadata: list,
    service_name: str,
    target_version: str,
) -> sd_pb2.RollbackDescriptorResponse:
    req = sd_pb2.RollbackDescriptorRequest(
        service_name=service_name,
        target_version=target_version,
    )
    return stub.RollbackDescriptor(req, metadata=metadata)


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit a protobuf descriptor to Stew gateway")
    parser.add_argument("--gateway", default="127.0.0.1:3012", help="Gateway gRPC address")
    parser.add_argument("--service", required=True, help="Service name (e.g. stew.api.v1.MyService)")
    parser.add_argument("--descriptor", required=True, help="Path to compiled .pb file")
    parser.add_argument("--api-key", required=True, help="Service API key for authentication")
    parser.add_argument("--version", default="", help="Explicit version string (auto-generated if empty)")
    parser.add_argument("--description", default="", help="Human-readable description of this version")
    parser.add_argument("--force", action="store_true", help="Force overwrite, ignore compatibility warnings")
    parser.add_argument("--rollback", default="", help="Rollback to this version instead of uploading")
    args = parser.parse_args()

    descriptor_path: str = args.descriptor
    if not os.path.isfile(descriptor_path):
        log.error("descriptor file not found: %s", descriptor_path)
        return 1

    with open(descriptor_path, "rb") as fh:
        descriptor_data = fh.read()

    descriptor_hash = hashlib.sha256(descriptor_data).hexdigest()[:12]
    version = args.version or f"{int(time.time())}-{descriptor_hash}"

    channel = grpc.insecure_channel(args.gateway)
    stub = sd_grpc.ServiceDiscoveryServiceStub(channel)
    metadata = make_metadata(args.api_key)

    # --- rollback path ---
    if args.rollback:
        log.info("rolling back %s to version %s", args.service, args.rollback)
        try:
            resp = rollback_descriptor(stub, metadata, args.service, args.rollback)
        except grpc.RpcError as exc:
            log.error("rollback failed: [%s] %s", exc.code(), exc.details())
            return 1
        if resp.success:
            log.info("rollback succeeded, active version: %s", resp.active_version)
            return 0
        log.error("rollback failed: %s", resp.message)
        return 1

    # --- upload path ---
    # Fetch current active version for optimistic locking
    previous_version = get_active_version(stub, metadata, args.service)
    if previous_version:
        log.info("current active version: %s", previous_version)
    else:
        log.info("no active version found, this is a fresh upload")

    log.info(
        "uploading descriptor for %s (version=%s, size=%d bytes, sha256=...%s)",
        args.service,
        version,
        len(descriptor_data),
        descriptor_hash,
    )

    try:
        resp = upload_descriptor(
            stub,
            metadata,
            service_name=args.service,
            descriptor_data=descriptor_data,
            descriptor_version=version,
            description=args.description or f"auto-submitted at startup, hash={descriptor_hash}",
            previous_version=previous_version,
            force=args.force,
        )
    except grpc.RpcError as exc:
        log.error("upload failed: [%s] %s", exc.code(), exc.details())
        return 1

    if not resp.success:
        log.error("upload rejected: %s", resp.message)
        return 1

    log.info("upload succeeded, applied version: %s", resp.applied_version)
    log.info("discovered services: %s", list(resp.discovered_services))

    if resp.compatibility_warnings:
        log.warning("compatibility warnings detected:")
        for w in resp.compatibility_warnings:
            log.warning("  - %s", w)
        if not args.force:
            log.warning("re-run with --force to ignore warnings")

    return 0


if __name__ == "__main__":
    sys.exit(main())

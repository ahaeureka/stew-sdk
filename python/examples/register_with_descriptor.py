#!/usr/bin/env python3
"""
Service registration with embedded descriptor for Stew gateway.

This example shows the one-call path: RegisterService with the compiled .pb
included in the request. The gateway validates, stores, and loads the descriptor
atomically with service instance registration.

Usage:
    python3 register_with_descriptor.py \
        --gateway 127.0.0.1:3012 \
        --service my-service \
        --address 10.0.0.5:50051 \
        --tags version=v1.2.3,env=prod \
        --descriptor /app/proto/my_service.pb \
        --api-key <service-api-key>
"""

import argparse
import logging
import os
import sys
import time

import grpc

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stew.api.v1 import service_discovery_pb2 as sd_pb2
from stew.api.v1 import service_discovery_pb2_grpc as sd_grpc

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("register_with_descriptor")

_HEARTBEAT_INTERVAL = 30  # seconds


def parse_tags(tags_str: str) -> dict:
    result: dict[str, str] = {}
    for pair in tags_str.split(","):
        pair = pair.strip()
        if not pair:
            continue
        if "=" in pair:
            k, v = pair.split("=", 1)
            result[k.strip()] = v.strip()
        else:
            result[pair] = "true"
    return result


def register(
    stub: sd_grpc.ServiceDiscoveryServiceStub,
    metadata: list,
    service_name: str,
    address: str,
    tags: dict,
    descriptor_data: bytes | None,
) -> sd_pb2.RegisterServiceResponse:
    instance = sd_pb2.ServiceInstance(
        service_name=service_name,
        address=address,
        tags=tags,
        status="healthy",
    )
    req = sd_pb2.RegisterServiceRequest(
        instance=instance,
        protobuf_descriptor=descriptor_data or b"",
    )
    return stub.RegisterService(req, metadata=metadata)


def keepalive_loop(
    stub: sd_grpc.ServiceDiscoveryServiceStub,
    metadata: list,
    service_name: str,
    instance_id: str,
    interval: int,
) -> None:
    """Send periodic health updates to keep the service instance alive."""
    log.info("starting keepalive loop (interval=%ds)", interval)
    while True:
        time.sleep(interval)
        try:
            req = sd_pb2.UpdateServiceHealthRequest(
                service_name=service_name,
                instance_id=instance_id,
                status="healthy",
            )
            stub.UpdateServiceHealth(req, metadata=metadata)
            log.debug("keepalive sent for instance %s", instance_id)
        except grpc.RpcError as exc:
            log.warning("keepalive failed: [%s] %s", exc.code(), exc.details())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Register a service instance with its protobuf descriptor"
    )
    parser.add_argument("--gateway", default="127.0.0.1:3012")
    parser.add_argument("--service", required=True, help="Service name")
    parser.add_argument("--address", required=True, help="gRPC listen address of this instance")
    parser.add_argument("--tags", default="", help="Comma-separated key=value tags")
    parser.add_argument("--descriptor", default="", help="Path to compiled .pb file (optional)")
    parser.add_argument("--api-key", required=True, help="Service API key")
    parser.add_argument(
        "--keepalive",
        action="store_true",
        help="Stay alive and send periodic health updates",
    )
    args = parser.parse_args()

    descriptor_data: bytes | None = None
    if args.descriptor:
        if not os.path.isfile(args.descriptor):
            log.error("descriptor file not found: %s", args.descriptor)
            return 1
        with open(args.descriptor, "rb") as fh:
            descriptor_data = fh.read()
        log.info("loaded descriptor from %s (%d bytes)", args.descriptor, len(descriptor_data))

    metadata = [("x-api-key", args.api_key)]
    channel = grpc.insecure_channel(args.gateway)
    stub = sd_grpc.ServiceDiscoveryServiceStub(channel)

    try:
        resp = register(
            stub,
            metadata,
            service_name=args.service,
            address=args.address,
            tags=parse_tags(args.tags),
            descriptor_data=descriptor_data,
        )
    except grpc.RpcError as exc:
        log.error("registration failed: [%s] %s", exc.code(), exc.details())
        return 1

    if not resp.success:
        log.error("registration rejected: %s", resp.message)
        return 1

    log.info("registered successfully, instance_id=%s", resp.instance_id)

    if args.keepalive:
        import threading

        t = threading.Thread(
            target=keepalive_loop,
            args=(stub, metadata, args.service, resp.instance_id, _HEARTBEAT_INTERVAL),
            daemon=True,
        )
        t.start()
        log.info("press Ctrl+C to deregister and exit")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            log.info("deregistering instance %s", resp.instance_id)
            try:
                stub.DeregisterService(
                    sd_pb2.DeregisterServiceRequest(
                        service_name=args.service,
                        instance_id=resp.instance_id,
                    ),
                    metadata=metadata,
                )
                log.info("deregistered")
            except grpc.RpcError as exc:
                log.warning("deregistration failed: [%s] %s", exc.code(), exc.details())

    return 0


if __name__ == "__main__":
    sys.exit(main())

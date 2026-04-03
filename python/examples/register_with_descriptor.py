#!/usr/bin/env python3
"""
Gateway client demo for Stew gateway.

The SDK appends one business-managed endpoint into gateway discovery, persists
the generated endpoint_id locally, uploads the .pb descriptor, and keeps both
heartbeat and descriptor refresh loops running.

Usage:
        APP_SECRET=ak_xxx python3 keepalive_demo.py \
                --gateway 127.0.0.1:3012 \
                --service stew.api.v1.OrderService \
                --descriptor ./order_service.pb \
                --address 127.0.0.1 \
                --port 50051
"""

import argparse
import asyncio
import logging
import os
import signal
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stew import Endpoint, GatewayClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("keepalive_demo")


_stop_event = asyncio.Event()


def _on_signal(*_args: object) -> None:
    _stop_event.set()


async def run(
    gateway: str,
    app_secret: str,
    service: str,
    interval: int,
    descriptor_path: str,
    descriptor_refresh_interval: int,
    address: str,
    port: int,
    weight: int,
    endpoint_state_path: str,
) -> None:
    async with GatewayClient(
        gateway,
        app_secret=app_secret,
        service_name=service,
        pb_path=descriptor_path,
        keepalive_interval=interval,
        local_endpoint=Endpoint(address=address, port=port, weight=weight),
        endpoint_state_path=endpoint_state_path,
        descriptor_refresh_interval=descriptor_refresh_interval,
    ) as client:
        await client.registered.wait()
        log.info("gateway client started. Press Ctrl+C to stop.")
        await _stop_event.wait()
        log.info("gateway client stopping")


def main() -> int:
    parser = argparse.ArgumentParser(description="Keepalive demo for Stew gateway")
    parser.add_argument("--gateway", default=os.environ.get("GATEWAY_ADDR", "127.0.0.1:3012"))
    parser.add_argument("--service", required=True, help="Service name (e.g. stew.api.v1.OrderService)")
    parser.add_argument("--descriptor", required=True, help="Path to compiled .pb file")
    parser.add_argument("--address", required=True, help="Business service bind address")
    parser.add_argument("--port", required=True, type=int, help="Business service bind port")
    parser.add_argument("--weight", type=int, default=1, help="Endpoint weight / priority")
    parser.add_argument(
        "--endpoint-state-path",
        default="",
        help="Local file for persisting endpoint_id binding (defaults to {descriptor}.endpoint.json).",
    )
    parser.add_argument(
        "--app-secret",
        default=os.environ.get("APP_SECRET", ""),
        help="Service credential.  Defaults to APP_SECRET env var.",
    )
    parser.add_argument("--interval", type=int, default=30, help="Heartbeat interval in seconds")
    parser.add_argument(
        "--descriptor-refresh-interval",
        type=int,
        default=30,
        help="Poll interval in seconds for dynamic .pb refresh; 0 disables it.",
    )
    args = parser.parse_args()

    if not args.app_secret:
        log.error("app_secret is required (--app-secret or APP_SECRET env var)")
        return 1
    if not os.path.isfile(args.descriptor):
        log.error("descriptor file not found: %s", args.descriptor)
        return 1

    loop = asyncio.new_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _on_signal)

    try:
        loop.run_until_complete(
            run(
                args.gateway,
                args.app_secret,
                args.service,
                args.interval,
                args.descriptor,
                args.descriptor_refresh_interval,
                args.address,
                args.port,
                args.weight,
                args.endpoint_state_path,
            )
        )
    finally:
        loop.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Keepalive demo for Stew gateway (admin-first model).

Service registration (RegisterService / DeregisterService) is an admin-only
operation performed from the management UI.  The business service only needs
to:
  1. Upload its .pb descriptor on startup (see descriptor_submit.py).
  2. Send periodic heartbeats so the gateway knows the instance is healthy.

This script demonstrates the heartbeat / keepalive workflow using the
high-level DiscoveryClient.

Usage:
    APP_SECRET=ak_xxx python3 keepalive_demo.py \
        --gateway 127.0.0.1:3012 \
        --service stew.api.v1.OrderService \
        --instance order-prod-1
"""

import argparse
import asyncio
import logging
import os
import signal
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stew import DiscoveryClient, DiscoveryError
from stew.api.v1 import service_discovery_pb2 as _pb

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("keepalive_demo")


_stop_event = asyncio.Event()


def _on_signal(*_args: object) -> None:
    _stop_event.set()


async def run(gateway: str, app_secret: str, service: str, instance_id: str, interval: int) -> None:
    def on_keepalive_error(e: DiscoveryError) -> None:
        log.warning("keepalive error: %s", e)

    async with DiscoveryClient(gateway, app_secret=app_secret) as client:
        # Show current instances so the user can confirm the instance_id
        try:
            instances = await client.get_instances(service, healthy_only=False)
            log.info("registered instances for %s:", service)
            for inst in instances:
                log.info("  instance_id=%s  status=%s", inst["instance_id"], inst["status"])
        except DiscoveryError as e:
            log.warning("could not list instances: %s", e)

        await client.start_keepalive(
            service_name=service,
            instance_id=instance_id,
            interval=interval,
            on_error=on_keepalive_error,
        )
        log.info("keepalive started (interval=%ds).  Press Ctrl+C to stop.", interval)

        await _stop_event.wait()
        client.stop_keepalive(service, instance_id)
        log.info("keepalive stopped")


def main() -> int:
    parser = argparse.ArgumentParser(description="Keepalive demo for Stew gateway")
    parser.add_argument("--gateway", default=os.environ.get("GATEWAY_ADDR", "127.0.0.1:3012"))
    parser.add_argument("--service", required=True, help="Service name (e.g. stew.api.v1.OrderService)")
    parser.add_argument("--instance", required=True, help="Instance ID configured in the admin UI")
    parser.add_argument(
        "--app-secret",
        default=os.environ.get("APP_SECRET", ""),
        help="Service credential.  Defaults to APP_SECRET env var.",
    )
    parser.add_argument("--interval", type=int, default=30, help="Heartbeat interval in seconds")
    args = parser.parse_args()

    if not args.app_secret:
        log.error("app_secret is required (--app-secret or APP_SECRET env var)")
        return 1

    loop = asyncio.new_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _on_signal)

    try:
        loop.run_until_complete(
            run(args.gateway, args.app_secret, args.service, args.instance, args.interval)
        )
    finally:
        loop.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Descriptor submit tool for Stew gateway.

Uploads a compiled .pb descriptor file to the gateway using the high-level
SyncDiscoveryClient.  Suitable as a Docker CMD / Kubernetes init-container
that runs once at service startup before the main process starts.

Usage:
    APP_SECRET=ak_xxx python3 descriptor_submit.py \
        --gateway 127.0.0.1:3012 \
        --service stew.api.v1.OrderService \
        --descriptor /app/proto/order_service.pb

    # Rollback to a previous version:
    APP_SECRET=ak_xxx python3 descriptor_submit.py \
        --gateway 127.0.0.1:3012 \
        --service stew.api.v1.OrderService \
        --descriptor /dev/null \
        --rollback v2.0.0
"""

import argparse
import logging
import os
import sys

# Add the sdk/python directory to path if running directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stew import SyncDiscoveryClient, ConflictError, DiscoveryError, NotFoundError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("descriptor_submit")


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit a protobuf descriptor to Stew gateway")
    parser.add_argument("--gateway", default=os.environ.get("GATEWAY_ADDR", "127.0.0.1:3012"))
    parser.add_argument("--service", required=True, help="Service name (e.g. stew.api.v1.MyService)")
    parser.add_argument("--descriptor", required=True, help="Path to compiled .pb file")
    parser.add_argument(
        "--app-secret",
        default=os.environ.get("APP_SECRET", ""),
        help="Service credential (app_secret).  Defaults to APP_SECRET env var.",
    )
    parser.add_argument("--version", default="", help="Explicit version tag (auto-generated if empty)")
    parser.add_argument("--description", default="", help="Human-readable description of this version")
    parser.add_argument("--force", action="store_true", help="Ignore compatibility warnings")
    parser.add_argument("--rollback", default="", help="Rollback to this version instead of uploading")
    args = parser.parse_args()

    if not args.app_secret:
        log.error("app_secret is required (--app-secret or APP_SECRET env var)")
        return 1

    with SyncDiscoveryClient(args.gateway, app_secret=args.app_secret) as client:
        # --- rollback path ---
        if args.rollback:
            log.info("rolling back %s to version %s", args.service, args.rollback)
            try:
                active = client.rollback_descriptor(args.service, args.rollback)
                log.info("rollback succeeded, active version: %s", active)
                return 0
            except NotFoundError as e:
                log.error("target version not found: %s", e)
                return 1
            except DiscoveryError as e:
                log.error("rollback failed: %s", e)
                return 1

        # --- upload path ---
        if not os.path.isfile(args.descriptor):
            log.error("descriptor file not found: %s", args.descriptor)
            return 1

        # Fetch current active version for optimistic locking.
        # ConflictError is raised when another deployment won the race — treat
        # as idempotent success so parallel pods don't fail each other.
        active = client.get_active_version(args.service)
        log.info("current active version: %s", active or "(none)")

        try:
            result = client.upload_descriptor_from_file(
                service_name=args.service,
                pb_path=args.descriptor,
                version=args.version,
                description=args.description or "auto-submitted at startup",
                previous_version=active or "",
                force=args.force,
            )
        except ConflictError as e:
            # Another instance already submitted a newer descriptor; not an error.
            log.info("descriptor already updated by concurrent deployment: %s", e)
            return 0
        except DiscoveryError as e:
            log.error("upload failed: %s", e)
            return 1

        log.info("upload succeeded, applied version: %s", result["applied_version"])
        log.info("discovered services: %s", result["discovered_services"])

        for w in result["compatibility_warnings"]:
            log.warning("compat warning: %s", w)
        if result["compatibility_warnings"] and not args.force:
            log.warning("re-run with --force to ignore warnings")

    return 0


if __name__ == "__main__":
    sys.exit(main())

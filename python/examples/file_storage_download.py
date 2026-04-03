#!/usr/bin/env python3
"""Download a file from Stew via gRPC chunked download."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stew import DownloadProgress, FileStorageClient

log = logging.getLogger("file_storage_download")


def _format_bytes(value: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f}{unit}" if unit != "B" else f"{int(size)}{unit}"
        size /= 1024
    return f"{value}B"


def _build_progress_logger() -> callable:
    def _on_progress(progress: DownloadProgress) -> None:
        log.info(
            "downloaded chunk %s/%s (%s/%s)",
            progress.chunk_index,
            progress.total_chunks,
            _format_bytes(progress.downloaded_bytes),
            _format_bytes(progress.total_bytes),
        )

    return _on_progress


async def run(args: argparse.Namespace) -> int:
    async with FileStorageClient(
        args.gateway,
        app_secret=args.app_secret,
        timeout=args.timeout,
        use_tls=args.tls,
    ) as client:
        saved = await client.download_file_to_path(
            file_id=args.file_id,
            output_path=args.output,
            chunk_size=args.chunk_size,
            verify_integrity=args.verify_integrity,
            replace_existing=args.replace_existing,
            on_progress=_build_progress_logger() if args.show_progress else None,
        )

    log.info(
        "download complete: %s (%s, etag=%s)",
        saved.path,
        _format_bytes(saved.bytes_written),
        saved.etag or "",
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Download a file from Stew via gRPC")
    parser.add_argument("--gateway", default=os.environ.get("GATEWAY_ADDR", "127.0.0.1:3012"))
    parser.add_argument("--file-id", required=True, help="File ID to download")
    parser.add_argument(
        "--output",
        default="",
        help="Output path. Defaults to server filename and streams directly to disk.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1024 * 1024,
        help="Chunk size in bytes for gRPC range download.",
    )
    parser.add_argument(
        "--app-secret",
        default=os.environ.get("APP_SECRET", ""),
        help="Service credential. Defaults to APP_SECRET env var.",
    )
    parser.add_argument(
        "--verify-integrity",
        action="store_true",
        help="Verify the assembled download with server-side checksum confirmation.",
    )
    parser.add_argument(
        "--show-progress",
        action="store_true",
        help="Log per-chunk download progress.",
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Overwrite the final output file when it already exists.",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="Per-RPC timeout in seconds.")
    parser.add_argument("--tls", action="store_true", help="Connect with TLS.")
    args = parser.parse_args()

    if not args.app_secret:
        log.error("app_secret is required (--app-secret or APP_SECRET env var)")
        return 1

    return asyncio.run(run(args))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    raise SystemExit(main())
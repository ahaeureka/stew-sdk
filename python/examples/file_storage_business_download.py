#!/usr/bin/env python3
"""Business-oriented file download flow using gRPC chunked download."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stew import DownloadProgress, FileStorageClient

log = logging.getLogger("file_storage_business_download")


def _format_bytes(value: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f}{unit}" if unit != "B" else f"{int(size)}{unit}"
        size /= 1024
    return f"{value}B"


def _safe_folder(folder: str) -> Path:
    cleaned = folder.strip().strip("/")
    return Path(cleaned) if cleaned else Path()


def _build_progress_logger(file_id: str):
    def _on_progress(progress: DownloadProgress) -> None:
        log.info(
            "file=%s chunk=%s/%s downloaded=%s/%s",
            file_id,
            progress.chunk_index,
            progress.total_chunks,
            _format_bytes(progress.downloaded_bytes),
            _format_bytes(progress.total_bytes),
        )

    return _on_progress


async def run(args: argparse.Namespace) -> int:
    business_root = Path(args.business_root).expanduser().resolve()
    business_root.mkdir(parents=True, exist_ok=True)

    async with FileStorageClient(
        args.gateway,
        app_secret=args.app_secret,
        timeout=args.timeout,
        use_tls=args.tls,
    ) as client:
        info = await client.get_file_info(file_id=args.file_id)
        log.info(
            "file info: id=%s name=%s size=%s folder=%s checksum=%s",
            info.id,
            info.filename,
            _format_bytes(int(info.file_size or 0)),
            info.folder or "/",
            info.checksum or "",
        )

        relative_dir = _safe_folder(info.folder or "")
        filename = info.filename or f"{args.file_id}.bin"
        target_path = business_root / relative_dir / filename

        saved = await client.download_file_to_path(
            file_id=args.file_id,
            output_path=str(target_path),
            file_size=int(info.file_size or 0),
            content_type=info.content_type or "application/octet-stream",
            chunk_size=args.chunk_size,
            verify_integrity=True,
            on_progress=_build_progress_logger(args.file_id),
            resume=True,
            replace_existing=args.replace_existing,
        )

    log.info(
        "business file ready: path=%s bytes=%s content_type=%s etag=%s",
        saved.path,
        _format_bytes(saved.bytes_written),
        saved.content_type,
        saved.etag or "",
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Query file info and download to a business directory via gRPC"
    )
    parser.add_argument("--gateway", default=os.environ.get("GATEWAY_ADDR", "127.0.0.1:3012"))
    parser.add_argument("--file-id", required=True, help="File ID to download")
    parser.add_argument(
        "--business-root",
        required=True,
        help="Root directory for business-side files. File folder/name are appended automatically.",
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Overwrite the final business file when it already exists.",
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
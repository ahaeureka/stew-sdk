"""Stew Gateway file storage gRPC clients."""

from __future__ import annotations

import asyncio
import hashlib
import inspect
import os
from collections.abc import AsyncIterable, Iterable, Sequence
from dataclasses import dataclass
from typing import Any, Callable

import grpc
import grpc.aio

from stew.api.v1 import file_storage_model as _fs_model
from stew.api.v1 import file_storage_pb2 as _fs_pb
from stew.api.v1 import file_storage_pb2_grpc as _fs_grpc

from ._discovery.errors import DiscoveryError
from ._discovery.helpers import (
    AioGatewayClientBase,
    MetadataEntry,
    SyncGatewayClientBase,
    wrap_rpc_error,
)

DEFAULT_CHUNK_SIZE = 64 * 1024
FileStorageError = DiscoveryError
UploadSource = bytes | bytearray | memoryview | Iterable[bytes] | AsyncIterable[bytes]
PartEtagInput = _fs_model.PartEtag | _fs_pb.PartEtag | tuple[int, str]


@dataclass
class DownloadedFile:
    data: bytes
    content_type: str
    filename: str = ""
    content_disposition: str = ""
    etag: str = ""
    metadata: _fs_model.DownloadFileHttpMetadata | None = None


@dataclass
class DownloadedFileChunk:
    data: bytes
    chunk_index: int
    total_chunks: int
    start: int
    end: int
    total_size: int
    content_type: str
    filename: str = ""
    content_disposition: str = ""
    etag: str = ""
    content_range: str = ""
    metadata: _fs_model.DownloadFileHttpMetadata | None = None


@dataclass
class DownloadProgress:
    downloaded_bytes: int
    total_bytes: int
    chunk_index: int
    total_chunks: int


@dataclass
class SavedDownloadedFile:
    path: str
    bytes_written: int
    content_type: str
    filename: str = ""
    content_disposition: str = ""
    etag: str = ""
    metadata: _fs_model.DownloadFileHttpMetadata | None = None


def _coerce_protobuf_message(value: Any, message_type: type[Any]) -> Any:
    if isinstance(value, message_type):
        return value
    if hasattr(value, "to_protobuf"):
        message = value.to_protobuf()
        if isinstance(message, message_type):
            return message
    raise TypeError(f"Expected {message_type.__name__}, got {type(value).__name__}")


def _normalize_chunk(chunk: bytes | bytearray | memoryview) -> bytes:
    if isinstance(chunk, bytes):
        return chunk
    return bytes(chunk)


async def _iter_chunks(data: UploadSource, *, chunk_size: int) -> AsyncIterable[bytes]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if isinstance(data, (bytes, bytearray, memoryview)):
        raw = _normalize_chunk(data)
        for start in range(0, len(raw), chunk_size):
            yield raw[start:start + chunk_size]
        return

    if hasattr(data, "__aiter__"):
        async for chunk in data:  # type: ignore[union-attr]
            normalized = _normalize_chunk(chunk)
            if normalized:
                yield normalized
        return

    for chunk in data:  # type: ignore[union-attr]
        normalized = _normalize_chunk(chunk)
        if normalized:
            yield normalized


def _extract_download_metadata(
    response: Any,
) -> _fs_model.DownloadFileHttpMetadata | None:
    for extension in response.extensions:
        metadata = _fs_pb.DownloadFileHttpMetadata()
        if extension.Unpack(metadata):
            return _fs_model.DownloadFileHttpMetadata.from_protobuf(metadata)
    return None


def _coerce_part_etag(value: PartEtagInput) -> _fs_pb.PartEtag:
    if isinstance(value, tuple):
        part_number, etag = value
        return _fs_pb.PartEtag(part_number=part_number, etag=etag)
    return _coerce_protobuf_message(value, _fs_pb.PartEtag)


def _metadata_to_dict(metadata: Any) -> dict[str, str]:
    if metadata is None:
        return {}

    result: dict[str, str] = {}
    for key, value in metadata:
        result[str(key)] = value if isinstance(value, str) else value.decode("utf-8")
    return result


def _parse_content_range_total(content_range: str) -> int | None:
    if not content_range or "/" not in content_range:
        return None
    total = content_range.rsplit("/", maxsplit=1)[-1]
    if total == "*":
        return None
    try:
        return int(total)
    except ValueError:
        return None


async def _maybe_call_progress(
    callback: Callable[[DownloadProgress], Any] | None,
    progress: DownloadProgress,
) -> None:
    if callback is None:
        return

    result = callback(progress)
    if inspect.isawaitable(result):
        await result


def _chunk_number_for_offset(offset: int, chunk_size: int) -> int:
    return (offset // chunk_size) + 1


def _iter_range_windows(
    *,
    start_offset: int,
    total_size: int,
    chunk_size: int,
) -> Iterable[tuple[int, int, int]]:
    start = start_offset
    while start < total_size:
        chunk_index = _chunk_number_for_offset(start, chunk_size)
        chunk_boundary_end = min(chunk_index * chunk_size, total_size) - 1
        yield start, chunk_boundary_end, chunk_index
        start = chunk_boundary_end + 1


def _update_hasher_from_file(hasher: hashlib._Hash, file_path: str) -> None:
    with open(file_path, "rb") as fh:
        while True:
            block = fh.read(1024 * 1024)
            if not block:
                return
            hasher.update(block)


def _ensure_output_path_is_writable(output_path: str, *, replace_existing: bool) -> None:
    if not os.path.exists(output_path):
        return

    if not replace_existing:
        raise FileExistsError(
            f"Output file already exists: {output_path}. "
            "Pass replace_existing=True to overwrite it."
        )


class FileStorageClient(AioGatewayClientBase[_fs_grpc.FileStorageServiceStub]):
    """Async gRPC client for stew.api.v1.FileStorageService."""

    def _create_stub(self, channel: grpc.aio.Channel) -> _fs_grpc.FileStorageServiceStub:
        return _fs_grpc.FileStorageServiceStub(channel)

    async def _download_call(
        self,
        message: _fs_pb.DownloadFileRequest,
        *,
        business_id: str = "",
        extra_metadata: Sequence[tuple[str, str]] = (),
    ) -> tuple[Any, dict[str, str]]:
        call = self._s.DownloadFile(
            message,
            metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
            timeout=self._timeout,
        )
        response = await self._call(call)

        if hasattr(call, "initial_metadata"):
            metadata = _metadata_to_dict(await call.initial_metadata())
        else:
            metadata = {}

        return response, metadata

    async def verify_download_checksum(
        self,
        *,
        file_id: str,
        checksum: str,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> bool:
        response, response_headers = await self._download_call(
            _fs_pb.DownloadFileRequest(file_id=file_id, checksum=checksum, verify_only=True),
            business_id=business_id,
            extra_metadata=extra_metadata,
        )
        _ = response
        status_code = response_headers.get("x-http-status", "")
        if status_code == "204":
            return True
        if status_code == "412":
            return False
        raise FileStorageError(
            f"Checksum verification rejected with HTTP status {status_code or 'unknown'}",
            code=grpc.StatusCode.UNKNOWN,
        )

    async def _verify_integrity_or_raise(
        self,
        *,
        file_id: str,
        checksum: str,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> None:
        verified = await self.verify_download_checksum(
            file_id=file_id,
            checksum=checksum,
            business_id=business_id,
            extra_metadata=extra_metadata,
        )
        if not verified:
            raise FileStorageError(
                "Downloaded file integrity verification failed",
                code=grpc.StatusCode.DATA_LOSS,
            )

    async def _call(self, coro):  # type: ignore[no-untyped-def]
        try:
            return await coro
        except grpc.RpcError as exc:
            raise wrap_rpc_error(exc) from exc

    async def upload_file(
        self,
        *,
        data: UploadSource,
        filename: str = "",
        content_type: str = "",
        folder: str = "/",
        business_context: str = "",
        metadata: _fs_model.UploadFileMetadata | _fs_pb.UploadFileMetadata | None = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _fs_model.UploadFileResponse:
        metadata_message = (
            _coerce_protobuf_message(metadata, _fs_pb.UploadFileMetadata)
            if metadata is not None
            else _fs_pb.UploadFileMetadata(
                filename=filename,
                content_type=content_type,
                folder=folder,
                business_context=business_context,
            )
        )

        async def request_iter() -> AsyncIterable[_fs_pb.UploadFileRequest]:
            yield _fs_pb.UploadFileRequest(metadata=metadata_message)
            async for chunk in _iter_chunks(data, chunk_size=chunk_size):
                yield _fs_pb.UploadFileRequest(chunk_data=chunk)

        response: _fs_pb.UploadFileResponse = await self._call(
            self._s.UploadFile(
                request_iter(),
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _fs_model.UploadFileResponse.from_protobuf(response)

    async def init_resumable_upload(
        self,
        request: _fs_model.InitResumableUploadRequest | _fs_pb.InitResumableUploadRequest | None = None,
        *,
        filename: str = "",
        content_type: str = "",
        folder: str = "/",
        total_size: int = 0,
        part_size: int = 0,
        business_context: str = "",
        checksum: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _fs_model.InitResumableUploadResponse:
        message = (
            _coerce_protobuf_message(request, _fs_pb.InitResumableUploadRequest)
            if request is not None
            else _fs_pb.InitResumableUploadRequest(
                filename=filename,
                content_type=content_type,
                folder=folder,
                total_size=total_size,
                part_size=part_size,
                business_context=business_context,
                checksum=checksum,
            )
        )
        response: _fs_pb.InitResumableUploadResponse = await self._call(
            self._s.InitResumableUpload(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _fs_model.InitResumableUploadResponse.from_protobuf(response)

    async def upload_part(
        self,
        *,
        upload_id: str,
        part_number: int,
        data: UploadSource,
        header: _fs_model.UploadPartHeader | _fs_pb.UploadPartHeader | None = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _fs_model.UploadPartResponse:
        header_message = (
            _coerce_protobuf_message(header, _fs_pb.UploadPartHeader)
            if header is not None
            else _fs_pb.UploadPartHeader(upload_id=upload_id, part_number=part_number)
        )

        async def request_iter() -> AsyncIterable[_fs_pb.UploadPartRequest]:
            yield _fs_pb.UploadPartRequest(header=header_message)
            async for chunk in _iter_chunks(data, chunk_size=chunk_size):
                yield _fs_pb.UploadPartRequest(chunk_data=chunk)

        response: _fs_pb.UploadPartResponse = await self._call(
            self._s.UploadPart(
                request_iter(),
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _fs_model.UploadPartResponse.from_protobuf(response)

    async def complete_resumable_upload(
        self,
        request: _fs_model.CompleteResumableUploadRequest | _fs_pb.CompleteResumableUploadRequest | None = None,
        *,
        upload_id: str = "",
        parts: Sequence[PartEtagInput] = (),
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _fs_model.UploadFileResponse:
        message = (
            _coerce_protobuf_message(request, _fs_pb.CompleteResumableUploadRequest)
            if request is not None
            else _fs_pb.CompleteResumableUploadRequest(
                upload_id=upload_id,
                parts=[_coerce_part_etag(part) for part in parts],
            )
        )
        response: _fs_pb.UploadFileResponse = await self._call(
            self._s.CompleteResumableUpload(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _fs_model.UploadFileResponse.from_protobuf(response)

    async def abort_resumable_upload(
        self,
        upload_id: str = "",
        request: _fs_model.AbortResumableUploadRequest | _fs_pb.AbortResumableUploadRequest | None = None,
        *,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> None:
        message = (
            _coerce_protobuf_message(request, _fs_pb.AbortResumableUploadRequest)
            if request is not None
            else _fs_pb.AbortResumableUploadRequest(upload_id=upload_id)
        )
        await self._call(
            self._s.AbortResumableUpload(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )

    async def get_upload_status(
        self,
        upload_id: str = "",
        request: _fs_model.GetUploadStatusRequest | _fs_pb.GetUploadStatusRequest | None = None,
        *,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _fs_model.GetUploadStatusResponse:
        message = (
            _coerce_protobuf_message(request, _fs_pb.GetUploadStatusRequest)
            if request is not None
            else _fs_pb.GetUploadStatusRequest(upload_id=upload_id)
        )
        response: _fs_pb.GetUploadStatusResponse = await self._call(
            self._s.GetUploadStatus(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _fs_model.GetUploadStatusResponse.from_protobuf(response)

    async def download_file(
        self,
        *,
        file_id: str,
        checksum: str = "",
        verify_only: bool = False,
        verify_integrity: bool = False,
        on_progress: Callable[[DownloadProgress], Any] | None = None,
        request: _fs_model.DownloadFileRequest | _fs_pb.DownloadFileRequest | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> DownloadedFile:
        message = (
            _coerce_protobuf_message(request, _fs_pb.DownloadFileRequest)
            if request is not None
            else _fs_pb.DownloadFileRequest(
                file_id=file_id,
                checksum=checksum,
                verify_only=verify_only,
            )
        )
        response, metadata_headers = await self._download_call(
            message,
            business_id=business_id,
            extra_metadata=extra_metadata,
        )
        metadata = _extract_download_metadata(response)
        data = response.data
        total_bytes = int(metadata_headers.get("content-length", str(len(data)))) if data else 0
        if not verify_only:
            await _maybe_call_progress(
                on_progress,
                DownloadProgress(
                    downloaded_bytes=len(data),
                    total_bytes=total_bytes or len(data),
                    chunk_index=1,
                    total_chunks=1,
                ),
            )
        if verify_integrity and not verify_only:
            await self._verify_integrity_or_raise(
                file_id=file_id,
                checksum=hashlib.sha256(data).hexdigest(),
                business_id=business_id,
                extra_metadata=extra_metadata,
            )

        return DownloadedFile(
            data=data,
            content_type=response.content_type,
            filename=metadata.filename if metadata is not None and metadata.filename else "",
            content_disposition=(
                metadata.content_disposition
                if metadata is not None and metadata.content_disposition
                else ""
            ),
            etag=metadata.etag if metadata is not None and metadata.etag else "",
            metadata=metadata,
        )

    async def iter_download_file_chunks(
        self,
        *,
        file_id: str,
        chunk_size: int = 1024 * 1024,
        file_size: int | None = None,
        content_type: str = "",
        start_offset: int = 0,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> AsyncIterable[DownloadedFileChunk]:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")
        if start_offset < 0:
            raise ValueError("start_offset must be greater than or equal to 0")

        resolved_file_size = file_size
        resolved_content_type = content_type
        if resolved_file_size is None or resolved_file_size <= 0:
            info = await self.get_file_info(
                file_id=file_id,
                business_id=business_id,
                extra_metadata=extra_metadata,
            )
            resolved_file_size = int(info.file_size or 0)
            if not resolved_content_type:
                resolved_content_type = info.content_type or "application/octet-stream"

        if resolved_file_size <= 0:
            raise ValueError("File size is unknown, cannot download in chunks.")
        if start_offset > resolved_file_size:
            raise ValueError("start_offset exceeds file size")

        total_chunks = (resolved_file_size + chunk_size - 1) // chunk_size
        for start, end, chunk_index in _iter_range_windows(
            start_offset=start_offset,
            total_size=resolved_file_size,
            chunk_size=chunk_size,
        ):
            request = _fs_pb.DownloadFileRequest(file_id=file_id)
            response, response_headers = await self._download_call(
                request,
                business_id=business_id,
                extra_metadata=[*extra_metadata, ("range", f"bytes={start}-{end}")],
            )
            metadata = _extract_download_metadata(response)
            status_code = response_headers.get("x-http-status", "206")
            if status_code not in {"200", "206"}:
                raise FileStorageError(
                    f"Chunk download rejected with HTTP status {status_code}",
                    code=grpc.StatusCode.UNKNOWN,
                )

            effective_total_size = _parse_content_range_total(
                response_headers.get("content-range", "")
            ) or resolved_file_size

            yield DownloadedFileChunk(
                data=response.data,
                chunk_index=chunk_index,
                total_chunks=total_chunks,
                start=start,
                end=end,
                total_size=effective_total_size,
                content_type=response.content_type or resolved_content_type,
                filename=metadata.filename if metadata is not None and metadata.filename else "",
                content_disposition=(
                    metadata.content_disposition
                    if metadata is not None and metadata.content_disposition
                    else ""
                ),
                etag=metadata.etag if metadata is not None and metadata.etag else "",
                content_range=response_headers.get("content-range", ""),
                metadata=metadata,
            )

    async def download_file_in_chunks(
        self,
        *,
        file_id: str,
        chunk_size: int = 1024 * 1024,
        file_size: int | None = None,
        content_type: str = "",
        verify_integrity: bool = False,
        on_progress: Callable[[DownloadProgress], Any] | None = None,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> DownloadedFile:
        parts: list[bytes] = []
        resolved_content_type = content_type
        filename = ""
        content_disposition = ""
        etag = ""
        metadata: _fs_model.DownloadFileHttpMetadata | None = None
        downloaded_bytes = 0

        async for chunk in self.iter_download_file_chunks(
            file_id=file_id,
            chunk_size=chunk_size,
            file_size=file_size,
            content_type=content_type,
            business_id=business_id,
            extra_metadata=extra_metadata,
        ):
            parts.append(chunk.data)
            downloaded_bytes += len(chunk.data)
            if not resolved_content_type:
                resolved_content_type = chunk.content_type
            if chunk.filename:
                filename = chunk.filename
            if chunk.content_disposition:
                content_disposition = chunk.content_disposition
            if chunk.etag:
                etag = chunk.etag
            if chunk.metadata is not None:
                metadata = chunk.metadata
            await _maybe_call_progress(
                on_progress,
                DownloadProgress(
                    downloaded_bytes=downloaded_bytes,
                    total_bytes=chunk.total_size,
                    chunk_index=chunk.chunk_index,
                    total_chunks=chunk.total_chunks,
                ),
            )

        data = b"".join(parts)
        if verify_integrity:
            await self._verify_integrity_or_raise(
                file_id=file_id,
                checksum=hashlib.sha256(data).hexdigest(),
                business_id=business_id,
                extra_metadata=extra_metadata,
            )

        return DownloadedFile(
            data=data,
            content_type=resolved_content_type or "application/octet-stream",
            filename=filename,
            content_disposition=content_disposition,
            etag=etag,
            metadata=metadata,
        )

    async def download_file_to_path(
        self,
        *,
        file_id: str,
        output_path: str = "",
        chunk_size: int = 1024 * 1024,
        file_size: int | None = None,
        content_type: str = "",
        verify_integrity: bool = False,
        on_progress: Callable[[DownloadProgress], Any] | None = None,
        resume: bool = True,
        replace_existing: bool = False,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> SavedDownloadedFile:
        info: _fs_model.FileInfo | None = None
        if file_size is None or file_size <= 0 or not content_type or not output_path:
            info = await self.get_file_info(
                file_id=file_id,
                business_id=business_id,
                extra_metadata=extra_metadata,
            )

        resolved_file_size = int(file_size or (info.file_size if info is not None else 0) or 0)
        resolved_content_type = content_type or (
            (info.content_type if info is not None else "") or "application/octet-stream"
        )
        filename = (info.filename if info is not None else "") or ""
        resolved_output_path = output_path or filename or f"{file_id}.bin"

        parent = os.path.dirname(os.path.abspath(resolved_output_path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        _ensure_output_path_is_writable(
            resolved_output_path,
            replace_existing=replace_existing,
        )
        tmp_path = f"{resolved_output_path}.part"

        hasher = hashlib.sha256() if verify_integrity else None
        fh = None
        bytes_written = 0
        content_disposition = ""
        etag = ""
        metadata: _fs_model.DownloadFileHttpMetadata | None = None
        start_offset = 0

        try:
            if resume and os.path.exists(tmp_path):
                existing_size = os.path.getsize(tmp_path)
                if resolved_file_size > 0 and existing_size > resolved_file_size:
                    os.remove(tmp_path)
                    existing_size = 0
                if existing_size > 0:
                    start_offset = existing_size
                    bytes_written = existing_size
                    if hasher is not None:
                        _update_hasher_from_file(hasher, tmp_path)
                    await _maybe_call_progress(
                        on_progress,
                        DownloadProgress(
                            downloaded_bytes=bytes_written,
                            total_bytes=resolved_file_size,
                            chunk_index=min(
                                _chunk_number_for_offset(max(existing_size - 1, 0), chunk_size),
                                max((resolved_file_size + chunk_size - 1) // chunk_size, 1),
                            ),
                            total_chunks=max((resolved_file_size + chunk_size - 1) // chunk_size, 1),
                        ),
                    )

                if resolved_file_size > 0 and existing_size == resolved_file_size:
                    if hasher is not None:
                        await self._verify_integrity_or_raise(
                            file_id=file_id,
                            checksum=hasher.hexdigest(),
                            business_id=business_id,
                            extra_metadata=extra_metadata,
                        )
                    os.replace(tmp_path, resolved_output_path)
                    return SavedDownloadedFile(
                        path=resolved_output_path,
                        bytes_written=existing_size,
                        content_type=resolved_content_type,
                        filename=filename,
                        content_disposition=content_disposition,
                        etag=etag,
                        metadata=metadata,
                    )

            async for chunk in self.iter_download_file_chunks(
                file_id=file_id,
                chunk_size=chunk_size,
                file_size=resolved_file_size,
                content_type=resolved_content_type,
                start_offset=start_offset,
                business_id=business_id,
                extra_metadata=extra_metadata,
            ):
                if fh is None:
                    mode = "ab" if start_offset > 0 and os.path.exists(tmp_path) else "wb"
                    fh = open(tmp_path, mode)

                fh.write(chunk.data)
                bytes_written += len(chunk.data)
                if hasher is not None:
                    hasher.update(chunk.data)
                if chunk.filename:
                    filename = chunk.filename
                if chunk.content_disposition:
                    content_disposition = chunk.content_disposition
                if chunk.etag:
                    etag = chunk.etag
                if chunk.metadata is not None:
                    metadata = chunk.metadata
                await _maybe_call_progress(
                    on_progress,
                    DownloadProgress(
                        downloaded_bytes=bytes_written,
                        total_bytes=chunk.total_size,
                        chunk_index=chunk.chunk_index,
                        total_chunks=chunk.total_chunks,
                    ),
                )

            if fh is None:
                raise FileStorageError(
                    "Chunk download produced no data",
                    code=grpc.StatusCode.UNKNOWN,
                )

            fh.close()
            fh = None

            if hasher is not None:
                await self._verify_integrity_or_raise(
                    file_id=file_id,
                    checksum=hasher.hexdigest(),
                    business_id=business_id,
                    extra_metadata=extra_metadata,
                )

            os.replace(tmp_path, resolved_output_path)

            return SavedDownloadedFile(
                path=resolved_output_path,
                bytes_written=bytes_written,
                content_type=resolved_content_type,
                filename=filename,
                content_disposition=content_disposition,
                etag=etag,
                metadata=metadata,
            )
        except Exception:
            if fh is not None and not fh.closed:
                fh.close()
            raise

    async def delete_file(
        self,
        file_id: str = "",
        request: _fs_model.DeleteFileRequest | _fs_pb.DeleteFileRequest | None = None,
        *,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> None:
        message = (
            _coerce_protobuf_message(request, _fs_pb.DeleteFileRequest)
            if request is not None
            else _fs_pb.DeleteFileRequest(file_id=file_id)
        )
        await self._call(
            self._s.DeleteFile(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )

    async def list_files(
        self,
        request: _fs_model.ListFilesRequest | _fs_pb.ListFilesRequest | None = None,
        *,
        folder: str = "/",
        page_size: int = 100,
        page_token: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _fs_model.ListFilesResponse:
        message = (
            _coerce_protobuf_message(request, _fs_pb.ListFilesRequest)
            if request is not None
            else _fs_pb.ListFilesRequest(
                folder=folder,
                page_size=page_size,
                page_token=page_token,
            )
        )
        response: _fs_pb.ListFilesResponse = await self._call(
            self._s.ListFiles(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _fs_model.ListFilesResponse.from_protobuf(response)

    async def get_file_info(
        self,
        file_id: str = "",
        request: _fs_model.GetFileInfoRequest | _fs_pb.GetFileInfoRequest | None = None,
        *,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> _fs_model.FileInfo:
        message = (
            _coerce_protobuf_message(request, _fs_pb.GetFileInfoRequest)
            if request is not None
            else _fs_pb.GetFileInfoRequest(file_id=file_id)
        )
        response: _fs_pb.FileInfo = await self._call(
            self._s.GetFileInfo(
                message,
                metadata=self._meta(extra_metadata=extra_metadata, business_id=business_id),
                timeout=self._timeout,
            )
        )
        return _fs_model.FileInfo.from_protobuf(response)


class SyncFileStorageClient(SyncGatewayClientBase[FileStorageClient]):
    """Synchronous facade over :class:`FileStorageClient`."""

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        super().__init__(FileStorageClient, *args, **kwargs)

    def upload_file(self, **kwargs) -> _fs_model.UploadFileResponse:  # type: ignore[no-untyped-def]
        return self._run(self._client.upload_file(**kwargs))

    def init_resumable_upload(self, *args, **kwargs) -> _fs_model.InitResumableUploadResponse:  # type: ignore[no-untyped-def]
        return self._run(self._client.init_resumable_upload(*args, **kwargs))

    def upload_part(self, **kwargs) -> _fs_model.UploadPartResponse:  # type: ignore[no-untyped-def]
        return self._run(self._client.upload_part(**kwargs))

    def complete_resumable_upload(self, *args, **kwargs) -> _fs_model.UploadFileResponse:  # type: ignore[no-untyped-def]
        return self._run(self._client.complete_resumable_upload(*args, **kwargs))

    def abort_resumable_upload(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        self._run(self._client.abort_resumable_upload(*args, **kwargs))

    def get_upload_status(self, *args, **kwargs) -> _fs_model.GetUploadStatusResponse:  # type: ignore[no-untyped-def]
        return self._run(self._client.get_upload_status(*args, **kwargs))

    def download_file(self, **kwargs) -> DownloadedFile:  # type: ignore[no-untyped-def]
        return self._run(self._client.download_file(**kwargs))

    def download_file_to_path(self, **kwargs) -> SavedDownloadedFile:  # type: ignore[no-untyped-def]
        return self._run(self._client.download_file_to_path(**kwargs))

    def download_file_in_chunks(self, **kwargs) -> DownloadedFile:  # type: ignore[no-untyped-def]
        return self._run(self._client.download_file_in_chunks(**kwargs))

    def verify_download_checksum(self, **kwargs) -> bool:  # type: ignore[no-untyped-def]
        return self._run(self._client.verify_download_checksum(**kwargs))

    def iter_download_file_chunks(self, **kwargs) -> list[DownloadedFileChunk]:  # type: ignore[no-untyped-def]
        async def _collect() -> list[DownloadedFileChunk]:
            chunks: list[DownloadedFileChunk] = []
            async for chunk in self._client.iter_download_file_chunks(**kwargs):
                chunks.append(chunk)
            return chunks

        return self._run(_collect())

    def delete_file(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        self._run(self._client.delete_file(*args, **kwargs))

    def list_files(self, *args, **kwargs) -> _fs_model.ListFilesResponse:  # type: ignore[no-untyped-def]
        return self._run(self._client.list_files(*args, **kwargs))

    def get_file_info(self, *args, **kwargs) -> _fs_model.FileInfo:  # type: ignore[no-untyped-def]
        return self._run(self._client.get_file_info(*args, **kwargs))


__all__ = [
    "DEFAULT_CHUNK_SIZE",
    "DownloadedFile",
    "DownloadedFileChunk",
    "DownloadProgress",
    "FileStorageClient",
    "FileStorageError",
    "SavedDownloadedFile",
    "SyncFileStorageClient",
]
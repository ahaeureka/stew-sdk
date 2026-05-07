import asyncio
from pathlib import Path

from google.protobuf.any_pb2 import Any
import pytest

from stew import (
    DownloadProgress,
    DownloadedFile,
    DownloadedFileChunk,
    FileStorageClient,
    SavedDownloadedFile,
    SyncFileStorageClient,
    collect_grpc_context_metadata,
    grpc_context_passthrough,
)
from stew.api.v1 import file_storage_model as file_storage_model
from stew.api.v1 import file_storage_pb2 as file_storage_pb2


def test_file_storage_client_is_exported() -> None:
    assert FileStorageClient is not None
    assert SyncFileStorageClient is not None
    assert DownloadedFile is not None


def test_download_file_extracts_extension_metadata() -> None:
    metadata = file_storage_pb2.DownloadFileHttpMetadata(
        filename="report.pdf",
        content_disposition='attachment; filename="report.pdf"',
        etag='"etag-value"',
    )
    extension = Any()
    extension.Pack(metadata)
    response = type(
        "HttpBodyLike",
        (),
        {
            "data": b"payload",
            "content_type": "application/pdf",
            "extensions": [extension],
        },
    )()

    class Stub:
        async def DownloadFile(self, request, metadata, timeout):
            assert request.file_id == "file-1"
            assert metadata == [("x-api-key", "ak_xxx")]
            assert timeout == 30.0
            return response

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]

    downloaded = asyncio.run(client.download_file(file_id="file-1"))

    assert downloaded == DownloadedFile(
        data=b"payload",
        content_type="application/pdf",
        filename="report.pdf",
        content_disposition='attachment; filename="report.pdf"',
        etag='"etag-value"',
        metadata=file_storage_model.DownloadFileHttpMetadata(
            filename="report.pdf",
            content_disposition='attachment; filename="report.pdf"',
            etag='"etag-value"',
        ),
    )


def test_collect_grpc_context_metadata_filters_and_normalizes_headers() -> None:
    class FakeContext:
        def invocation_metadata(self):
            return [
                ("authorization", "Bearer token-123"),
                ("X-User-Id", "user-1"),
                ("x-request-id", "req-1"),
                ("x-api-key", "should-not-pass"),
                ("grpc-timeout", "1S"),
            ]

    metadata = collect_grpc_context_metadata(FakeContext())

    assert metadata == [
        ("authorization", "Bearer token-123"),
        ("x-user-id", "user-1"),
        ("x-request-id", "req-1"),
    ]


def test_file_storage_client_merges_grpc_context_passthrough_metadata() -> None:
    captured: dict[str, object] = {}

    class FakeContext:
        def invocation_metadata(self):
            return [
                ("authorization", "Bearer token-123"),
                ("x-user-id", "user-1"),
                ("x-request-id", "req-1"),
                ("x-api-key", "inbound-secret"),
            ]

    class Stub:
        async def GetFileInfo(self, request, metadata, timeout):
            captured["metadata"] = list(metadata)
            return file_storage_pb2.FileInfo(
                id="file-1",
                filename="archive.bin",
                content_type="application/octet-stream",
                file_size=10,
            )

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]

    with grpc_context_passthrough(FakeContext()):
        asyncio.run(client.get_file_info(file_id="file-1"))

    assert captured["metadata"] == [
        ("authorization", "Bearer token-123"),
        ("x-user-id", "user-1"),
        ("x-request-id", "req-1"),
        ("x-api-key", "ak_xxx"),
    ]


def test_get_file_info_accepts_business_id_and_extra_metadata() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def GetFileInfo(self, request, metadata, timeout):
            captured["metadata"] = list(metadata)
            return file_storage_pb2.FileInfo(
                id="file-1",
                filename="archive.bin",
                content_type="application/octet-stream",
                file_size=10,
            )

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]

    asyncio.run(
        client.get_file_info(
            file_id="file-1",
            business_id="skillforge",
            extra_metadata=[("x-request-id", "req-1")],
        )
    )

    assert captured["metadata"] == [
        ("x-api-key", "ak_xxx"),
        ("x-business-id", "skillforge"),
        ("x-request-id", "req-1"),
    ]


def test_download_file_reports_progress_and_verifies_integrity() -> None:
    metadata = file_storage_pb2.DownloadFileHttpMetadata(
        filename="report.pdf",
        content_disposition='attachment; filename="report.pdf"',
        etag='"etag-value"',
    )
    extension = Any()
    extension.Pack(metadata)
    progress_events: list[DownloadProgress] = []
    verification_checks: list[str] = []

    class FakeCall:
        def __init__(self, payload: bytes, response_headers: list[tuple[str, str]]) -> None:
            self._payload = payload
            self._response_headers = response_headers

        def __await__(self):
            async def _wait():
                return type(
                    "HttpBodyLike",
                    (),
                    {
                        "data": self._payload,
                        "content_type": "application/pdf",
                        "extensions": [extension],
                    },
                )()

            return _wait().__await__()

        async def initial_metadata(self):
            return self._response_headers

    class Stub:
        def DownloadFile(self, request, metadata, timeout):
            if request.verify_only:
                verification_checks.append(request.checksum)
                return FakeCall(b"", [("x-http-status", "204")])

            assert request.file_id == "file-1"
            return FakeCall(b"payload", [("content-length", "7")])

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]

    downloaded = asyncio.run(
        client.download_file(
            file_id="file-1",
            verify_integrity=True,
            on_progress=progress_events.append,
        )
    )

    assert downloaded.data == b"payload"
    assert progress_events == [
        DownloadProgress(downloaded_bytes=7, total_bytes=7, chunk_index=1, total_chunks=1)
    ]
    assert verification_checks == [
        "239f59ed55e737c77147cf55ad0c1b030b6d7ee748a7426952f9b852d5a935e5"
    ]


def test_complete_resumable_upload_accepts_tuple_parts() -> None:
    captured = {}

    class Stub:
        async def CompleteResumableUpload(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = metadata
            captured["timeout"] = timeout
            return file_storage_pb2.UploadFileResponse()

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.complete_resumable_upload(upload_id="upload-1", parts=[(1, "etag-1"), (2, "etag-2")])
    )

    assert result == file_storage_model.UploadFileResponse()
    assert captured["metadata"] == [("x-api-key", "ak_xxx")]
    assert captured["timeout"] == 30.0
    assert captured["request"].upload_id == "upload-1"
    assert [(part.part_number, part.etag) for part in captured["request"].parts] == [
        (1, "etag-1"),
        (2, "etag-2"),
    ]


def test_download_file_in_chunks_uses_grpc_range_metadata() -> None:
    metadata = file_storage_pb2.DownloadFileHttpMetadata(
        filename="archive.bin",
        content_disposition='attachment; filename="archive.bin"',
        etag='"checksum"',
    )
    extension = Any()
    extension.Pack(metadata)
    requests: list[list[tuple[str, str]]] = []

    class FakeCall:
        def __init__(self, payload: bytes, response_headers: list[tuple[str, str]]) -> None:
            self._payload = payload
            self._response_headers = response_headers

        def __await__(self):
            async def _wait():
                return type(
                    "HttpBodyLike",
                    (),
                    {
                        "data": self._payload,
                        "content_type": "application/octet-stream",
                        "extensions": [extension],
                    },
                )()

            return _wait().__await__()

        async def initial_metadata(self):
            return self._response_headers

    class Stub:
        async def GetFileInfo(self, request, metadata, timeout):
            assert request.file_id == "file-1"
            return file_storage_pb2.FileInfo(
                id="file-1",
                filename="archive.bin",
                content_type="application/octet-stream",
                file_size=10,
            )

        def DownloadFile(self, request, metadata, timeout):
            requests.append(list(metadata))
            range_header = dict(metadata).get("range", "")
            assert request.file_id == "file-1"
            assert timeout == 30.0
            payload_by_range = {
                "bytes=0-3": b"abcd",
                "bytes=4-7": b"efgh",
                "bytes=8-9": b"ij",
            }
            content_range = range_header.replace("=", " ", 1) + "/10"
            return FakeCall(
                payload_by_range[range_header],
                [("x-http-status", "206"), ("content-range", content_range)],
            )

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]

    downloaded = asyncio.run(client.download_file_in_chunks(file_id="file-1", chunk_size=4))

    assert downloaded == DownloadedFile(
        data=b"abcdefghij",
        content_type="application/octet-stream",
        filename="archive.bin",
        content_disposition='attachment; filename="archive.bin"',
        etag='"checksum"',
        metadata=file_storage_model.DownloadFileHttpMetadata(
            filename="archive.bin",
            content_disposition='attachment; filename="archive.bin"',
            etag='"checksum"',
        ),
    )
    assert requests == [
        [("x-api-key", "ak_xxx"), ("range", "bytes=0-3")],
        [("x-api-key", "ak_xxx"), ("range", "bytes=4-7")],
        [("x-api-key", "ak_xxx"), ("range", "bytes=8-9")],
    ]


def test_download_file_in_chunks_reports_progress_and_verifies_integrity() -> None:
    extension = Any()
    extension.Pack(
        file_storage_pb2.DownloadFileHttpMetadata(
            filename="archive.bin",
            content_disposition='attachment; filename="archive.bin"',
            etag='"checksum"',
        )
    )
    progress_events: list[DownloadProgress] = []
    verification_checks: list[str] = []

    class FakeCall:
        def __init__(self, payload: bytes, response_headers: list[tuple[str, str]]) -> None:
            self._payload = payload
            self._response_headers = response_headers

        def __await__(self):
            async def _wait():
                return type(
                    "HttpBodyLike",
                    (),
                    {
                        "data": self._payload,
                        "content_type": "application/octet-stream",
                        "extensions": [extension],
                    },
                )()

            return _wait().__await__()

        async def initial_metadata(self):
            return self._response_headers

    class Stub:
        async def GetFileInfo(self, request, metadata, timeout):
            return file_storage_pb2.FileInfo(
                id=request.file_id,
                filename="archive.bin",
                content_type="application/octet-stream",
                file_size=8,
            )

        def DownloadFile(self, request, metadata, timeout):
            if request.verify_only:
                verification_checks.append(request.checksum)
                return FakeCall(b"", [("x-http-status", "204")])

            payload_by_range = {
                "bytes=0-3": b"abcd",
                "bytes=4-7": b"efgh",
            }
            range_header = dict(metadata)["range"]
            return FakeCall(
                payload_by_range[range_header],
                [
                    ("x-http-status", "206"),
                    ("content-range", range_header.replace("=", " ", 1) + "/8"),
                ],
            )

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]

    downloaded = asyncio.run(
        client.download_file_in_chunks(
            file_id="file-1",
            chunk_size=4,
            verify_integrity=True,
            on_progress=progress_events.append,
        )
    )

    assert downloaded.data == b"abcdefgh"
    assert progress_events == [
        DownloadProgress(downloaded_bytes=4, total_bytes=8, chunk_index=1, total_chunks=2),
        DownloadProgress(downloaded_bytes=8, total_bytes=8, chunk_index=2, total_chunks=2),
    ]
    assert verification_checks == [
        "9c56cc51b374c3ba189210d5b6d4bf57790d351c96c47c02190ecf1e430635ab"
    ]


def test_verify_download_checksum_returns_false_on_mismatch() -> None:
    class FakeCall:
        def __await__(self):
            async def _wait():
                return type(
                    "HttpBodyLike",
                    (),
                    {
                        "data": b"",
                        "content_type": "application/octet-stream",
                        "extensions": [],
                    },
                )()

            return _wait().__await__()

        async def initial_metadata(self):
            return [("x-http-status", "412")]

    class Stub:
        def DownloadFile(self, request, metadata, timeout):
            assert request.verify_only is True
            assert request.checksum == "bad"
            return FakeCall()

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]

    verified = asyncio.run(client.verify_download_checksum(file_id="file-1", checksum="bad"))

    assert verified is False


def test_download_file_to_path_streams_without_buffering_all_data(tmp_path: Path) -> None:
    extension = Any()
    extension.Pack(
        file_storage_pb2.DownloadFileHttpMetadata(
            filename="video.bin",
            content_disposition='attachment; filename="video.bin"',
            etag='"etag-video"',
        )
    )
    progress_events: list[DownloadProgress] = []
    verification_checks: list[str] = []

    class FakeCall:
        def __init__(self, payload: bytes, response_headers: list[tuple[str, str]]) -> None:
            self._payload = payload
            self._response_headers = response_headers

        def __await__(self):
            async def _wait():
                return type(
                    "HttpBodyLike",
                    (),
                    {
                        "data": self._payload,
                        "content_type": "application/octet-stream",
                        "extensions": [extension],
                    },
                )()

            return _wait().__await__()

        async def initial_metadata(self):
            return self._response_headers

    class Stub:
        async def GetFileInfo(self, request, metadata, timeout):
            return file_storage_pb2.FileInfo(
                id=request.file_id,
                filename="video.bin",
                content_type="application/octet-stream",
                file_size=8,
            )

        def DownloadFile(self, request, metadata, timeout):
            if request.verify_only:
                verification_checks.append(request.checksum)
                return FakeCall(b"", [("x-http-status", "204")])

            payload_by_range = {
                "bytes=0-3": b"abcd",
                "bytes=4-7": b"efgh",
            }
            range_header = dict(metadata)["range"]
            return FakeCall(
                payload_by_range[range_header],
                [
                    ("x-http-status", "206"),
                    ("content-range", range_header.replace("=", " ", 1) + "/8"),
                ],
            )

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]
    output_path = tmp_path / "nested" / "video.bin"

    saved = asyncio.run(
        client.download_file_to_path(
            file_id="file-1",
            output_path=str(output_path),
            chunk_size=4,
            verify_integrity=True,
            on_progress=progress_events.append,
        )
    )

    assert saved == SavedDownloadedFile(
        path=str(output_path),
        bytes_written=8,
        content_type="application/octet-stream",
        filename="video.bin",
        content_disposition='attachment; filename="video.bin"',
        etag='"etag-video"',
        metadata=file_storage_model.DownloadFileHttpMetadata(
            filename="video.bin",
            content_disposition='attachment; filename="video.bin"',
            etag='"etag-video"',
        ),
    )
    assert output_path.read_bytes() == b"abcdefgh"
    assert not output_path.with_suffix(output_path.suffix + ".part").exists()
    assert progress_events == [
        DownloadProgress(downloaded_bytes=4, total_bytes=8, chunk_index=1, total_chunks=2),
        DownloadProgress(downloaded_bytes=8, total_bytes=8, chunk_index=2, total_chunks=2),
    ]
    assert verification_checks == [
        "9c56cc51b374c3ba189210d5b6d4bf57790d351c96c47c02190ecf1e430635ab"
    ]


def test_download_file_to_path_rejects_existing_target_by_default(tmp_path: Path) -> None:
    output_path = tmp_path / "video.bin"
    output_path.write_bytes(b"existing")

    class Stub:
        def DownloadFile(self, request, metadata, timeout):
            raise AssertionError("download should not start when target already exists")

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]

    with pytest.raises(FileExistsError, match="replace_existing=True"):
        asyncio.run(
            client.download_file_to_path(
                file_id="file-1",
                output_path=str(output_path),
                file_size=8,
                content_type="application/octet-stream",
            )
        )

    assert output_path.read_bytes() == b"existing"


def test_download_file_to_path_overwrites_existing_target_when_enabled(tmp_path: Path) -> None:
    extension = Any()
    extension.Pack(
        file_storage_pb2.DownloadFileHttpMetadata(
            filename="video.bin",
            content_disposition='attachment; filename="video.bin"',
            etag='"etag-video"',
        )
    )

    class FakeCall:
        def __init__(self, payload: bytes, response_headers: list[tuple[str, str]]) -> None:
            self._payload = payload
            self._response_headers = response_headers

        def __await__(self):
            async def _wait():
                return type(
                    "HttpBodyLike",
                    (),
                    {
                        "data": self._payload,
                        "content_type": "application/octet-stream",
                        "extensions": [extension],
                    },
                )()

            return _wait().__await__()

        async def initial_metadata(self):
            return self._response_headers

    class Stub:
        def DownloadFile(self, request, metadata, timeout):
            range_header = dict(metadata)["range"]
            payload_by_range = {
                "bytes=0-3": b"abcd",
                "bytes=4-7": b"efgh",
            }
            return FakeCall(
                payload_by_range[range_header],
                [
                    ("x-http-status", "206"),
                    ("content-range", range_header.replace("=", " ", 1) + "/8"),
                ],
            )

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]
    output_path = tmp_path / "video.bin"
    output_path.write_bytes(b"old-data")

    saved = asyncio.run(
        client.download_file_to_path(
            file_id="file-1",
            output_path=str(output_path),
            file_size=8,
            content_type="application/octet-stream",
            chunk_size=4,
            replace_existing=True,
        )
    )

    assert saved.path == str(output_path)
    assert output_path.read_bytes() == b"abcdefgh"


def test_download_file_to_path_resumes_existing_part_file(tmp_path: Path) -> None:
    extension = Any()
    extension.Pack(
        file_storage_pb2.DownloadFileHttpMetadata(
            filename="video.bin",
            content_disposition='attachment; filename="video.bin"',
            etag='"etag-video"',
        )
    )
    progress_events: list[DownloadProgress] = []
    requests: list[str] = []
    verification_checks: list[str] = []

    class FakeCall:
        def __init__(self, payload: bytes, response_headers: list[tuple[str, str]]) -> None:
            self._payload = payload
            self._response_headers = response_headers

        def __await__(self):
            async def _wait():
                return type(
                    "HttpBodyLike",
                    (),
                    {
                        "data": self._payload,
                        "content_type": "application/octet-stream",
                        "extensions": [extension],
                    },
                )()

            return _wait().__await__()

        async def initial_metadata(self):
            return self._response_headers

    class Stub:
        async def GetFileInfo(self, request, metadata, timeout):
            return file_storage_pb2.FileInfo(
                id=request.file_id,
                filename="video.bin",
                content_type="application/octet-stream",
                file_size=8,
            )

        def DownloadFile(self, request, metadata, timeout):
            if request.verify_only:
                verification_checks.append(request.checksum)
                return FakeCall(b"", [("x-http-status", "204")])

            range_header = dict(metadata)["range"]
            requests.append(range_header)
            assert range_header == "bytes=4-7"
            return FakeCall(
                b"efgh",
                [
                    ("x-http-status", "206"),
                    ("content-range", "bytes 4-7/8"),
                ],
            )

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]
    output_path = tmp_path / "downloads" / "video.bin"
    part_path = Path(f"{output_path}.part")
    part_path.parent.mkdir(parents=True, exist_ok=True)
    part_path.write_bytes(b"abcd")

    saved = asyncio.run(
        client.download_file_to_path(
            file_id="file-1",
            output_path=str(output_path),
            chunk_size=4,
            verify_integrity=True,
            on_progress=progress_events.append,
            resume=True,
        )
    )

    assert saved.path == str(output_path)
    assert saved.bytes_written == 8
    assert output_path.read_bytes() == b"abcdefgh"
    assert not part_path.exists()
    assert requests == ["bytes=4-7"]
    assert progress_events == [
        DownloadProgress(downloaded_bytes=4, total_bytes=8, chunk_index=1, total_chunks=2),
        DownloadProgress(downloaded_bytes=8, total_bytes=8, chunk_index=2, total_chunks=2),
    ]
    assert verification_checks == [
        "9c56cc51b374c3ba189210d5b6d4bf57790d351c96c47c02190ecf1e430635ab"
    ]


def test_iter_download_file_chunks_yields_chunk_metadata() -> None:
    extension = Any()
    extension.Pack(
        file_storage_pb2.DownloadFileHttpMetadata(
            filename="report.csv",
            content_disposition='attachment; filename="report.csv"',
            etag='"etag-value"',
        )
    )

    class FakeCall:
        def __await__(self):
            async def _wait():
                return type(
                    "HttpBodyLike",
                    (),
                    {
                        "data": b"part",
                        "content_type": "text/csv",
                        "extensions": [extension],
                    },
                )()

            return _wait().__await__()

        async def initial_metadata(self):
            return [("x-http-status", "206"), ("content-range", "bytes 0-3/4")]

    class Stub:
        def DownloadFile(self, request, metadata, timeout):
            assert dict(metadata)["range"] == "bytes=0-3"
            return FakeCall()

    async def _collect(client: FileStorageClient) -> list[DownloadedFileChunk]:
        chunks: list[DownloadedFileChunk] = []
        async for chunk in client.iter_download_file_chunks(file_id="file-1", file_size=4, chunk_size=4):
            chunks.append(chunk)
        return chunks

    client = FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]

    chunks = asyncio.run(_collect(client))

    assert chunks == [
        DownloadedFileChunk(
            data=b"part",
            chunk_index=1,
            total_chunks=1,
            start=0,
            end=3,
            total_size=4,
            content_type="text/csv",
            filename="report.csv",
            content_disposition='attachment; filename="report.csv"',
            etag='"etag-value"',
            content_range="bytes 0-3/4",
            metadata=file_storage_model.DownloadFileHttpMetadata(
                filename="report.csv",
                content_disposition='attachment; filename="report.csv"',
                etag='"etag-value"',
            ),
        )
    ]
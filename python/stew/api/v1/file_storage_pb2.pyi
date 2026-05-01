import datetime

from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.api import httpbody_pb2 as _httpbody_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UploadSessionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UPLOAD_SESSION_STATUS_UNSPECIFIED: _ClassVar[UploadSessionStatus]
    UPLOAD_SESSION_STATUS_ACTIVE: _ClassVar[UploadSessionStatus]
    UPLOAD_SESSION_STATUS_COMPLETED: _ClassVar[UploadSessionStatus]
    UPLOAD_SESSION_STATUS_ABORTED: _ClassVar[UploadSessionStatus]

class PathEntryKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PATH_ENTRY_KIND_UNSPECIFIED: _ClassVar[PathEntryKind]
    PATH_ENTRY_KIND_FILE: _ClassVar[PathEntryKind]
    PATH_ENTRY_KIND_DIRECTORY: _ClassVar[PathEntryKind]
UPLOAD_SESSION_STATUS_UNSPECIFIED: UploadSessionStatus
UPLOAD_SESSION_STATUS_ACTIVE: UploadSessionStatus
UPLOAD_SESSION_STATUS_COMPLETED: UploadSessionStatus
UPLOAD_SESSION_STATUS_ABORTED: UploadSessionStatus
PATH_ENTRY_KIND_UNSPECIFIED: PathEntryKind
PATH_ENTRY_KIND_FILE: PathEntryKind
PATH_ENTRY_KIND_DIRECTORY: PathEntryKind

class UploadFileRequest(_message.Message):
    __slots__ = ("metadata", "chunk_data")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    metadata: UploadFileMetadata
    chunk_data: bytes
    def __init__(self, metadata: _Optional[_Union[UploadFileMetadata, _Mapping]] = ..., chunk_data: _Optional[bytes] = ...) -> None: ...

class UploadFileMetadata(_message.Message):
    __slots__ = ("filename", "content_type", "folder", "business_context")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    filename: str
    content_type: str
    folder: str
    business_context: str
    def __init__(self, filename: _Optional[str] = ..., content_type: _Optional[str] = ..., folder: _Optional[str] = ..., business_context: _Optional[str] = ...) -> None: ...

class UploadFileResponse(_message.Message):
    __slots__ = ("file_info", "callback_result")
    FILE_INFO_FIELD_NUMBER: _ClassVar[int]
    CALLBACK_RESULT_FIELD_NUMBER: _ClassVar[int]
    file_info: FileInfo
    callback_result: CallbackResult
    def __init__(self, file_info: _Optional[_Union[FileInfo, _Mapping]] = ..., callback_result: _Optional[_Union[CallbackResult, _Mapping]] = ...) -> None: ...

class InitResumableUploadRequest(_message.Message):
    __slots__ = ("filename", "content_type", "folder", "total_size", "part_size", "business_context", "checksum")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    PART_SIZE_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    filename: str
    content_type: str
    folder: str
    total_size: int
    part_size: int
    business_context: str
    checksum: str
    def __init__(self, filename: _Optional[str] = ..., content_type: _Optional[str] = ..., folder: _Optional[str] = ..., total_size: _Optional[int] = ..., part_size: _Optional[int] = ..., business_context: _Optional[str] = ..., checksum: _Optional[str] = ...) -> None: ...

class InitResumableUploadResponse(_message.Message):
    __slots__ = ("upload_id", "part_size", "total_parts", "expires_at")
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    PART_SIZE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PARTS_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    upload_id: str
    part_size: int
    total_parts: int
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, upload_id: _Optional[str] = ..., part_size: _Optional[int] = ..., total_parts: _Optional[int] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UploadPartRequest(_message.Message):
    __slots__ = ("header", "chunk_data")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    header: UploadPartHeader
    chunk_data: bytes
    def __init__(self, header: _Optional[_Union[UploadPartHeader, _Mapping]] = ..., chunk_data: _Optional[bytes] = ...) -> None: ...

class UploadPartHeader(_message.Message):
    __slots__ = ("upload_id", "part_number")
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    upload_id: str
    part_number: int
    def __init__(self, upload_id: _Optional[str] = ..., part_number: _Optional[int] = ...) -> None: ...

class UploadPartResponse(_message.Message):
    __slots__ = ("part_number", "etag", "bytes_written")
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    BYTES_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    part_number: int
    etag: str
    bytes_written: int
    def __init__(self, part_number: _Optional[int] = ..., etag: _Optional[str] = ..., bytes_written: _Optional[int] = ...) -> None: ...

class CompleteResumableUploadRequest(_message.Message):
    __slots__ = ("upload_id", "parts")
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    upload_id: str
    parts: _containers.RepeatedCompositeFieldContainer[PartEtag]
    def __init__(self, upload_id: _Optional[str] = ..., parts: _Optional[_Iterable[_Union[PartEtag, _Mapping]]] = ...) -> None: ...

class PartEtag(_message.Message):
    __slots__ = ("part_number", "etag")
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    part_number: int
    etag: str
    def __init__(self, part_number: _Optional[int] = ..., etag: _Optional[str] = ...) -> None: ...

class AbortResumableUploadRequest(_message.Message):
    __slots__ = ("upload_id",)
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    upload_id: str
    def __init__(self, upload_id: _Optional[str] = ...) -> None: ...

class GetUploadStatusRequest(_message.Message):
    __slots__ = ("upload_id",)
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    upload_id: str
    def __init__(self, upload_id: _Optional[str] = ...) -> None: ...

class GetUploadStatusResponse(_message.Message):
    __slots__ = ("upload_id", "status", "completed_parts", "total_parts", "expires_at", "filename", "total_size")
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_PARTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PARTS_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    upload_id: str
    status: UploadSessionStatus
    completed_parts: _containers.RepeatedCompositeFieldContainer[UploadedPartInfo]
    total_parts: int
    expires_at: _timestamp_pb2.Timestamp
    filename: str
    total_size: int
    def __init__(self, upload_id: _Optional[str] = ..., status: _Optional[_Union[UploadSessionStatus, str]] = ..., completed_parts: _Optional[_Iterable[_Union[UploadedPartInfo, _Mapping]]] = ..., total_parts: _Optional[int] = ..., expires_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., filename: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class UploadedPartInfo(_message.Message):
    __slots__ = ("part_number", "etag", "size", "completed_at")
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    part_number: int
    etag: str
    size: int
    completed_at: _timestamp_pb2.Timestamp
    def __init__(self, part_number: _Optional[int] = ..., etag: _Optional[str] = ..., size: _Optional[int] = ..., completed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DownloadFileRequest(_message.Message):
    __slots__ = ("file_id", "checksum", "verify_only")
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    VERIFY_ONLY_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    checksum: str
    verify_only: bool
    def __init__(self, file_id: _Optional[str] = ..., checksum: _Optional[str] = ..., verify_only: bool = ...) -> None: ...

class DownloadFileHttpMetadata(_message.Message):
    __slots__ = ("filename", "content_disposition", "etag")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_DISPOSITION_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    filename: str
    content_disposition: str
    etag: str
    def __init__(self, filename: _Optional[str] = ..., content_disposition: _Optional[str] = ..., etag: _Optional[str] = ...) -> None: ...

class DownloadFileChunk(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class DeleteFileRequest(_message.Message):
    __slots__ = ("file_id",)
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    def __init__(self, file_id: _Optional[str] = ...) -> None: ...

class ListFilesRequest(_message.Message):
    __slots__ = ("folder", "page_size", "page_token")
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    folder: str
    page_size: int
    page_token: str
    def __init__(self, folder: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListFilesResponse(_message.Message):
    __slots__ = ("files", "next_page_token", "total_count")
    FILES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[FileInfo]
    next_page_token: str
    total_count: int
    def __init__(self, files: _Optional[_Iterable[_Union[FileInfo, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_count: _Optional[int] = ...) -> None: ...

class GetFileInfoRequest(_message.Message):
    __slots__ = ("file_id",)
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    def __init__(self, file_id: _Optional[str] = ...) -> None: ...

class CallbackResult(_message.Message):
    __slots__ = ("accepted", "reference_id", "message")
    ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    accepted: bool
    reference_id: str
    message: str
    def __init__(self, accepted: bool = ..., reference_id: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class FileInfo(_message.Message):
    __slots__ = ("id", "filename", "content_type", "file_size", "folder", "owner_id", "checksum", "storage_backend", "created_at", "updated_at", "local_path", "storage_key")
    ID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    STORAGE_BACKEND_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    LOCAL_PATH_FIELD_NUMBER: _ClassVar[int]
    STORAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    id: str
    filename: str
    content_type: str
    file_size: int
    folder: str
    owner_id: str
    checksum: str
    storage_backend: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    local_path: str
    storage_key: str
    def __init__(self, id: _Optional[str] = ..., filename: _Optional[str] = ..., content_type: _Optional[str] = ..., file_size: _Optional[int] = ..., folder: _Optional[str] = ..., owner_id: _Optional[str] = ..., checksum: _Optional[str] = ..., storage_backend: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., local_path: _Optional[str] = ..., storage_key: _Optional[str] = ...) -> None: ...

class VirtualPathRef(_message.Message):
    __slots__ = ("folder", "relative_path")
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_PATH_FIELD_NUMBER: _ClassVar[int]
    folder: str
    relative_path: str
    def __init__(self, folder: _Optional[str] = ..., relative_path: _Optional[str] = ...) -> None: ...

class PathSelector(_message.Message):
    __slots__ = ("file_id", "path")
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    path: VirtualPathRef
    def __init__(self, file_id: _Optional[str] = ..., path: _Optional[_Union[VirtualPathRef, _Mapping]] = ...) -> None: ...

class PathEntry(_message.Message):
    __slots__ = ("kind", "name", "path", "parent_folder", "file_id", "content_type", "size_bytes", "checksum", "created_at", "updated_at", "has_children")
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    PARENT_FOLDER_FIELD_NUMBER: _ClassVar[int]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    HAS_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    kind: PathEntryKind
    name: str
    path: str
    parent_folder: str
    file_id: str
    content_type: str
    size_bytes: int
    checksum: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    has_children: bool
    def __init__(self, kind: _Optional[_Union[PathEntryKind, str]] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., parent_folder: _Optional[str] = ..., file_id: _Optional[str] = ..., content_type: _Optional[str] = ..., size_bytes: _Optional[int] = ..., checksum: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., has_children: bool = ...) -> None: ...

class ListFolderRequest(_message.Message):
    __slots__ = ("folder", "page_size", "page_token", "include_files", "include_directories")
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_FILES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DIRECTORIES_FIELD_NUMBER: _ClassVar[int]
    folder: str
    page_size: int
    page_token: str
    include_files: bool
    include_directories: bool
    def __init__(self, folder: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., include_files: bool = ..., include_directories: bool = ...) -> None: ...

class ListFolderResponse(_message.Message):
    __slots__ = ("entries", "next_page_token", "total_count")
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[PathEntry]
    next_page_token: str
    total_count: int
    def __init__(self, entries: _Optional[_Iterable[_Union[PathEntry, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_count: _Optional[int] = ...) -> None: ...

class GetPathInfoRequest(_message.Message):
    __slots__ = ("selector",)
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    selector: PathSelector
    def __init__(self, selector: _Optional[_Union[PathSelector, _Mapping]] = ...) -> None: ...

class GetPathInfoResponse(_message.Message):
    __slots__ = ("entry",)
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    entry: PathEntry
    def __init__(self, entry: _Optional[_Union[PathEntry, _Mapping]] = ...) -> None: ...

class ReadTextFileRequest(_message.Message):
    __slots__ = ("selector", "max_bytes", "fail_if_binary")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    MAX_BYTES_FIELD_NUMBER: _ClassVar[int]
    FAIL_IF_BINARY_FIELD_NUMBER: _ClassVar[int]
    selector: PathSelector
    max_bytes: int
    fail_if_binary: bool
    def __init__(self, selector: _Optional[_Union[PathSelector, _Mapping]] = ..., max_bytes: _Optional[int] = ..., fail_if_binary: bool = ...) -> None: ...

class ReadTextFileResponse(_message.Message):
    __slots__ = ("entry", "text", "content_type", "size_bytes", "checksum", "updated_at", "truncated", "lossy")
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    LOSSY_FIELD_NUMBER: _ClassVar[int]
    entry: PathEntry
    text: str
    content_type: str
    size_bytes: int
    checksum: str
    updated_at: _timestamp_pb2.Timestamp
    truncated: bool
    lossy: bool
    def __init__(self, entry: _Optional[_Union[PathEntry, _Mapping]] = ..., text: _Optional[str] = ..., content_type: _Optional[str] = ..., size_bytes: _Optional[int] = ..., checksum: _Optional[str] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., truncated: bool = ..., lossy: bool = ...) -> None: ...

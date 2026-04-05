import datetime

from google.api import annotations_pb2 as _annotations_pb2
from google.api import httpbody_pb2 as _httpbody_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AssetScopeKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ASSET_SCOPE_KIND_UNSPECIFIED: _ClassVar[AssetScopeKind]
    ASSET_SCOPE_KIND_USER: _ClassVar[AssetScopeKind]
    ASSET_SCOPE_KIND_SERVICE: _ClassVar[AssetScopeKind]
    ASSET_SCOPE_KIND_TENANT: _ClassVar[AssetScopeKind]
    ASSET_SCOPE_KIND_GLOBAL: _ClassVar[AssetScopeKind]

class AssetVersionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ASSET_VERSION_STATUS_UNSPECIFIED: _ClassVar[AssetVersionStatus]
    ASSET_VERSION_STATUS_DRAFT: _ClassVar[AssetVersionStatus]
    ASSET_VERSION_STATUS_READY: _ClassVar[AssetVersionStatus]
    ASSET_VERSION_STATUS_ARCHIVED: _ClassVar[AssetVersionStatus]
    ASSET_VERSION_STATUS_FAILED: _ClassVar[AssetVersionStatus]

class AssetEntryKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ASSET_ENTRY_KIND_UNSPECIFIED: _ClassVar[AssetEntryKind]
    ASSET_ENTRY_KIND_FILE: _ClassVar[AssetEntryKind]
    ASSET_ENTRY_KIND_DIRECTORY: _ClassVar[AssetEntryKind]

class AssetDiffMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ASSET_DIFF_MODE_UNSPECIFIED: _ClassVar[AssetDiffMode]
    ASSET_DIFF_MODE_STRUCTURE_ONLY: _ClassVar[AssetDiffMode]
    ASSET_DIFF_MODE_WITH_TEXT: _ClassVar[AssetDiffMode]

class AssetChangeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ASSET_CHANGE_TYPE_UNSPECIFIED: _ClassVar[AssetChangeType]
    ASSET_CHANGE_TYPE_ADDED: _ClassVar[AssetChangeType]
    ASSET_CHANGE_TYPE_REMOVED: _ClassVar[AssetChangeType]
    ASSET_CHANGE_TYPE_MODIFIED: _ClassVar[AssetChangeType]
    ASSET_CHANGE_TYPE_RENAMED: _ClassVar[AssetChangeType]
    ASSET_CHANGE_TYPE_TYPE_CHANGED: _ClassVar[AssetChangeType]

class AssetTextDiffStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ASSET_TEXT_DIFF_STATUS_UNSPECIFIED: _ClassVar[AssetTextDiffStatus]
    ASSET_TEXT_DIFF_STATUS_NOT_REQUESTED: _ClassVar[AssetTextDiffStatus]
    ASSET_TEXT_DIFF_STATUS_READY: _ClassVar[AssetTextDiffStatus]
    ASSET_TEXT_DIFF_STATUS_BINARY: _ClassVar[AssetTextDiffStatus]
    ASSET_TEXT_DIFF_STATUS_TOO_LARGE: _ClassVar[AssetTextDiffStatus]
    ASSET_TEXT_DIFF_STATUS_LOSSY: _ClassVar[AssetTextDiffStatus]
    ASSET_TEXT_DIFF_STATUS_ERROR: _ClassVar[AssetTextDiffStatus]
ASSET_SCOPE_KIND_UNSPECIFIED: AssetScopeKind
ASSET_SCOPE_KIND_USER: AssetScopeKind
ASSET_SCOPE_KIND_SERVICE: AssetScopeKind
ASSET_SCOPE_KIND_TENANT: AssetScopeKind
ASSET_SCOPE_KIND_GLOBAL: AssetScopeKind
ASSET_VERSION_STATUS_UNSPECIFIED: AssetVersionStatus
ASSET_VERSION_STATUS_DRAFT: AssetVersionStatus
ASSET_VERSION_STATUS_READY: AssetVersionStatus
ASSET_VERSION_STATUS_ARCHIVED: AssetVersionStatus
ASSET_VERSION_STATUS_FAILED: AssetVersionStatus
ASSET_ENTRY_KIND_UNSPECIFIED: AssetEntryKind
ASSET_ENTRY_KIND_FILE: AssetEntryKind
ASSET_ENTRY_KIND_DIRECTORY: AssetEntryKind
ASSET_DIFF_MODE_UNSPECIFIED: AssetDiffMode
ASSET_DIFF_MODE_STRUCTURE_ONLY: AssetDiffMode
ASSET_DIFF_MODE_WITH_TEXT: AssetDiffMode
ASSET_CHANGE_TYPE_UNSPECIFIED: AssetChangeType
ASSET_CHANGE_TYPE_ADDED: AssetChangeType
ASSET_CHANGE_TYPE_REMOVED: AssetChangeType
ASSET_CHANGE_TYPE_MODIFIED: AssetChangeType
ASSET_CHANGE_TYPE_RENAMED: AssetChangeType
ASSET_CHANGE_TYPE_TYPE_CHANGED: AssetChangeType
ASSET_TEXT_DIFF_STATUS_UNSPECIFIED: AssetTextDiffStatus
ASSET_TEXT_DIFF_STATUS_NOT_REQUESTED: AssetTextDiffStatus
ASSET_TEXT_DIFF_STATUS_READY: AssetTextDiffStatus
ASSET_TEXT_DIFF_STATUS_BINARY: AssetTextDiffStatus
ASSET_TEXT_DIFF_STATUS_TOO_LARGE: AssetTextDiffStatus
ASSET_TEXT_DIFF_STATUS_LOSSY: AssetTextDiffStatus
ASSET_TEXT_DIFF_STATUS_ERROR: AssetTextDiffStatus

class AssetCapabilities(_message.Message):
    __slots__ = ("can_edit", "can_rename", "can_delete", "can_create_draft", "can_publish", "can_activate")
    CAN_EDIT_FIELD_NUMBER: _ClassVar[int]
    CAN_RENAME_FIELD_NUMBER: _ClassVar[int]
    CAN_DELETE_FIELD_NUMBER: _ClassVar[int]
    CAN_CREATE_DRAFT_FIELD_NUMBER: _ClassVar[int]
    CAN_PUBLISH_FIELD_NUMBER: _ClassVar[int]
    CAN_ACTIVATE_FIELD_NUMBER: _ClassVar[int]
    can_edit: bool
    can_rename: bool
    can_delete: bool
    can_create_draft: bool
    can_publish: bool
    can_activate: bool
    def __init__(self, can_edit: bool = ..., can_rename: bool = ..., can_delete: bool = ..., can_create_draft: bool = ..., can_publish: bool = ..., can_activate: bool = ...) -> None: ...

class AssetCollection(_message.Message):
    __slots__ = ("asset_space", "asset_id", "display_name", "description", "scope_kind", "scope_value", "active_version_id", "draft_version_id", "has_draft", "total_versions", "created_at", "updated_at", "capabilities")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SCOPE_KIND_FIELD_NUMBER: _ClassVar[int]
    SCOPE_VALUE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    HAS_DRAFT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    display_name: str
    description: str
    scope_kind: AssetScopeKind
    scope_value: str
    active_version_id: str
    draft_version_id: str
    has_draft: bool
    total_versions: int
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    capabilities: AssetCapabilities
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., scope_kind: _Optional[_Union[AssetScopeKind, str]] = ..., scope_value: _Optional[str] = ..., active_version_id: _Optional[str] = ..., draft_version_id: _Optional[str] = ..., has_draft: bool = ..., total_versions: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., capabilities: _Optional[_Union[AssetCapabilities, _Mapping]] = ...) -> None: ...

class AssetVersionSummary(_message.Message):
    __slots__ = ("asset_space", "asset_id", "version_id", "status", "description", "created_by", "created_at", "is_active", "is_draft", "base_version_id", "version_hash", "entry_count", "total_bytes", "manifest_path", "has_unpublished_changes", "capabilities")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    IS_DRAFT_FIELD_NUMBER: _ClassVar[int]
    BASE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_HASH_FIELD_NUMBER: _ClassVar[int]
    ENTRY_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_BYTES_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_PATH_FIELD_NUMBER: _ClassVar[int]
    HAS_UNPUBLISHED_CHANGES_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    version_id: str
    status: AssetVersionStatus
    description: str
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    is_active: bool
    is_draft: bool
    base_version_id: str
    version_hash: str
    entry_count: int
    total_bytes: int
    manifest_path: str
    has_unpublished_changes: bool
    capabilities: AssetCapabilities
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., version_id: _Optional[str] = ..., status: _Optional[_Union[AssetVersionStatus, str]] = ..., description: _Optional[str] = ..., created_by: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., is_active: bool = ..., is_draft: bool = ..., base_version_id: _Optional[str] = ..., version_hash: _Optional[str] = ..., entry_count: _Optional[int] = ..., total_bytes: _Optional[int] = ..., manifest_path: _Optional[str] = ..., has_unpublished_changes: bool = ..., capabilities: _Optional[_Union[AssetCapabilities, _Mapping]] = ...) -> None: ...

class AssetTreeEntry(_message.Message):
    __slots__ = ("entry_kind", "path", "parent_path", "name", "file_id", "content_type", "size_bytes", "checksum", "has_children", "is_text_previewable", "language_hint", "entry_revision", "created_at", "updated_at", "capabilities")
    ENTRY_KIND_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    PARENT_PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    HAS_CHILDREN_FIELD_NUMBER: _ClassVar[int]
    IS_TEXT_PREVIEWABLE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_HINT_FIELD_NUMBER: _ClassVar[int]
    ENTRY_REVISION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    entry_kind: AssetEntryKind
    path: str
    parent_path: str
    name: str
    file_id: str
    content_type: str
    size_bytes: int
    checksum: str
    has_children: bool
    is_text_previewable: bool
    language_hint: str
    entry_revision: int
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    capabilities: AssetCapabilities
    def __init__(self, entry_kind: _Optional[_Union[AssetEntryKind, str]] = ..., path: _Optional[str] = ..., parent_path: _Optional[str] = ..., name: _Optional[str] = ..., file_id: _Optional[str] = ..., content_type: _Optional[str] = ..., size_bytes: _Optional[int] = ..., checksum: _Optional[str] = ..., has_children: bool = ..., is_text_previewable: bool = ..., language_hint: _Optional[str] = ..., entry_revision: _Optional[int] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., capabilities: _Optional[_Union[AssetCapabilities, _Mapping]] = ...) -> None: ...

class AssetDiffSummary(_message.Message):
    __slots__ = ("total_changes", "added_count", "removed_count", "modified_count", "renamed_count", "type_changed_count", "text_diff_count", "binary_change_count")
    TOTAL_CHANGES_FIELD_NUMBER: _ClassVar[int]
    ADDED_COUNT_FIELD_NUMBER: _ClassVar[int]
    REMOVED_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_COUNT_FIELD_NUMBER: _ClassVar[int]
    RENAMED_COUNT_FIELD_NUMBER: _ClassVar[int]
    TYPE_CHANGED_COUNT_FIELD_NUMBER: _ClassVar[int]
    TEXT_DIFF_COUNT_FIELD_NUMBER: _ClassVar[int]
    BINARY_CHANGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    total_changes: int
    added_count: int
    removed_count: int
    modified_count: int
    renamed_count: int
    type_changed_count: int
    text_diff_count: int
    binary_change_count: int
    def __init__(self, total_changes: _Optional[int] = ..., added_count: _Optional[int] = ..., removed_count: _Optional[int] = ..., modified_count: _Optional[int] = ..., renamed_count: _Optional[int] = ..., type_changed_count: _Optional[int] = ..., text_diff_count: _Optional[int] = ..., binary_change_count: _Optional[int] = ...) -> None: ...

class AssetDiffEntry(_message.Message):
    __slots__ = ("path", "old_path", "change_type", "old_entry_kind", "new_entry_kind", "old_file_id", "new_file_id", "old_checksum", "new_checksum", "old_size_bytes", "new_size_bytes", "is_text", "language_hint", "text_diff_status", "unified_diff", "diff_truncated", "old_preview", "new_preview", "diff_detail_available")
    PATH_FIELD_NUMBER: _ClassVar[int]
    OLD_PATH_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OLD_ENTRY_KIND_FIELD_NUMBER: _ClassVar[int]
    NEW_ENTRY_KIND_FIELD_NUMBER: _ClassVar[int]
    OLD_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    OLD_CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    NEW_CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    OLD_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    NEW_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    IS_TEXT_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_HINT_FIELD_NUMBER: _ClassVar[int]
    TEXT_DIFF_STATUS_FIELD_NUMBER: _ClassVar[int]
    UNIFIED_DIFF_FIELD_NUMBER: _ClassVar[int]
    DIFF_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    OLD_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    NEW_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    DIFF_DETAIL_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    path: str
    old_path: str
    change_type: AssetChangeType
    old_entry_kind: AssetEntryKind
    new_entry_kind: AssetEntryKind
    old_file_id: str
    new_file_id: str
    old_checksum: str
    new_checksum: str
    old_size_bytes: int
    new_size_bytes: int
    is_text: bool
    language_hint: str
    text_diff_status: AssetTextDiffStatus
    unified_diff: str
    diff_truncated: bool
    old_preview: str
    new_preview: str
    diff_detail_available: bool
    def __init__(self, path: _Optional[str] = ..., old_path: _Optional[str] = ..., change_type: _Optional[_Union[AssetChangeType, str]] = ..., old_entry_kind: _Optional[_Union[AssetEntryKind, str]] = ..., new_entry_kind: _Optional[_Union[AssetEntryKind, str]] = ..., old_file_id: _Optional[str] = ..., new_file_id: _Optional[str] = ..., old_checksum: _Optional[str] = ..., new_checksum: _Optional[str] = ..., old_size_bytes: _Optional[int] = ..., new_size_bytes: _Optional[int] = ..., is_text: bool = ..., language_hint: _Optional[str] = ..., text_diff_status: _Optional[_Union[AssetTextDiffStatus, str]] = ..., unified_diff: _Optional[str] = ..., diff_truncated: bool = ..., old_preview: _Optional[str] = ..., new_preview: _Optional[str] = ..., diff_detail_available: bool = ...) -> None: ...

class ListAssetCollectionsRequest(_message.Message):
    __slots__ = ("asset_space", "scope_kind", "scope_value", "page_size", "page_token")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    SCOPE_KIND_FIELD_NUMBER: _ClassVar[int]
    SCOPE_VALUE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    scope_kind: AssetScopeKind
    scope_value: str
    page_size: int
    page_token: str
    def __init__(self, asset_space: _Optional[str] = ..., scope_kind: _Optional[_Union[AssetScopeKind, str]] = ..., scope_value: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListAssetCollectionsResponse(_message.Message):
    __slots__ = ("collections", "next_page_token", "total_count")
    COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    collections: _containers.RepeatedCompositeFieldContainer[AssetCollection]
    next_page_token: str
    total_count: int
    def __init__(self, collections: _Optional[_Iterable[_Union[AssetCollection, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_count: _Optional[int] = ...) -> None: ...

class GetAssetCollectionRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ...) -> None: ...

class ListAssetTreeRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "version_id", "folder", "page_size", "page_token", "include_files", "include_directories")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_FILES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DIRECTORIES_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    version_id: str
    folder: str
    page_size: int
    page_token: str
    include_files: bool
    include_directories: bool
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., version_id: _Optional[str] = ..., folder: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., include_files: bool = ..., include_directories: bool = ...) -> None: ...

class ListAssetTreeResponse(_message.Message):
    __slots__ = ("collection", "version", "entries", "next_page_token", "total_count")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    collection: AssetCollection
    version: AssetVersionSummary
    entries: _containers.RepeatedCompositeFieldContainer[AssetTreeEntry]
    next_page_token: str
    total_count: int
    def __init__(self, collection: _Optional[_Union[AssetCollection, _Mapping]] = ..., version: _Optional[_Union[AssetVersionSummary, _Mapping]] = ..., entries: _Optional[_Iterable[_Union[AssetTreeEntry, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_count: _Optional[int] = ...) -> None: ...

class ListAssetVersionsRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "include_archived")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    include_archived: bool
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., include_archived: bool = ...) -> None: ...

class ListAssetVersionsResponse(_message.Message):
    __slots__ = ("collection", "versions", "active_version_id", "draft_version_id")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    collection: AssetCollection
    versions: _containers.RepeatedCompositeFieldContainer[AssetVersionSummary]
    active_version_id: str
    draft_version_id: str
    def __init__(self, collection: _Optional[_Union[AssetCollection, _Mapping]] = ..., versions: _Optional[_Iterable[_Union[AssetVersionSummary, _Mapping]]] = ..., active_version_id: _Optional[str] = ..., draft_version_id: _Optional[str] = ...) -> None: ...

class GetAssetVersionRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "version_id")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    version_id: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., version_id: _Optional[str] = ...) -> None: ...

class GetAssetVersionResponse(_message.Message):
    __slots__ = ("collection", "version", "base_version", "draft_diff_summary")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    BASE_VERSION_FIELD_NUMBER: _ClassVar[int]
    DRAFT_DIFF_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    collection: AssetCollection
    version: AssetVersionSummary
    base_version: AssetVersionSummary
    draft_diff_summary: AssetDiffSummary
    def __init__(self, collection: _Optional[_Union[AssetCollection, _Mapping]] = ..., version: _Optional[_Union[AssetVersionSummary, _Mapping]] = ..., base_version: _Optional[_Union[AssetVersionSummary, _Mapping]] = ..., draft_diff_summary: _Optional[_Union[AssetDiffSummary, _Mapping]] = ...) -> None: ...

class CreateDraftVersionRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "base_version_id", "draft_version_id", "description")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    base_version_id: str
    draft_version_id: str
    description: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., base_version_id: _Optional[str] = ..., draft_version_id: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateDraftVersionResponse(_message.Message):
    __slots__ = ("collection", "draft_version", "base_version")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_FIELD_NUMBER: _ClassVar[int]
    BASE_VERSION_FIELD_NUMBER: _ClassVar[int]
    collection: AssetCollection
    draft_version: AssetVersionSummary
    base_version: AssetVersionSummary
    def __init__(self, collection: _Optional[_Union[AssetCollection, _Mapping]] = ..., draft_version: _Optional[_Union[AssetVersionSummary, _Mapping]] = ..., base_version: _Optional[_Union[AssetVersionSummary, _Mapping]] = ...) -> None: ...

class DiscardDraftVersionRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "draft_version_id")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    draft_version_id: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., draft_version_id: _Optional[str] = ...) -> None: ...

class GetAssetEntryTextRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "version_id", "path")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    version_id: str
    path: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., version_id: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class GetAssetEntryTextResponse(_message.Message):
    __slots__ = ("entry", "version_id", "text", "content_type", "checksum", "size_bytes", "entry_revision", "truncated", "lossy", "language_hint")
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    ENTRY_REVISION_FIELD_NUMBER: _ClassVar[int]
    TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    LOSSY_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_HINT_FIELD_NUMBER: _ClassVar[int]
    entry: AssetTreeEntry
    version_id: str
    text: str
    content_type: str
    checksum: str
    size_bytes: int
    entry_revision: int
    truncated: bool
    lossy: bool
    language_hint: str
    def __init__(self, entry: _Optional[_Union[AssetTreeEntry, _Mapping]] = ..., version_id: _Optional[str] = ..., text: _Optional[str] = ..., content_type: _Optional[str] = ..., checksum: _Optional[str] = ..., size_bytes: _Optional[int] = ..., entry_revision: _Optional[int] = ..., truncated: bool = ..., lossy: bool = ..., language_hint: _Optional[str] = ...) -> None: ...

class UpdateDraftTextEntryRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "draft_version_id", "path", "text", "content_type", "expected_entry_revision", "commit_message")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_ENTRY_REVISION_FIELD_NUMBER: _ClassVar[int]
    COMMIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    draft_version_id: str
    path: str
    text: str
    content_type: str
    expected_entry_revision: int
    commit_message: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., draft_version_id: _Optional[str] = ..., path: _Optional[str] = ..., text: _Optional[str] = ..., content_type: _Optional[str] = ..., expected_entry_revision: _Optional[int] = ..., commit_message: _Optional[str] = ...) -> None: ...

class UpdateDraftTextEntryResponse(_message.Message):
    __slots__ = ("entry", "draft_version_id", "file_id", "checksum", "size_bytes", "entry_revision", "saved_at")
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    ENTRY_REVISION_FIELD_NUMBER: _ClassVar[int]
    SAVED_AT_FIELD_NUMBER: _ClassVar[int]
    entry: AssetTreeEntry
    draft_version_id: str
    file_id: str
    checksum: str
    size_bytes: int
    entry_revision: int
    saved_at: _timestamp_pb2.Timestamp
    def __init__(self, entry: _Optional[_Union[AssetTreeEntry, _Mapping]] = ..., draft_version_id: _Optional[str] = ..., file_id: _Optional[str] = ..., checksum: _Optional[str] = ..., size_bytes: _Optional[int] = ..., entry_revision: _Optional[int] = ..., saved_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RenameDraftEntryRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "draft_version_id", "path", "new_path")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    NEW_PATH_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    draft_version_id: str
    path: str
    new_path: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., draft_version_id: _Optional[str] = ..., path: _Optional[str] = ..., new_path: _Optional[str] = ...) -> None: ...

class RenameDraftEntryResponse(_message.Message):
    __slots__ = ("entry", "old_path")
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    OLD_PATH_FIELD_NUMBER: _ClassVar[int]
    entry: AssetTreeEntry
    old_path: str
    def __init__(self, entry: _Optional[_Union[AssetTreeEntry, _Mapping]] = ..., old_path: _Optional[str] = ...) -> None: ...

class DeleteDraftEntryRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "draft_version_id", "path")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    draft_version_id: str
    path: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., draft_version_id: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class DeleteDraftEntryResponse(_message.Message):
    __slots__ = ("draft_version_id", "deleted_path")
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DELETED_PATH_FIELD_NUMBER: _ClassVar[int]
    draft_version_id: str
    deleted_path: str
    def __init__(self, draft_version_id: _Optional[str] = ..., deleted_path: _Optional[str] = ...) -> None: ...

class DiffAssetVersionsRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "left_version_id", "right_version_id", "diff_mode", "path_prefix", "page_size", "page_token")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    LEFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    RIGHT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DIFF_MODE_FIELD_NUMBER: _ClassVar[int]
    PATH_PREFIX_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    left_version_id: str
    right_version_id: str
    diff_mode: AssetDiffMode
    path_prefix: str
    page_size: int
    page_token: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., left_version_id: _Optional[str] = ..., right_version_id: _Optional[str] = ..., diff_mode: _Optional[_Union[AssetDiffMode, str]] = ..., path_prefix: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class DiffAssetVersionsResponse(_message.Message):
    __slots__ = ("collection", "left_version", "right_version", "summary", "entries", "next_page_token", "total_count")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    LEFT_VERSION_FIELD_NUMBER: _ClassVar[int]
    RIGHT_VERSION_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    collection: AssetCollection
    left_version: AssetVersionSummary
    right_version: AssetVersionSummary
    summary: AssetDiffSummary
    entries: _containers.RepeatedCompositeFieldContainer[AssetDiffEntry]
    next_page_token: str
    total_count: int
    def __init__(self, collection: _Optional[_Union[AssetCollection, _Mapping]] = ..., left_version: _Optional[_Union[AssetVersionSummary, _Mapping]] = ..., right_version: _Optional[_Union[AssetVersionSummary, _Mapping]] = ..., summary: _Optional[_Union[AssetDiffSummary, _Mapping]] = ..., entries: _Optional[_Iterable[_Union[AssetDiffEntry, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_count: _Optional[int] = ...) -> None: ...

class DiffAssetDraftRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "draft_version_id", "base_version_id", "diff_mode", "path_prefix", "page_size", "page_token")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DIFF_MODE_FIELD_NUMBER: _ClassVar[int]
    PATH_PREFIX_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    draft_version_id: str
    base_version_id: str
    diff_mode: AssetDiffMode
    path_prefix: str
    page_size: int
    page_token: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., draft_version_id: _Optional[str] = ..., base_version_id: _Optional[str] = ..., diff_mode: _Optional[_Union[AssetDiffMode, str]] = ..., path_prefix: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class DiffAssetDraftResponse(_message.Message):
    __slots__ = ("collection", "draft_version", "base_version", "summary", "entries", "next_page_token", "total_count")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_FIELD_NUMBER: _ClassVar[int]
    BASE_VERSION_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    collection: AssetCollection
    draft_version: AssetVersionSummary
    base_version: AssetVersionSummary
    summary: AssetDiffSummary
    entries: _containers.RepeatedCompositeFieldContainer[AssetDiffEntry]
    next_page_token: str
    total_count: int
    def __init__(self, collection: _Optional[_Union[AssetCollection, _Mapping]] = ..., draft_version: _Optional[_Union[AssetVersionSummary, _Mapping]] = ..., base_version: _Optional[_Union[AssetVersionSummary, _Mapping]] = ..., summary: _Optional[_Union[AssetDiffSummary, _Mapping]] = ..., entries: _Optional[_Iterable[_Union[AssetDiffEntry, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_count: _Optional[int] = ...) -> None: ...

class GetAssetDiffEntryDetailRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "left_version_id", "right_version_id", "path", "diff_mode")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    LEFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    RIGHT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    DIFF_MODE_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    left_version_id: str
    right_version_id: str
    path: str
    diff_mode: AssetDiffMode
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., left_version_id: _Optional[str] = ..., right_version_id: _Optional[str] = ..., path: _Optional[str] = ..., diff_mode: _Optional[_Union[AssetDiffMode, str]] = ...) -> None: ...

class GetAssetDiffEntryDetailResponse(_message.Message):
    __slots__ = ("entry", "left_text", "right_text", "left_truncated", "right_truncated", "language_hint")
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    LEFT_TEXT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_TEXT_FIELD_NUMBER: _ClassVar[int]
    LEFT_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    RIGHT_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_HINT_FIELD_NUMBER: _ClassVar[int]
    entry: AssetDiffEntry
    left_text: str
    right_text: str
    left_truncated: bool
    right_truncated: bool
    language_hint: str
    def __init__(self, entry: _Optional[_Union[AssetDiffEntry, _Mapping]] = ..., left_text: _Optional[str] = ..., right_text: _Optional[str] = ..., left_truncated: bool = ..., right_truncated: bool = ..., language_hint: _Optional[str] = ...) -> None: ...

class PublishDraftVersionRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "draft_version_id", "version_id", "description", "previous_version_id")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    draft_version_id: str
    version_id: str
    description: str
    previous_version_id: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., draft_version_id: _Optional[str] = ..., version_id: _Optional[str] = ..., description: _Optional[str] = ..., previous_version_id: _Optional[str] = ...) -> None: ...

class PublishDraftVersionResponse(_message.Message):
    __slots__ = ("collection", "published_version", "active_version_id", "summary")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_VERSION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    collection: AssetCollection
    published_version: AssetVersionSummary
    active_version_id: str
    summary: AssetDiffSummary
    def __init__(self, collection: _Optional[_Union[AssetCollection, _Mapping]] = ..., published_version: _Optional[_Union[AssetVersionSummary, _Mapping]] = ..., active_version_id: _Optional[str] = ..., summary: _Optional[_Union[AssetDiffSummary, _Mapping]] = ...) -> None: ...

class ActivateAssetVersionRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "target_version_id", "previous_version_id")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    target_version_id: str
    previous_version_id: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., target_version_id: _Optional[str] = ..., previous_version_id: _Optional[str] = ...) -> None: ...

class ExportAssetEntryRequest(_message.Message):
    __slots__ = ("asset_space", "asset_id", "version_id", "path")
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    asset_space: str
    asset_id: str
    version_id: str
    path: str
    def __init__(self, asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., version_id: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class ActivateAssetVersionResponse(_message.Message):
    __slots__ = ("collection", "active_version_id", "active_version")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_VERSION_FIELD_NUMBER: _ClassVar[int]
    collection: AssetCollection
    active_version_id: str
    active_version: AssetVersionSummary
    def __init__(self, collection: _Optional[_Union[AssetCollection, _Mapping]] = ..., active_version_id: _Optional[str] = ..., active_version: _Optional[_Union[AssetVersionSummary, _Mapping]] = ...) -> None: ...

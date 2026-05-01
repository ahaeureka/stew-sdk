import business_asset_browser_pb2 as _business_asset_browser_pb2
from google.api import annotations_pb2 as _annotations_pb2
import pricing_pb2 as _pricing_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPricingPagePreviewRequest(_message.Message):
    __slots__ = ("business_id", "locale", "page_key", "draft_version_id", "billing_interval")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    PAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    BILLING_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    locale: str
    page_key: str
    draft_version_id: str
    billing_interval: str
    def __init__(self, business_id: _Optional[str] = ..., locale: _Optional[str] = ..., page_key: _Optional[str] = ..., draft_version_id: _Optional[str] = ..., billing_interval: _Optional[str] = ...) -> None: ...

class PricingPagePreviewResponse(_message.Message):
    __slots__ = ("page", "draft_version_id", "base_version_id", "has_unpublished_changes")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    HAS_UNPUBLISHED_CHANGES_FIELD_NUMBER: _ClassVar[int]
    page: _pricing_pb2.PricingPageResponse
    draft_version_id: str
    base_version_id: str
    has_unpublished_changes: bool
    def __init__(self, page: _Optional[_Union[_pricing_pb2.PricingPageResponse, _Mapping]] = ..., draft_version_id: _Optional[str] = ..., base_version_id: _Optional[str] = ..., has_unpublished_changes: bool = ...) -> None: ...

class EnsurePricingCollectionRequest(_message.Message):
    __slots__ = ("business_id", "asset_space", "asset_id", "scope_kind", "scope_value", "display_name", "description")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    SCOPE_KIND_FIELD_NUMBER: _ClassVar[int]
    SCOPE_VALUE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    asset_space: str
    asset_id: str
    scope_kind: _business_asset_browser_pb2.AssetScopeKind
    scope_value: str
    display_name: str
    description: str
    def __init__(self, business_id: _Optional[str] = ..., asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., scope_kind: _Optional[_Union[_business_asset_browser_pb2.AssetScopeKind, str]] = ..., scope_value: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class ListPricingVersionsRequest(_message.Message):
    __slots__ = ("business_id", "asset_space", "asset_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    asset_space: str
    asset_id: str
    def __init__(self, business_id: _Optional[str] = ..., asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ...) -> None: ...

class CreatePricingDraftRequest(_message.Message):
    __slots__ = ("business_id", "asset_space", "asset_id", "base_version_id", "draft_version_id", "description", "display_version")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_VERSION_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    asset_space: str
    asset_id: str
    base_version_id: str
    draft_version_id: str
    description: str
    display_version: str
    def __init__(self, business_id: _Optional[str] = ..., asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., base_version_id: _Optional[str] = ..., draft_version_id: _Optional[str] = ..., description: _Optional[str] = ..., display_version: _Optional[str] = ...) -> None: ...

class GetPricingDraftContentRequest(_message.Message):
    __slots__ = ("business_id", "asset_space", "asset_id", "version_id", "path")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    asset_space: str
    asset_id: str
    version_id: str
    path: str
    def __init__(self, business_id: _Optional[str] = ..., asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., version_id: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class SavePricingDraftRequest(_message.Message):
    __slots__ = ("business_id", "asset_space", "asset_id", "draft_version_id", "path", "text", "content_type", "expected_entry_revision", "commit_message")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_ENTRY_REVISION_FIELD_NUMBER: _ClassVar[int]
    COMMIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    asset_space: str
    asset_id: str
    draft_version_id: str
    path: str
    text: str
    content_type: str
    expected_entry_revision: int
    commit_message: str
    def __init__(self, business_id: _Optional[str] = ..., asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., draft_version_id: _Optional[str] = ..., path: _Optional[str] = ..., text: _Optional[str] = ..., content_type: _Optional[str] = ..., expected_entry_revision: _Optional[int] = ..., commit_message: _Optional[str] = ...) -> None: ...

class PublishPricingDraftRequest(_message.Message):
    __slots__ = ("business_id", "asset_space", "asset_id", "draft_version_id", "version_id", "description", "previous_version_id", "display_version")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_VERSION_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    asset_space: str
    asset_id: str
    draft_version_id: str
    version_id: str
    description: str
    previous_version_id: str
    display_version: str
    def __init__(self, business_id: _Optional[str] = ..., asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., draft_version_id: _Optional[str] = ..., version_id: _Optional[str] = ..., description: _Optional[str] = ..., previous_version_id: _Optional[str] = ..., display_version: _Optional[str] = ...) -> None: ...

class ActivatePricingVersionRequest(_message.Message):
    __slots__ = ("business_id", "asset_space", "asset_id", "target_version_id", "previous_version_id")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    asset_space: str
    asset_id: str
    target_version_id: str
    previous_version_id: str
    def __init__(self, business_id: _Optional[str] = ..., asset_space: _Optional[str] = ..., asset_id: _Optional[str] = ..., target_version_id: _Optional[str] = ..., previous_version_id: _Optional[str] = ...) -> None: ...

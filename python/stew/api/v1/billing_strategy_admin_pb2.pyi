import datetime

import billing_common_pb2 as _billing_common_pb2
import entitlement_pb2 as _entitlement_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protobuf_pydantic_gen import pydantic_pb2 as _pydantic_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StrategyPackageSection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STRATEGY_PACKAGE_SECTION_UNSPECIFIED: _ClassVar[StrategyPackageSection]
    STRATEGY_PACKAGE_SECTION_ENTITLEMENT_PLANS: _ClassVar[StrategyPackageSection]
    STRATEGY_PACKAGE_SECTION_BILLING_POLICIES: _ClassVar[StrategyPackageSection]
    STRATEGY_PACKAGE_SECTION_SERVICE_BINDINGS: _ClassVar[StrategyPackageSection]
    STRATEGY_PACKAGE_SECTION_PRICING_VIEWS: _ClassVar[StrategyPackageSection]

class StrategyImportMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STRATEGY_IMPORT_MODE_UNSPECIFIED: _ClassVar[StrategyImportMode]
    STRATEGY_IMPORT_MODE_CREATE_MISSING_ONLY: _ClassVar[StrategyImportMode]
    STRATEGY_IMPORT_MODE_UPSERT_MUTABLE_OBJECTS: _ClassVar[StrategyImportMode]
    STRATEGY_IMPORT_MODE_FAIL_IF_EXISTS: _ClassVar[StrategyImportMode]

class StrategyImportConflictPolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STRATEGY_IMPORT_CONFLICT_POLICY_UNSPECIFIED: _ClassVar[StrategyImportConflictPolicy]
    STRATEGY_IMPORT_CONFLICT_POLICY_FAIL: _ClassVar[StrategyImportConflictPolicy]
    STRATEGY_IMPORT_CONFLICT_POLICY_SKIP_REUSABLE: _ClassVar[StrategyImportConflictPolicy]
    STRATEGY_IMPORT_CONFLICT_POLICY_APPLY_MUTABLE_PATCH_ONLY: _ClassVar[StrategyImportConflictPolicy]

class StrategyPackageDiagnosticSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STRATEGY_PACKAGE_DIAGNOSTIC_SEVERITY_UNSPECIFIED: _ClassVar[StrategyPackageDiagnosticSeverity]
    STRATEGY_PACKAGE_DIAGNOSTIC_SEVERITY_INFO: _ClassVar[StrategyPackageDiagnosticSeverity]
    STRATEGY_PACKAGE_DIAGNOSTIC_SEVERITY_WARNING: _ClassVar[StrategyPackageDiagnosticSeverity]
    STRATEGY_PACKAGE_DIAGNOSTIC_SEVERITY_ERROR: _ClassVar[StrategyPackageDiagnosticSeverity]

class StrategyImportAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STRATEGY_IMPORT_ACTION_UNSPECIFIED: _ClassVar[StrategyImportAction]
    STRATEGY_IMPORT_ACTION_CREATE: _ClassVar[StrategyImportAction]
    STRATEGY_IMPORT_ACTION_UPDATE: _ClassVar[StrategyImportAction]
    STRATEGY_IMPORT_ACTION_REUSE: _ClassVar[StrategyImportAction]
    STRATEGY_IMPORT_ACTION_PUBLISH: _ClassVar[StrategyImportAction]
    STRATEGY_IMPORT_ACTION_SKIP: _ClassVar[StrategyImportAction]
    STRATEGY_IMPORT_ACTION_CONFLICT: _ClassVar[StrategyImportAction]
    STRATEGY_IMPORT_ACTION_NOOP: _ClassVar[StrategyImportAction]

class StrategyPackageObjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STRATEGY_PACKAGE_OBJECT_TYPE_UNSPECIFIED: _ClassVar[StrategyPackageObjectType]
    STRATEGY_PACKAGE_OBJECT_TYPE_PLAN: _ClassVar[StrategyPackageObjectType]
    STRATEGY_PACKAGE_OBJECT_TYPE_POLICY: _ClassVar[StrategyPackageObjectType]
    STRATEGY_PACKAGE_OBJECT_TYPE_ARTIFACT: _ClassVar[StrategyPackageObjectType]
    STRATEGY_PACKAGE_OBJECT_TYPE_BUNDLE: _ClassVar[StrategyPackageObjectType]
    STRATEGY_PACKAGE_OBJECT_TYPE_SERVICE_BINDING: _ClassVar[StrategyPackageObjectType]
    STRATEGY_PACKAGE_OBJECT_TYPE_PRICING_VIEW: _ClassVar[StrategyPackageObjectType]

class StrategyImportJobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STRATEGY_IMPORT_JOB_STATUS_UNSPECIFIED: _ClassVar[StrategyImportJobStatus]
    STRATEGY_IMPORT_JOB_STATUS_PENDING: _ClassVar[StrategyImportJobStatus]
    STRATEGY_IMPORT_JOB_STATUS_RUNNING: _ClassVar[StrategyImportJobStatus]
    STRATEGY_IMPORT_JOB_STATUS_SUCCEEDED: _ClassVar[StrategyImportJobStatus]
    STRATEGY_IMPORT_JOB_STATUS_FAILED: _ClassVar[StrategyImportJobStatus]
STRATEGY_PACKAGE_SECTION_UNSPECIFIED: StrategyPackageSection
STRATEGY_PACKAGE_SECTION_ENTITLEMENT_PLANS: StrategyPackageSection
STRATEGY_PACKAGE_SECTION_BILLING_POLICIES: StrategyPackageSection
STRATEGY_PACKAGE_SECTION_SERVICE_BINDINGS: StrategyPackageSection
STRATEGY_PACKAGE_SECTION_PRICING_VIEWS: StrategyPackageSection
STRATEGY_IMPORT_MODE_UNSPECIFIED: StrategyImportMode
STRATEGY_IMPORT_MODE_CREATE_MISSING_ONLY: StrategyImportMode
STRATEGY_IMPORT_MODE_UPSERT_MUTABLE_OBJECTS: StrategyImportMode
STRATEGY_IMPORT_MODE_FAIL_IF_EXISTS: StrategyImportMode
STRATEGY_IMPORT_CONFLICT_POLICY_UNSPECIFIED: StrategyImportConflictPolicy
STRATEGY_IMPORT_CONFLICT_POLICY_FAIL: StrategyImportConflictPolicy
STRATEGY_IMPORT_CONFLICT_POLICY_SKIP_REUSABLE: StrategyImportConflictPolicy
STRATEGY_IMPORT_CONFLICT_POLICY_APPLY_MUTABLE_PATCH_ONLY: StrategyImportConflictPolicy
STRATEGY_PACKAGE_DIAGNOSTIC_SEVERITY_UNSPECIFIED: StrategyPackageDiagnosticSeverity
STRATEGY_PACKAGE_DIAGNOSTIC_SEVERITY_INFO: StrategyPackageDiagnosticSeverity
STRATEGY_PACKAGE_DIAGNOSTIC_SEVERITY_WARNING: StrategyPackageDiagnosticSeverity
STRATEGY_PACKAGE_DIAGNOSTIC_SEVERITY_ERROR: StrategyPackageDiagnosticSeverity
STRATEGY_IMPORT_ACTION_UNSPECIFIED: StrategyImportAction
STRATEGY_IMPORT_ACTION_CREATE: StrategyImportAction
STRATEGY_IMPORT_ACTION_UPDATE: StrategyImportAction
STRATEGY_IMPORT_ACTION_REUSE: StrategyImportAction
STRATEGY_IMPORT_ACTION_PUBLISH: StrategyImportAction
STRATEGY_IMPORT_ACTION_SKIP: StrategyImportAction
STRATEGY_IMPORT_ACTION_CONFLICT: StrategyImportAction
STRATEGY_IMPORT_ACTION_NOOP: StrategyImportAction
STRATEGY_PACKAGE_OBJECT_TYPE_UNSPECIFIED: StrategyPackageObjectType
STRATEGY_PACKAGE_OBJECT_TYPE_PLAN: StrategyPackageObjectType
STRATEGY_PACKAGE_OBJECT_TYPE_POLICY: StrategyPackageObjectType
STRATEGY_PACKAGE_OBJECT_TYPE_ARTIFACT: StrategyPackageObjectType
STRATEGY_PACKAGE_OBJECT_TYPE_BUNDLE: StrategyPackageObjectType
STRATEGY_PACKAGE_OBJECT_TYPE_SERVICE_BINDING: StrategyPackageObjectType
STRATEGY_PACKAGE_OBJECT_TYPE_PRICING_VIEW: StrategyPackageObjectType
STRATEGY_IMPORT_JOB_STATUS_UNSPECIFIED: StrategyImportJobStatus
STRATEGY_IMPORT_JOB_STATUS_PENDING: StrategyImportJobStatus
STRATEGY_IMPORT_JOB_STATUS_RUNNING: StrategyImportJobStatus
STRATEGY_IMPORT_JOB_STATUS_SUCCEEDED: StrategyImportJobStatus
STRATEGY_IMPORT_JOB_STATUS_FAILED: StrategyImportJobStatus

class BillingStrategyPackage(_message.Message):
    __slots__ = ("document_type", "schema_version", "exported_at", "export_scope", "source", "id_policy", "entitlement_plans", "billing_policies", "service_bindings", "pricing_views", "integrity")
    DOCUMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    EXPORTED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPORT_SCOPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    ID_POLICY_FIELD_NUMBER: _ClassVar[int]
    ENTITLEMENT_PLANS_FIELD_NUMBER: _ClassVar[int]
    BILLING_POLICIES_FIELD_NUMBER: _ClassVar[int]
    SERVICE_BINDINGS_FIELD_NUMBER: _ClassVar[int]
    PRICING_VIEWS_FIELD_NUMBER: _ClassVar[int]
    INTEGRITY_FIELD_NUMBER: _ClassVar[int]
    document_type: str
    schema_version: str
    exported_at: _timestamp_pb2.Timestamp
    export_scope: StrategyPackageExportScope
    source: StrategyPackageSource
    id_policy: StrategyPackageIdPolicy
    entitlement_plans: _containers.RepeatedCompositeFieldContainer[StrategyPackagePlan]
    billing_policies: _containers.RepeatedCompositeFieldContainer[StrategyPackagePolicy]
    service_bindings: _containers.RepeatedCompositeFieldContainer[StrategyPackageServiceBinding]
    pricing_views: _containers.RepeatedCompositeFieldContainer[StrategyPackagePricingView]
    integrity: StrategyPackageIntegrity
    def __init__(self, document_type: _Optional[str] = ..., schema_version: _Optional[str] = ..., exported_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., export_scope: _Optional[_Union[StrategyPackageExportScope, _Mapping]] = ..., source: _Optional[_Union[StrategyPackageSource, _Mapping]] = ..., id_policy: _Optional[_Union[StrategyPackageIdPolicy, _Mapping]] = ..., entitlement_plans: _Optional[_Iterable[_Union[StrategyPackagePlan, _Mapping]]] = ..., billing_policies: _Optional[_Iterable[_Union[StrategyPackagePolicy, _Mapping]]] = ..., service_bindings: _Optional[_Iterable[_Union[StrategyPackageServiceBinding, _Mapping]]] = ..., pricing_views: _Optional[_Iterable[_Union[StrategyPackagePricingView, _Mapping]]] = ..., integrity: _Optional[_Union[StrategyPackageIntegrity, _Mapping]] = ...) -> None: ...

class StrategyPackageExportScope(_message.Message):
    __slots__ = ("business_id", "strategy_key", "sections", "include_archived", "include_inactive_bundles")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_KEY_FIELD_NUMBER: _ClassVar[int]
    SECTIONS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_INACTIVE_BUNDLES_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    strategy_key: str
    sections: _containers.RepeatedScalarFieldContainer[StrategyPackageSection]
    include_archived: bool
    include_inactive_bundles: bool
    def __init__(self, business_id: _Optional[str] = ..., strategy_key: _Optional[str] = ..., sections: _Optional[_Iterable[_Union[StrategyPackageSection, str]]] = ..., include_archived: bool = ..., include_inactive_bundles: bool = ...) -> None: ...

class StrategyPackageSource(_message.Message):
    __slots__ = ("exporter", "exporter_version", "workspace")
    EXPORTER_FIELD_NUMBER: _ClassVar[int]
    EXPORTER_VERSION_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    exporter: str
    exporter_version: str
    workspace: str
    def __init__(self, exporter: _Optional[str] = ..., exporter_version: _Optional[str] = ..., workspace: _Optional[str] = ...) -> None: ...

class StrategyPackageIdPolicy(_message.Message):
    __slots__ = ("plan_identity", "policy_identity", "artifact_identity", "bundle_identity", "binding_identity", "runtime_refs_are_authoritative")
    PLAN_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    POLICY_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    BINDING_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_REFS_ARE_AUTHORITATIVE_FIELD_NUMBER: _ClassVar[int]
    plan_identity: str
    policy_identity: str
    artifact_identity: str
    bundle_identity: str
    binding_identity: str
    runtime_refs_are_authoritative: bool
    def __init__(self, plan_identity: _Optional[str] = ..., policy_identity: _Optional[str] = ..., artifact_identity: _Optional[str] = ..., bundle_identity: _Optional[str] = ..., binding_identity: _Optional[str] = ..., runtime_refs_are_authoritative: bool = ...) -> None: ...

class StrategyPackagePlanRuntimeRefs(_message.Message):
    __slots__ = ("plan_id",)
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    plan_id: str
    def __init__(self, plan_id: _Optional[str] = ...) -> None: ...

class StrategyPackagePlan(_message.Message):
    __slots__ = ("plan_key", "plan_code", "runtime_refs", "create_plan_request", "metadata_contract")
    PLAN_KEY_FIELD_NUMBER: _ClassVar[int]
    PLAN_CODE_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_REFS_FIELD_NUMBER: _ClassVar[int]
    CREATE_PLAN_REQUEST_FIELD_NUMBER: _ClassVar[int]
    METADATA_CONTRACT_FIELD_NUMBER: _ClassVar[int]
    plan_key: str
    plan_code: str
    runtime_refs: StrategyPackagePlanRuntimeRefs
    create_plan_request: _entitlement_pb2.CreatePlanRequest
    metadata_contract: StrategyPackagePlanMetadataContract
    def __init__(self, plan_key: _Optional[str] = ..., plan_code: _Optional[str] = ..., runtime_refs: _Optional[_Union[StrategyPackagePlanRuntimeRefs, _Mapping]] = ..., create_plan_request: _Optional[_Union[_entitlement_pb2.CreatePlanRequest, _Mapping]] = ..., metadata_contract: _Optional[_Union[StrategyPackagePlanMetadataContract, _Mapping]] = ...) -> None: ...

class StrategyPackagePlanMetadataContract(_message.Message):
    __slots__ = ("billing_model", "price_keys")
    BILLING_MODEL_FIELD_NUMBER: _ClassVar[int]
    PRICE_KEYS_FIELD_NUMBER: _ClassVar[int]
    billing_model: str
    price_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, billing_model: _Optional[str] = ..., price_keys: _Optional[_Iterable[str]] = ...) -> None: ...

class StrategyPackagePolicyRuntimeRefs(_message.Message):
    __slots__ = ("policy_id",)
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    policy_id: str
    def __init__(self, policy_id: _Optional[str] = ...) -> None: ...

class StrategyPackagePolicyInfo(_message.Message):
    __slots__ = ("display_name", "description", "status")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    description: str
    status: str
    def __init__(self, display_name: _Optional[str] = ..., description: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class StrategyPackageArtifactRuntimeRefs(_message.Message):
    __slots__ = ("artifact_id",)
    ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    artifact_id: str
    def __init__(self, artifact_id: _Optional[str] = ...) -> None: ...

class StrategyPackageArtifact(_message.Message):
    __slots__ = ("artifact_key", "runtime_refs", "artifact_type", "artifact_version", "content_hash", "content")
    ARTIFACT_KEY_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_REFS_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_VERSION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_HASH_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    artifact_key: str
    runtime_refs: StrategyPackageArtifactRuntimeRefs
    artifact_type: _billing_common_pb2.BillingPolicyArtifactType
    artifact_version: str
    content_hash: str
    content: _struct_pb2.Struct
    def __init__(self, artifact_key: _Optional[str] = ..., runtime_refs: _Optional[_Union[StrategyPackageArtifactRuntimeRefs, _Mapping]] = ..., artifact_type: _Optional[_Union[_billing_common_pb2.BillingPolicyArtifactType, str]] = ..., artifact_version: _Optional[str] = ..., content_hash: _Optional[str] = ..., content: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class StrategyPackageBundleRuntimeRefs(_message.Message):
    __slots__ = ("published_bundle_version",)
    PUBLISHED_BUNDLE_VERSION_FIELD_NUMBER: _ClassVar[int]
    published_bundle_version: int
    def __init__(self, published_bundle_version: _Optional[int] = ...) -> None: ...

class StrategyPackageBundleArtifactRefs(_message.Message):
    __slots__ = ("provider_rate_card", "point_policy", "money_policy", "estimator")
    PROVIDER_RATE_CARD_FIELD_NUMBER: _ClassVar[int]
    POINT_POLICY_FIELD_NUMBER: _ClassVar[int]
    MONEY_POLICY_FIELD_NUMBER: _ClassVar[int]
    ESTIMATOR_FIELD_NUMBER: _ClassVar[int]
    provider_rate_card: str
    point_policy: str
    money_policy: str
    estimator: str
    def __init__(self, provider_rate_card: _Optional[str] = ..., point_policy: _Optional[str] = ..., money_policy: _Optional[str] = ..., estimator: _Optional[str] = ...) -> None: ...

class StrategyPackageBundle(_message.Message):
    __slots__ = ("bundle_key", "bundle_version", "status", "factor_schema_version", "artifact_refs", "runtime_refs")
    BUNDLE_KEY_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_VERSION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FACTOR_SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_REFS_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_REFS_FIELD_NUMBER: _ClassVar[int]
    bundle_key: str
    bundle_version: int
    status: str
    factor_schema_version: str
    artifact_refs: StrategyPackageBundleArtifactRefs
    runtime_refs: StrategyPackageBundleRuntimeRefs
    def __init__(self, bundle_key: _Optional[str] = ..., bundle_version: _Optional[int] = ..., status: _Optional[str] = ..., factor_schema_version: _Optional[str] = ..., artifact_refs: _Optional[_Union[StrategyPackageBundleArtifactRefs, _Mapping]] = ..., runtime_refs: _Optional[_Union[StrategyPackageBundleRuntimeRefs, _Mapping]] = ...) -> None: ...

class StrategyPackagePolicy(_message.Message):
    __slots__ = ("policy_key", "runtime_refs", "policy", "artifacts", "bundles")
    POLICY_KEY_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_REFS_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    ARTIFACTS_FIELD_NUMBER: _ClassVar[int]
    BUNDLES_FIELD_NUMBER: _ClassVar[int]
    policy_key: str
    runtime_refs: StrategyPackagePolicyRuntimeRefs
    policy: StrategyPackagePolicyInfo
    artifacts: _containers.RepeatedCompositeFieldContainer[StrategyPackageArtifact]
    bundles: _containers.RepeatedCompositeFieldContainer[StrategyPackageBundle]
    def __init__(self, policy_key: _Optional[str] = ..., runtime_refs: _Optional[_Union[StrategyPackagePolicyRuntimeRefs, _Mapping]] = ..., policy: _Optional[_Union[StrategyPackagePolicyInfo, _Mapping]] = ..., artifacts: _Optional[_Iterable[_Union[StrategyPackageArtifact, _Mapping]]] = ..., bundles: _Optional[_Iterable[_Union[StrategyPackageBundle, _Mapping]]] = ...) -> None: ...

class StrategyPackagePolicyRef(_message.Message):
    __slots__ = ("policy_key",)
    POLICY_KEY_FIELD_NUMBER: _ClassVar[int]
    policy_key: str
    def __init__(self, policy_key: _Optional[str] = ...) -> None: ...

class StrategyPackagePlanPolicyOverride(_message.Message):
    __slots__ = ("plan_key", "policy_ref")
    PLAN_KEY_FIELD_NUMBER: _ClassVar[int]
    POLICY_REF_FIELD_NUMBER: _ClassVar[int]
    plan_key: str
    policy_ref: StrategyPackagePolicyRef
    def __init__(self, plan_key: _Optional[str] = ..., policy_ref: _Optional[_Union[StrategyPackagePolicyRef, _Mapping]] = ...) -> None: ...

class StrategyPackageServiceBinding(_message.Message):
    __slots__ = ("binding_key", "service_name", "business_id", "default_policy_ref", "policy_overrides_by_plan", "service_billing_config_patch")
    BINDING_KEY_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_POLICY_REF_FIELD_NUMBER: _ClassVar[int]
    POLICY_OVERRIDES_BY_PLAN_FIELD_NUMBER: _ClassVar[int]
    SERVICE_BILLING_CONFIG_PATCH_FIELD_NUMBER: _ClassVar[int]
    binding_key: str
    service_name: str
    business_id: str
    default_policy_ref: StrategyPackagePolicyRef
    policy_overrides_by_plan: _containers.RepeatedCompositeFieldContainer[StrategyPackagePlanPolicyOverride]
    service_billing_config_patch: _billing_common_pb2.ServiceBillingConfig
    def __init__(self, binding_key: _Optional[str] = ..., service_name: _Optional[str] = ..., business_id: _Optional[str] = ..., default_policy_ref: _Optional[_Union[StrategyPackagePolicyRef, _Mapping]] = ..., policy_overrides_by_plan: _Optional[_Iterable[_Union[StrategyPackagePlanPolicyOverride, _Mapping]]] = ..., service_billing_config_patch: _Optional[_Union[_billing_common_pb2.ServiceBillingConfig, _Mapping]] = ...) -> None: ...

class StrategyPackagePricingView(_message.Message):
    __slots__ = ("pricing_view_key", "asset_space", "document_path", "content")
    PRICING_VIEW_KEY_FIELD_NUMBER: _ClassVar[int]
    ASSET_SPACE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_PATH_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    pricing_view_key: str
    asset_space: str
    document_path: str
    content: _struct_pb2.Struct
    def __init__(self, pricing_view_key: _Optional[str] = ..., asset_space: _Optional[str] = ..., document_path: _Optional[str] = ..., content: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class StrategyPackageIntegrity(_message.Message):
    __slots__ = ("hash_algorithm", "package_hash")
    HASH_ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_HASH_FIELD_NUMBER: _ClassVar[int]
    hash_algorithm: str
    package_hash: str
    def __init__(self, hash_algorithm: _Optional[str] = ..., package_hash: _Optional[str] = ...) -> None: ...

class ValidateStrategyPackageRequest(_message.Message):
    __slots__ = ("package", "allow_partial_sections", "allow_runtime_ref_mismatch", "conflict_policy")
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    ALLOW_PARTIAL_SECTIONS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_RUNTIME_REF_MISMATCH_FIELD_NUMBER: _ClassVar[int]
    CONFLICT_POLICY_FIELD_NUMBER: _ClassVar[int]
    package: BillingStrategyPackage
    allow_partial_sections: bool
    allow_runtime_ref_mismatch: bool
    conflict_policy: StrategyImportConflictPolicy
    def __init__(self, package: _Optional[_Union[BillingStrategyPackage, _Mapping]] = ..., allow_partial_sections: bool = ..., allow_runtime_ref_mismatch: bool = ..., conflict_policy: _Optional[_Union[StrategyImportConflictPolicy, str]] = ...) -> None: ...

class ValidateStrategyPackageResponse(_message.Message):
    __slots__ = ("success", "diagnostics", "plan", "summary")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    success: bool
    diagnostics: _containers.RepeatedCompositeFieldContainer[StrategyPackageDiagnostic]
    plan: StrategyImportPlan
    summary: StrategyImportCounts
    def __init__(self, success: bool = ..., diagnostics: _Optional[_Iterable[_Union[StrategyPackageDiagnostic, _Mapping]]] = ..., plan: _Optional[_Union[StrategyImportPlan, _Mapping]] = ..., summary: _Optional[_Union[StrategyImportCounts, _Mapping]] = ...) -> None: ...

class ValidateSkillforgeStrategyBundleRequest(_message.Message):
    __slots__ = ("source_bundle", "target_service_name", "allow_partial_sections", "allow_runtime_ref_mismatch", "conflict_policy")
    SOURCE_BUNDLE_FIELD_NUMBER: _ClassVar[int]
    TARGET_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ALLOW_PARTIAL_SECTIONS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_RUNTIME_REF_MISMATCH_FIELD_NUMBER: _ClassVar[int]
    CONFLICT_POLICY_FIELD_NUMBER: _ClassVar[int]
    source_bundle: _struct_pb2.Struct
    target_service_name: str
    allow_partial_sections: bool
    allow_runtime_ref_mismatch: bool
    conflict_policy: StrategyImportConflictPolicy
    def __init__(self, source_bundle: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., target_service_name: _Optional[str] = ..., allow_partial_sections: bool = ..., allow_runtime_ref_mismatch: bool = ..., conflict_policy: _Optional[_Union[StrategyImportConflictPolicy, str]] = ...) -> None: ...

class ValidateSkillforgeStrategyBundleResponse(_message.Message):
    __slots__ = ("success", "generated_package", "notices", "diagnostics", "plan", "summary")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    GENERATED_PACKAGE_FIELD_NUMBER: _ClassVar[int]
    NOTICES_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    success: bool
    generated_package: BillingStrategyPackage
    notices: _containers.RepeatedScalarFieldContainer[str]
    diagnostics: _containers.RepeatedCompositeFieldContainer[StrategyPackageDiagnostic]
    plan: StrategyImportPlan
    summary: StrategyImportCounts
    def __init__(self, success: bool = ..., generated_package: _Optional[_Union[BillingStrategyPackage, _Mapping]] = ..., notices: _Optional[_Iterable[str]] = ..., diagnostics: _Optional[_Iterable[_Union[StrategyPackageDiagnostic, _Mapping]]] = ..., plan: _Optional[_Union[StrategyImportPlan, _Mapping]] = ..., summary: _Optional[_Union[StrategyImportCounts, _Mapping]] = ...) -> None: ...

class ImportStrategyPackageRequest(_message.Message):
    __slots__ = ("package", "mode", "conflict_policy", "dry_run", "allow_partial_sections")
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    CONFLICT_POLICY_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    ALLOW_PARTIAL_SECTIONS_FIELD_NUMBER: _ClassVar[int]
    package: BillingStrategyPackage
    mode: StrategyImportMode
    conflict_policy: StrategyImportConflictPolicy
    dry_run: bool
    allow_partial_sections: bool
    def __init__(self, package: _Optional[_Union[BillingStrategyPackage, _Mapping]] = ..., mode: _Optional[_Union[StrategyImportMode, str]] = ..., conflict_policy: _Optional[_Union[StrategyImportConflictPolicy, str]] = ..., dry_run: bool = ..., allow_partial_sections: bool = ...) -> None: ...

class ImportStrategyPackageResponse(_message.Message):
    __slots__ = ("success", "import_job_id", "diagnostics", "plan", "result")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    IMPORT_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    import_job_id: str
    diagnostics: _containers.RepeatedCompositeFieldContainer[StrategyPackageDiagnostic]
    plan: StrategyImportPlan
    result: StrategyImportResult
    def __init__(self, success: bool = ..., import_job_id: _Optional[str] = ..., diagnostics: _Optional[_Iterable[_Union[StrategyPackageDiagnostic, _Mapping]]] = ..., plan: _Optional[_Union[StrategyImportPlan, _Mapping]] = ..., result: _Optional[_Union[StrategyImportResult, _Mapping]] = ...) -> None: ...

class ImportSkillforgeStrategyBundleRequest(_message.Message):
    __slots__ = ("source_bundle", "target_service_name", "mode", "conflict_policy", "dry_run", "allow_partial_sections", "allow_runtime_ref_mismatch")
    SOURCE_BUNDLE_FIELD_NUMBER: _ClassVar[int]
    TARGET_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    CONFLICT_POLICY_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    ALLOW_PARTIAL_SECTIONS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_RUNTIME_REF_MISMATCH_FIELD_NUMBER: _ClassVar[int]
    source_bundle: _struct_pb2.Struct
    target_service_name: str
    mode: StrategyImportMode
    conflict_policy: StrategyImportConflictPolicy
    dry_run: bool
    allow_partial_sections: bool
    allow_runtime_ref_mismatch: bool
    def __init__(self, source_bundle: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., target_service_name: _Optional[str] = ..., mode: _Optional[_Union[StrategyImportMode, str]] = ..., conflict_policy: _Optional[_Union[StrategyImportConflictPolicy, str]] = ..., dry_run: bool = ..., allow_partial_sections: bool = ..., allow_runtime_ref_mismatch: bool = ...) -> None: ...

class ImportSkillforgeStrategyBundleResponse(_message.Message):
    __slots__ = ("success", "generated_package", "notices", "import_job_id", "diagnostics", "plan", "result")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    GENERATED_PACKAGE_FIELD_NUMBER: _ClassVar[int]
    NOTICES_FIELD_NUMBER: _ClassVar[int]
    IMPORT_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    generated_package: BillingStrategyPackage
    notices: _containers.RepeatedScalarFieldContainer[str]
    import_job_id: str
    diagnostics: _containers.RepeatedCompositeFieldContainer[StrategyPackageDiagnostic]
    plan: StrategyImportPlan
    result: StrategyImportResult
    def __init__(self, success: bool = ..., generated_package: _Optional[_Union[BillingStrategyPackage, _Mapping]] = ..., notices: _Optional[_Iterable[str]] = ..., import_job_id: _Optional[str] = ..., diagnostics: _Optional[_Iterable[_Union[StrategyPackageDiagnostic, _Mapping]]] = ..., plan: _Optional[_Union[StrategyImportPlan, _Mapping]] = ..., result: _Optional[_Union[StrategyImportResult, _Mapping]] = ...) -> None: ...

class ExportStrategyPackageRequest(_message.Message):
    __slots__ = ("business_id", "sections", "strategy_key", "include_archived", "include_inactive_bundles", "include_pricing_views")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SECTIONS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_KEY_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_INACTIVE_BUNDLES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PRICING_VIEWS_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    sections: _containers.RepeatedScalarFieldContainer[StrategyPackageSection]
    strategy_key: str
    include_archived: bool
    include_inactive_bundles: bool
    include_pricing_views: bool
    def __init__(self, business_id: _Optional[str] = ..., sections: _Optional[_Iterable[_Union[StrategyPackageSection, str]]] = ..., strategy_key: _Optional[str] = ..., include_archived: bool = ..., include_inactive_bundles: bool = ..., include_pricing_views: bool = ...) -> None: ...

class ExportStrategyPackageResponse(_message.Message):
    __slots__ = ("package",)
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    package: BillingStrategyPackage
    def __init__(self, package: _Optional[_Union[BillingStrategyPackage, _Mapping]] = ...) -> None: ...

class GetStrategyImportJobRequest(_message.Message):
    __slots__ = ("job_id",)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class StrategyPackageDiagnostic(_message.Message):
    __slots__ = ("severity", "code", "path", "message")
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    severity: StrategyPackageDiagnosticSeverity
    code: str
    path: str
    message: str
    def __init__(self, severity: _Optional[_Union[StrategyPackageDiagnosticSeverity, str]] = ..., code: _Optional[str] = ..., path: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class StrategyImportPlanItem(_message.Message):
    __slots__ = ("object_type", "stable_key", "path", "planned_action", "message", "depends_on_keys")
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    STABLE_KEY_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    PLANNED_ACTION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DEPENDS_ON_KEYS_FIELD_NUMBER: _ClassVar[int]
    object_type: StrategyPackageObjectType
    stable_key: str
    path: str
    planned_action: StrategyImportAction
    message: str
    depends_on_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, object_type: _Optional[_Union[StrategyPackageObjectType, str]] = ..., stable_key: _Optional[str] = ..., path: _Optional[str] = ..., planned_action: _Optional[_Union[StrategyImportAction, str]] = ..., message: _Optional[str] = ..., depends_on_keys: _Optional[_Iterable[str]] = ...) -> None: ...

class StrategyImportPlan(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[StrategyImportPlanItem]
    def __init__(self, items: _Optional[_Iterable[_Union[StrategyImportPlanItem, _Mapping]]] = ...) -> None: ...

class StrategyImportCounts(_message.Message):
    __slots__ = ("create_count", "update_count", "reuse_count", "publish_count", "skip_count", "conflict_count")
    CREATE_COUNT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_COUNT_FIELD_NUMBER: _ClassVar[int]
    REUSE_COUNT_FIELD_NUMBER: _ClassVar[int]
    PUBLISH_COUNT_FIELD_NUMBER: _ClassVar[int]
    SKIP_COUNT_FIELD_NUMBER: _ClassVar[int]
    CONFLICT_COUNT_FIELD_NUMBER: _ClassVar[int]
    create_count: int
    update_count: int
    reuse_count: int
    publish_count: int
    skip_count: int
    conflict_count: int
    def __init__(self, create_count: _Optional[int] = ..., update_count: _Optional[int] = ..., reuse_count: _Optional[int] = ..., publish_count: _Optional[int] = ..., skip_count: _Optional[int] = ..., conflict_count: _Optional[int] = ...) -> None: ...

class StrategyImportObjectResult(_message.Message):
    __slots__ = ("object_type", "stable_key", "path", "action", "runtime_id", "message")
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    STABLE_KEY_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    object_type: StrategyPackageObjectType
    stable_key: str
    path: str
    action: StrategyImportAction
    runtime_id: str
    message: str
    def __init__(self, object_type: _Optional[_Union[StrategyPackageObjectType, str]] = ..., stable_key: _Optional[str] = ..., path: _Optional[str] = ..., action: _Optional[_Union[StrategyImportAction, str]] = ..., runtime_id: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class StrategyImportResult(_message.Message):
    __slots__ = ("objects", "counts")
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    COUNTS_FIELD_NUMBER: _ClassVar[int]
    objects: _containers.RepeatedCompositeFieldContainer[StrategyImportObjectResult]
    counts: StrategyImportCounts
    def __init__(self, objects: _Optional[_Iterable[_Union[StrategyImportObjectResult, _Mapping]]] = ..., counts: _Optional[_Union[StrategyImportCounts, _Mapping]] = ...) -> None: ...

class StrategyImportJob(_message.Message):
    __slots__ = ("job_id", "status", "dry_run", "mode", "conflict_policy", "created_at", "started_at", "completed_at", "plan", "result", "diagnostics")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    CONFLICT_POLICY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    status: StrategyImportJobStatus
    dry_run: bool
    mode: StrategyImportMode
    conflict_policy: StrategyImportConflictPolicy
    created_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    plan: StrategyImportPlan
    result: StrategyImportResult
    diagnostics: _containers.RepeatedCompositeFieldContainer[StrategyPackageDiagnostic]
    def __init__(self, job_id: _Optional[str] = ..., status: _Optional[_Union[StrategyImportJobStatus, str]] = ..., dry_run: bool = ..., mode: _Optional[_Union[StrategyImportMode, str]] = ..., conflict_policy: _Optional[_Union[StrategyImportConflictPolicy, str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., started_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., completed_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., plan: _Optional[_Union[StrategyImportPlan, _Mapping]] = ..., result: _Optional[_Union[StrategyImportResult, _Mapping]] = ..., diagnostics: _Optional[_Iterable[_Union[StrategyPackageDiagnostic, _Mapping]]] = ...) -> None: ...

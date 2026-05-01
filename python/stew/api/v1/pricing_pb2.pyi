import datetime

from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LocalizedText(_message.Message):
    __slots__ = ("fallback", "values")
    class ValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FALLBACK_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    fallback: str
    values: _containers.ScalarMap[str, str]
    def __init__(self, fallback: _Optional[str] = ..., values: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PricingCtaConfig(_message.Message):
    __slots__ = ("key", "label", "action_type", "href", "target", "plan_id", "billing_interval", "requires_auth", "event_name", "disabled_reason")
    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    HREF_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    BILLING_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_AUTH_FIELD_NUMBER: _ClassVar[int]
    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    DISABLED_REASON_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: LocalizedText
    action_type: str
    href: str
    target: str
    plan_id: str
    billing_interval: str
    requires_auth: bool
    event_name: str
    disabled_reason: LocalizedText
    def __init__(self, key: _Optional[str] = ..., label: _Optional[_Union[LocalizedText, _Mapping]] = ..., action_type: _Optional[str] = ..., href: _Optional[str] = ..., target: _Optional[str] = ..., plan_id: _Optional[str] = ..., billing_interval: _Optional[str] = ..., requires_auth: bool = ..., event_name: _Optional[str] = ..., disabled_reason: _Optional[_Union[LocalizedText, _Mapping]] = ...) -> None: ...

class PricingBadge(_message.Message):
    __slots__ = ("key", "label", "tone")
    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    TONE_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: LocalizedText
    tone: str
    def __init__(self, key: _Optional[str] = ..., label: _Optional[_Union[LocalizedText, _Mapping]] = ..., tone: _Optional[str] = ...) -> None: ...

class PricingAmountSet(_message.Message):
    __slots__ = ("currency_code", "currency_symbol", "monthly_amount_minor", "quarterly_amount_minor", "yearly_amount_minor", "one_time_amount_minor", "monthly_equivalent_minor", "billing_anchor_label", "trial_days", "contact_sales_only", "price_label_override")
    CURRENCY_CODE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    MONTHLY_AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    QUARTERLY_AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    YEARLY_AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    ONE_TIME_AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    MONTHLY_EQUIVALENT_MINOR_FIELD_NUMBER: _ClassVar[int]
    BILLING_ANCHOR_LABEL_FIELD_NUMBER: _ClassVar[int]
    TRIAL_DAYS_FIELD_NUMBER: _ClassVar[int]
    CONTACT_SALES_ONLY_FIELD_NUMBER: _ClassVar[int]
    PRICE_LABEL_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    currency_code: str
    currency_symbol: str
    monthly_amount_minor: int
    quarterly_amount_minor: int
    yearly_amount_minor: int
    one_time_amount_minor: int
    monthly_equivalent_minor: int
    billing_anchor_label: LocalizedText
    trial_days: int
    contact_sales_only: bool
    price_label_override: LocalizedText
    def __init__(self, currency_code: _Optional[str] = ..., currency_symbol: _Optional[str] = ..., monthly_amount_minor: _Optional[int] = ..., quarterly_amount_minor: _Optional[int] = ..., yearly_amount_minor: _Optional[int] = ..., one_time_amount_minor: _Optional[int] = ..., monthly_equivalent_minor: _Optional[int] = ..., billing_anchor_label: _Optional[_Union[LocalizedText, _Mapping]] = ..., trial_days: _Optional[int] = ..., contact_sales_only: bool = ..., price_label_override: _Optional[_Union[LocalizedText, _Mapping]] = ...) -> None: ...

class PricingHeroConfig(_message.Message):
    __slots__ = ("eyebrow", "title", "subtitle", "announcement", "primary_cta", "secondary_cta", "disclaimer", "align", "background_variant")
    EYEBROW_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SUBTITLE_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_CTA_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_CTA_FIELD_NUMBER: _ClassVar[int]
    DISCLAIMER_FIELD_NUMBER: _ClassVar[int]
    ALIGN_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_VARIANT_FIELD_NUMBER: _ClassVar[int]
    eyebrow: LocalizedText
    title: LocalizedText
    subtitle: LocalizedText
    announcement: LocalizedText
    primary_cta: PricingCtaConfig
    secondary_cta: PricingCtaConfig
    disclaimer: LocalizedText
    align: str
    background_variant: str
    def __init__(self, eyebrow: _Optional[_Union[LocalizedText, _Mapping]] = ..., title: _Optional[_Union[LocalizedText, _Mapping]] = ..., subtitle: _Optional[_Union[LocalizedText, _Mapping]] = ..., announcement: _Optional[_Union[LocalizedText, _Mapping]] = ..., primary_cta: _Optional[_Union[PricingCtaConfig, _Mapping]] = ..., secondary_cta: _Optional[_Union[PricingCtaConfig, _Mapping]] = ..., disclaimer: _Optional[_Union[LocalizedText, _Mapping]] = ..., align: _Optional[str] = ..., background_variant: _Optional[str] = ...) -> None: ...

class PricingBillingToggleIntervalLabel(_message.Message):
    __slots__ = ("interval", "label")
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    interval: str
    label: LocalizedText
    def __init__(self, interval: _Optional[str] = ..., label: _Optional[_Union[LocalizedText, _Mapping]] = ...) -> None: ...

class PricingBillingToggleConfig(_message.Message):
    __slots__ = ("enabled", "default_interval", "allowed_intervals", "annual_savings_mode", "annual_savings_label", "interval_labels", "note")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_INTERVALS_FIELD_NUMBER: _ClassVar[int]
    ANNUAL_SAVINGS_MODE_FIELD_NUMBER: _ClassVar[int]
    ANNUAL_SAVINGS_LABEL_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_LABELS_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    default_interval: str
    allowed_intervals: _containers.RepeatedScalarFieldContainer[str]
    annual_savings_mode: str
    annual_savings_label: LocalizedText
    interval_labels: _containers.RepeatedCompositeFieldContainer[PricingBillingToggleIntervalLabel]
    note: LocalizedText
    def __init__(self, enabled: bool = ..., default_interval: _Optional[str] = ..., allowed_intervals: _Optional[_Iterable[str]] = ..., annual_savings_mode: _Optional[str] = ..., annual_savings_label: _Optional[_Union[LocalizedText, _Mapping]] = ..., interval_labels: _Optional[_Iterable[_Union[PricingBillingToggleIntervalLabel, _Mapping]]] = ..., note: _Optional[_Union[LocalizedText, _Mapping]] = ...) -> None: ...

class PricingPlanPresentation(_message.Message):
    __slots__ = ("plan_id", "visible", "audience_label", "headline", "subheadline", "description", "featured", "featured_badge", "tier_tag", "sort_order", "price", "badges", "highlights", "cta", "footnote", "comparison_group", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    VISIBLE_FIELD_NUMBER: _ClassVar[int]
    AUDIENCE_LABEL_FIELD_NUMBER: _ClassVar[int]
    HEADLINE_FIELD_NUMBER: _ClassVar[int]
    SUBHEADLINE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FEATURED_FIELD_NUMBER: _ClassVar[int]
    FEATURED_BADGE_FIELD_NUMBER: _ClassVar[int]
    TIER_TAG_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    BADGES_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHTS_FIELD_NUMBER: _ClassVar[int]
    CTA_FIELD_NUMBER: _ClassVar[int]
    FOOTNOTE_FIELD_NUMBER: _ClassVar[int]
    COMPARISON_GROUP_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    plan_id: str
    visible: bool
    audience_label: LocalizedText
    headline: LocalizedText
    subheadline: LocalizedText
    description: LocalizedText
    featured: bool
    featured_badge: LocalizedText
    tier_tag: str
    sort_order: int
    price: PricingAmountSet
    badges: _containers.RepeatedCompositeFieldContainer[PricingBadge]
    highlights: _containers.RepeatedCompositeFieldContainer[LocalizedText]
    cta: PricingCtaConfig
    footnote: LocalizedText
    comparison_group: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, plan_id: _Optional[str] = ..., visible: bool = ..., audience_label: _Optional[_Union[LocalizedText, _Mapping]] = ..., headline: _Optional[_Union[LocalizedText, _Mapping]] = ..., subheadline: _Optional[_Union[LocalizedText, _Mapping]] = ..., description: _Optional[_Union[LocalizedText, _Mapping]] = ..., featured: bool = ..., featured_badge: _Optional[_Union[LocalizedText, _Mapping]] = ..., tier_tag: _Optional[str] = ..., sort_order: _Optional[int] = ..., price: _Optional[_Union[PricingAmountSet, _Mapping]] = ..., badges: _Optional[_Iterable[_Union[PricingBadge, _Mapping]]] = ..., highlights: _Optional[_Iterable[_Union[LocalizedText, _Mapping]]] = ..., cta: _Optional[_Union[PricingCtaConfig, _Mapping]] = ..., footnote: _Optional[_Union[LocalizedText, _Mapping]] = ..., comparison_group: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PricingComparisonValueConfig(_message.Message):
    __slots__ = ("included", "text", "numeric_value", "unit", "emphasis")
    INCLUDED_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    NUMERIC_VALUE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    EMPHASIS_FIELD_NUMBER: _ClassVar[int]
    included: bool
    text: LocalizedText
    numeric_value: float
    unit: str
    emphasis: bool
    def __init__(self, included: bool = ..., text: _Optional[_Union[LocalizedText, _Mapping]] = ..., numeric_value: _Optional[float] = ..., unit: _Optional[str] = ..., emphasis: bool = ...) -> None: ...

class PricingComparisonPlanValue(_message.Message):
    __slots__ = ("plan_id", "value")
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    plan_id: str
    value: PricingComparisonValueConfig
    def __init__(self, plan_id: _Optional[str] = ..., value: _Optional[_Union[PricingComparisonValueConfig, _Mapping]] = ...) -> None: ...

class PricingComparisonRowConfig(_message.Message):
    __slots__ = ("key", "label", "description", "kind", "values_by_plan")
    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    VALUES_BY_PLAN_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: LocalizedText
    description: LocalizedText
    kind: str
    values_by_plan: _containers.RepeatedCompositeFieldContainer[PricingComparisonPlanValue]
    def __init__(self, key: _Optional[str] = ..., label: _Optional[_Union[LocalizedText, _Mapping]] = ..., description: _Optional[_Union[LocalizedText, _Mapping]] = ..., kind: _Optional[str] = ..., values_by_plan: _Optional[_Iterable[_Union[PricingComparisonPlanValue, _Mapping]]] = ...) -> None: ...

class PricingComparisonTableConfig(_message.Message):
    __slots__ = ("enabled", "title", "description", "columns", "rows", "sticky_header", "default_expanded")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    STICKY_HEADER_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_EXPANDED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    title: LocalizedText
    description: LocalizedText
    columns: _containers.RepeatedScalarFieldContainer[str]
    rows: _containers.RepeatedCompositeFieldContainer[PricingComparisonRowConfig]
    sticky_header: bool
    default_expanded: bool
    def __init__(self, enabled: bool = ..., title: _Optional[_Union[LocalizedText, _Mapping]] = ..., description: _Optional[_Union[LocalizedText, _Mapping]] = ..., columns: _Optional[_Iterable[str]] = ..., rows: _Optional[_Iterable[_Union[PricingComparisonRowConfig, _Mapping]]] = ..., sticky_header: bool = ..., default_expanded: bool = ...) -> None: ...

class PricingFaqItem(_message.Message):
    __slots__ = ("key", "question", "answer", "category")
    KEY_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    key: str
    question: LocalizedText
    answer: LocalizedText
    category: str
    def __init__(self, key: _Optional[str] = ..., question: _Optional[_Union[LocalizedText, _Mapping]] = ..., answer: _Optional[_Union[LocalizedText, _Mapping]] = ..., category: _Optional[str] = ...) -> None: ...

class PricingFaqSectionConfig(_message.Message):
    __slots__ = ("enabled", "title", "items")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    title: LocalizedText
    items: _containers.RepeatedCompositeFieldContainer[PricingFaqItem]
    def __init__(self, enabled: bool = ..., title: _Optional[_Union[LocalizedText, _Mapping]] = ..., items: _Optional[_Iterable[_Union[PricingFaqItem, _Mapping]]] = ...) -> None: ...

class PricingTrustItem(_message.Message):
    __slots__ = ("key", "title", "description", "icon")
    KEY_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    key: str
    title: LocalizedText
    description: LocalizedText
    icon: str
    def __init__(self, key: _Optional[str] = ..., title: _Optional[_Union[LocalizedText, _Mapping]] = ..., description: _Optional[_Union[LocalizedText, _Mapping]] = ..., icon: _Optional[str] = ...) -> None: ...

class PricingTrustSectionConfig(_message.Message):
    __slots__ = ("title", "items", "note")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    title: LocalizedText
    items: _containers.RepeatedCompositeFieldContainer[PricingTrustItem]
    note: LocalizedText
    def __init__(self, title: _Optional[_Union[LocalizedText, _Mapping]] = ..., items: _Optional[_Iterable[_Union[PricingTrustItem, _Mapping]]] = ..., note: _Optional[_Union[LocalizedText, _Mapping]] = ...) -> None: ...

class PricingThemeOverrideCssVar(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class PricingThemeOverrideConfig(_message.Message):
    __slots__ = ("mode", "accent_color", "accent_text_color", "surface_color", "surface_muted_color", "border_color", "hero_background", "featured_ring_color", "radius_scale", "font_family_heading", "font_family_body", "compact", "raw_css_vars")
    MODE_FIELD_NUMBER: _ClassVar[int]
    ACCENT_COLOR_FIELD_NUMBER: _ClassVar[int]
    ACCENT_TEXT_COLOR_FIELD_NUMBER: _ClassVar[int]
    SURFACE_COLOR_FIELD_NUMBER: _ClassVar[int]
    SURFACE_MUTED_COLOR_FIELD_NUMBER: _ClassVar[int]
    BORDER_COLOR_FIELD_NUMBER: _ClassVar[int]
    HERO_BACKGROUND_FIELD_NUMBER: _ClassVar[int]
    FEATURED_RING_COLOR_FIELD_NUMBER: _ClassVar[int]
    RADIUS_SCALE_FIELD_NUMBER: _ClassVar[int]
    FONT_FAMILY_HEADING_FIELD_NUMBER: _ClassVar[int]
    FONT_FAMILY_BODY_FIELD_NUMBER: _ClassVar[int]
    COMPACT_FIELD_NUMBER: _ClassVar[int]
    RAW_CSS_VARS_FIELD_NUMBER: _ClassVar[int]
    mode: str
    accent_color: str
    accent_text_color: str
    surface_color: str
    surface_muted_color: str
    border_color: str
    hero_background: str
    featured_ring_color: str
    radius_scale: str
    font_family_heading: str
    font_family_body: str
    compact: bool
    raw_css_vars: _containers.RepeatedCompositeFieldContainer[PricingThemeOverrideCssVar]
    def __init__(self, mode: _Optional[str] = ..., accent_color: _Optional[str] = ..., accent_text_color: _Optional[str] = ..., surface_color: _Optional[str] = ..., surface_muted_color: _Optional[str] = ..., border_color: _Optional[str] = ..., hero_background: _Optional[str] = ..., featured_ring_color: _Optional[str] = ..., radius_scale: _Optional[str] = ..., font_family_heading: _Optional[str] = ..., font_family_body: _Optional[str] = ..., compact: bool = ..., raw_css_vars: _Optional[_Iterable[_Union[PricingThemeOverrideCssVar, _Mapping]]] = ...) -> None: ...

class PricingPurchaseBehaviorConfig(_message.Message):
    __slots__ = ("default_mode", "allow_anonymous_purchase_cta", "sign_in_cta", "contact_sales_cta", "success_redirect_path", "cancel_redirect_path", "checkout_provider_hint")
    DEFAULT_MODE_FIELD_NUMBER: _ClassVar[int]
    ALLOW_ANONYMOUS_PURCHASE_CTA_FIELD_NUMBER: _ClassVar[int]
    SIGN_IN_CTA_FIELD_NUMBER: _ClassVar[int]
    CONTACT_SALES_CTA_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_REDIRECT_PATH_FIELD_NUMBER: _ClassVar[int]
    CANCEL_REDIRECT_PATH_FIELD_NUMBER: _ClassVar[int]
    CHECKOUT_PROVIDER_HINT_FIELD_NUMBER: _ClassVar[int]
    default_mode: str
    allow_anonymous_purchase_cta: bool
    sign_in_cta: PricingCtaConfig
    contact_sales_cta: PricingCtaConfig
    success_redirect_path: str
    cancel_redirect_path: str
    checkout_provider_hint: str
    def __init__(self, default_mode: _Optional[str] = ..., allow_anonymous_purchase_cta: bool = ..., sign_in_cta: _Optional[_Union[PricingCtaConfig, _Mapping]] = ..., contact_sales_cta: _Optional[_Union[PricingCtaConfig, _Mapping]] = ..., success_redirect_path: _Optional[str] = ..., cancel_redirect_path: _Optional[str] = ..., checkout_provider_hint: _Optional[str] = ...) -> None: ...

class PricingVisibilityRules(_message.Message):
    __slots__ = ("hide_inactive_plans", "hide_internal_plans", "allowed_plan_ids", "blocked_plan_ids", "require_metadata_public_true")
    HIDE_INACTIVE_PLANS_FIELD_NUMBER: _ClassVar[int]
    HIDE_INTERNAL_PLANS_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_PLAN_IDS_FIELD_NUMBER: _ClassVar[int]
    BLOCKED_PLAN_IDS_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_METADATA_PUBLIC_TRUE_FIELD_NUMBER: _ClassVar[int]
    hide_inactive_plans: bool
    hide_internal_plans: bool
    allowed_plan_ids: _containers.RepeatedScalarFieldContainer[str]
    blocked_plan_ids: _containers.RepeatedScalarFieldContainer[str]
    require_metadata_public_true: bool
    def __init__(self, hide_inactive_plans: bool = ..., hide_internal_plans: bool = ..., allowed_plan_ids: _Optional[_Iterable[str]] = ..., blocked_plan_ids: _Optional[_Iterable[str]] = ..., require_metadata_public_true: bool = ...) -> None: ...

class PricingConfig(_message.Message):
    __slots__ = ("schema_version", "business_id", "page_key", "status", "default_locale", "supported_locales", "page_title", "meta_description", "canonical_path", "hero", "billing_toggle", "plan_presentations", "comparison_table", "faq", "bottom_ctas", "trust_section", "footer_note", "theme_overrides", "purchase_behavior", "visibility_rules")
    SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_LOCALE_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_LOCALES_FIELD_NUMBER: _ClassVar[int]
    PAGE_TITLE_FIELD_NUMBER: _ClassVar[int]
    META_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CANONICAL_PATH_FIELD_NUMBER: _ClassVar[int]
    HERO_FIELD_NUMBER: _ClassVar[int]
    BILLING_TOGGLE_FIELD_NUMBER: _ClassVar[int]
    PLAN_PRESENTATIONS_FIELD_NUMBER: _ClassVar[int]
    COMPARISON_TABLE_FIELD_NUMBER: _ClassVar[int]
    FAQ_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_CTAS_FIELD_NUMBER: _ClassVar[int]
    TRUST_SECTION_FIELD_NUMBER: _ClassVar[int]
    FOOTER_NOTE_FIELD_NUMBER: _ClassVar[int]
    THEME_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_RULES_FIELD_NUMBER: _ClassVar[int]
    schema_version: str
    business_id: str
    page_key: str
    status: str
    default_locale: str
    supported_locales: _containers.RepeatedScalarFieldContainer[str]
    page_title: LocalizedText
    meta_description: LocalizedText
    canonical_path: str
    hero: PricingHeroConfig
    billing_toggle: PricingBillingToggleConfig
    plan_presentations: _containers.RepeatedCompositeFieldContainer[PricingPlanPresentation]
    comparison_table: PricingComparisonTableConfig
    faq: PricingFaqSectionConfig
    bottom_ctas: _containers.RepeatedCompositeFieldContainer[PricingCtaConfig]
    trust_section: PricingTrustSectionConfig
    footer_note: LocalizedText
    theme_overrides: PricingThemeOverrideConfig
    purchase_behavior: PricingPurchaseBehaviorConfig
    visibility_rules: PricingVisibilityRules
    def __init__(self, schema_version: _Optional[str] = ..., business_id: _Optional[str] = ..., page_key: _Optional[str] = ..., status: _Optional[str] = ..., default_locale: _Optional[str] = ..., supported_locales: _Optional[_Iterable[str]] = ..., page_title: _Optional[_Union[LocalizedText, _Mapping]] = ..., meta_description: _Optional[_Union[LocalizedText, _Mapping]] = ..., canonical_path: _Optional[str] = ..., hero: _Optional[_Union[PricingHeroConfig, _Mapping]] = ..., billing_toggle: _Optional[_Union[PricingBillingToggleConfig, _Mapping]] = ..., plan_presentations: _Optional[_Iterable[_Union[PricingPlanPresentation, _Mapping]]] = ..., comparison_table: _Optional[_Union[PricingComparisonTableConfig, _Mapping]] = ..., faq: _Optional[_Union[PricingFaqSectionConfig, _Mapping]] = ..., bottom_ctas: _Optional[_Iterable[_Union[PricingCtaConfig, _Mapping]]] = ..., trust_section: _Optional[_Union[PricingTrustSectionConfig, _Mapping]] = ..., footer_note: _Optional[_Union[LocalizedText, _Mapping]] = ..., theme_overrides: _Optional[_Union[PricingThemeOverrideConfig, _Mapping]] = ..., purchase_behavior: _Optional[_Union[PricingPurchaseBehaviorConfig, _Mapping]] = ..., visibility_rules: _Optional[_Union[PricingVisibilityRules, _Mapping]] = ...) -> None: ...

class GetPricingPageRequest(_message.Message):
    __slots__ = ("business_id", "locale", "page_key")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    PAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    locale: str
    page_key: str
    def __init__(self, business_id: _Optional[str] = ..., locale: _Optional[str] = ..., page_key: _Optional[str] = ...) -> None: ...

class PricingRevisionInfo(_message.Message):
    __slots__ = ("active_version_id", "display_version", "published_at", "etag", "source_mode")
    ACTIVE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_VERSION_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_AT_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    SOURCE_MODE_FIELD_NUMBER: _ClassVar[int]
    active_version_id: str
    display_version: str
    published_at: _timestamp_pb2.Timestamp
    etag: str
    source_mode: str
    def __init__(self, active_version_id: _Optional[str] = ..., display_version: _Optional[str] = ..., published_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., etag: _Optional[str] = ..., source_mode: _Optional[str] = ...) -> None: ...

class PricingHeroResolved(_message.Message):
    __slots__ = ("title", "eyebrow", "subtitle", "announcement", "disclaimer", "align", "background_variant", "primary_cta", "secondary_cta")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    EYEBROW_FIELD_NUMBER: _ClassVar[int]
    SUBTITLE_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_FIELD_NUMBER: _ClassVar[int]
    DISCLAIMER_FIELD_NUMBER: _ClassVar[int]
    ALIGN_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_VARIANT_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_CTA_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_CTA_FIELD_NUMBER: _ClassVar[int]
    title: str
    eyebrow: str
    subtitle: str
    announcement: str
    disclaimer: str
    align: str
    background_variant: str
    primary_cta: PricingCtaResolved
    secondary_cta: PricingCtaResolved
    def __init__(self, title: _Optional[str] = ..., eyebrow: _Optional[str] = ..., subtitle: _Optional[str] = ..., announcement: _Optional[str] = ..., disclaimer: _Optional[str] = ..., align: _Optional[str] = ..., background_variant: _Optional[str] = ..., primary_cta: _Optional[_Union[PricingCtaResolved, _Mapping]] = ..., secondary_cta: _Optional[_Union[PricingCtaResolved, _Mapping]] = ...) -> None: ...

class PricingBillingToggleResolvedIntervalLabel(_message.Message):
    __slots__ = ("interval", "label")
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    interval: str
    label: str
    def __init__(self, interval: _Optional[str] = ..., label: _Optional[str] = ...) -> None: ...

class PricingBillingToggleResolved(_message.Message):
    __slots__ = ("enabled", "default_interval", "allowed_intervals", "annual_savings_mode", "annual_savings_label", "interval_labels", "note")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_INTERVALS_FIELD_NUMBER: _ClassVar[int]
    ANNUAL_SAVINGS_MODE_FIELD_NUMBER: _ClassVar[int]
    ANNUAL_SAVINGS_LABEL_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_LABELS_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    default_interval: str
    allowed_intervals: _containers.RepeatedScalarFieldContainer[str]
    annual_savings_mode: str
    annual_savings_label: str
    interval_labels: _containers.RepeatedCompositeFieldContainer[PricingBillingToggleResolvedIntervalLabel]
    note: str
    def __init__(self, enabled: bool = ..., default_interval: _Optional[str] = ..., allowed_intervals: _Optional[_Iterable[str]] = ..., annual_savings_mode: _Optional[str] = ..., annual_savings_label: _Optional[str] = ..., interval_labels: _Optional[_Iterable[_Union[PricingBillingToggleResolvedIntervalLabel, _Mapping]]] = ..., note: _Optional[str] = ...) -> None: ...

class PricingBadgeResolved(_message.Message):
    __slots__ = ("key", "label", "tone")
    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    TONE_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: str
    tone: str
    def __init__(self, key: _Optional[str] = ..., label: _Optional[str] = ..., tone: _Optional[str] = ...) -> None: ...

class PricingCtaResolved(_message.Message):
    __slots__ = ("key", "label", "action_type", "href", "target", "plan_id", "billing_interval", "requires_auth", "event_name", "disabled_reason")
    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    HREF_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    BILLING_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_AUTH_FIELD_NUMBER: _ClassVar[int]
    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    DISABLED_REASON_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: str
    action_type: str
    href: str
    target: str
    plan_id: str
    billing_interval: str
    requires_auth: bool
    event_name: str
    disabled_reason: str
    def __init__(self, key: _Optional[str] = ..., label: _Optional[str] = ..., action_type: _Optional[str] = ..., href: _Optional[str] = ..., target: _Optional[str] = ..., plan_id: _Optional[str] = ..., billing_interval: _Optional[str] = ..., requires_auth: bool = ..., event_name: _Optional[str] = ..., disabled_reason: _Optional[str] = ...) -> None: ...

class PricingResolvedAmount(_message.Message):
    __slots__ = ("selected_interval", "currency_code", "currency_symbol", "amount_minor", "monthly_equivalent_minor", "billing_anchor_label", "savings_label", "is_contact_sales", "display_text")
    SELECTED_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_CODE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    MONTHLY_EQUIVALENT_MINOR_FIELD_NUMBER: _ClassVar[int]
    BILLING_ANCHOR_LABEL_FIELD_NUMBER: _ClassVar[int]
    SAVINGS_LABEL_FIELD_NUMBER: _ClassVar[int]
    IS_CONTACT_SALES_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_TEXT_FIELD_NUMBER: _ClassVar[int]
    selected_interval: str
    currency_code: str
    currency_symbol: str
    amount_minor: int
    monthly_equivalent_minor: int
    billing_anchor_label: str
    savings_label: str
    is_contact_sales: bool
    display_text: str
    def __init__(self, selected_interval: _Optional[str] = ..., currency_code: _Optional[str] = ..., currency_symbol: _Optional[str] = ..., amount_minor: _Optional[int] = ..., monthly_equivalent_minor: _Optional[int] = ..., billing_anchor_label: _Optional[str] = ..., savings_label: _Optional[str] = ..., is_contact_sales: bool = ..., display_text: _Optional[str] = ...) -> None: ...

class PricingFeatureResolved(_message.Message):
    __slots__ = ("key", "label", "included", "detail")
    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    INCLUDED_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: str
    included: bool
    detail: str
    def __init__(self, key: _Optional[str] = ..., label: _Optional[str] = ..., included: bool = ..., detail: _Optional[str] = ...) -> None: ...

class PricingQuotaResolved(_message.Message):
    __slots__ = ("key", "label", "limit", "unit", "reset_period", "display_text")
    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    RESET_PERIOD_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_TEXT_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: str
    limit: float
    unit: str
    reset_period: str
    display_text: str
    def __init__(self, key: _Optional[str] = ..., label: _Optional[str] = ..., limit: _Optional[float] = ..., unit: _Optional[str] = ..., reset_period: _Optional[str] = ..., display_text: _Optional[str] = ...) -> None: ...

class PricingPlanStateResolved(_message.Message):
    __slots__ = ("is_current_plan", "can_purchase", "can_upgrade", "can_downgrade", "requires_sign_in", "action_label", "disabled_reason", "subject_context_present", "subscription_id", "target_billing_interval")
    IS_CURRENT_PLAN_FIELD_NUMBER: _ClassVar[int]
    CAN_PURCHASE_FIELD_NUMBER: _ClassVar[int]
    CAN_UPGRADE_FIELD_NUMBER: _ClassVar[int]
    CAN_DOWNGRADE_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_SIGN_IN_FIELD_NUMBER: _ClassVar[int]
    ACTION_LABEL_FIELD_NUMBER: _ClassVar[int]
    DISABLED_REASON_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_CONTEXT_PRESENT_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_BILLING_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    is_current_plan: bool
    can_purchase: bool
    can_upgrade: bool
    can_downgrade: bool
    requires_sign_in: bool
    action_label: str
    disabled_reason: str
    subject_context_present: bool
    subscription_id: str
    target_billing_interval: str
    def __init__(self, is_current_plan: bool = ..., can_purchase: bool = ..., can_upgrade: bool = ..., can_downgrade: bool = ..., requires_sign_in: bool = ..., action_label: _Optional[str] = ..., disabled_reason: _Optional[str] = ..., subject_context_present: bool = ..., subscription_id: _Optional[str] = ..., target_billing_interval: _Optional[str] = ...) -> None: ...

class PricingPlanResolved(_message.Message):
    __slots__ = ("plan_id", "name", "description", "audience_label", "featured", "featured_badge", "price", "highlights", "enabled_features", "quotas", "badges", "cta", "footnote", "current_state")
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    AUDIENCE_LABEL_FIELD_NUMBER: _ClassVar[int]
    FEATURED_FIELD_NUMBER: _ClassVar[int]
    FEATURED_BADGE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHTS_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FEATURES_FIELD_NUMBER: _ClassVar[int]
    QUOTAS_FIELD_NUMBER: _ClassVar[int]
    BADGES_FIELD_NUMBER: _ClassVar[int]
    CTA_FIELD_NUMBER: _ClassVar[int]
    FOOTNOTE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATE_FIELD_NUMBER: _ClassVar[int]
    plan_id: str
    name: str
    description: str
    audience_label: str
    featured: bool
    featured_badge: str
    price: PricingResolvedAmount
    highlights: _containers.RepeatedScalarFieldContainer[str]
    enabled_features: _containers.RepeatedCompositeFieldContainer[PricingFeatureResolved]
    quotas: _containers.RepeatedCompositeFieldContainer[PricingQuotaResolved]
    badges: _containers.RepeatedCompositeFieldContainer[PricingBadgeResolved]
    cta: PricingCtaResolved
    footnote: str
    current_state: PricingPlanStateResolved
    def __init__(self, plan_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., audience_label: _Optional[str] = ..., featured: bool = ..., featured_badge: _Optional[str] = ..., price: _Optional[_Union[PricingResolvedAmount, _Mapping]] = ..., highlights: _Optional[_Iterable[str]] = ..., enabled_features: _Optional[_Iterable[_Union[PricingFeatureResolved, _Mapping]]] = ..., quotas: _Optional[_Iterable[_Union[PricingQuotaResolved, _Mapping]]] = ..., badges: _Optional[_Iterable[_Union[PricingBadgeResolved, _Mapping]]] = ..., cta: _Optional[_Union[PricingCtaResolved, _Mapping]] = ..., footnote: _Optional[str] = ..., current_state: _Optional[_Union[PricingPlanStateResolved, _Mapping]] = ...) -> None: ...

class PricingComparisonValueResolved(_message.Message):
    __slots__ = ("included", "text", "numeric_value", "unit", "emphasis")
    INCLUDED_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    NUMERIC_VALUE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    EMPHASIS_FIELD_NUMBER: _ClassVar[int]
    included: bool
    text: str
    numeric_value: float
    unit: str
    emphasis: bool
    def __init__(self, included: bool = ..., text: _Optional[str] = ..., numeric_value: _Optional[float] = ..., unit: _Optional[str] = ..., emphasis: bool = ...) -> None: ...

class PricingComparisonPlanValueResolved(_message.Message):
    __slots__ = ("plan_id", "value")
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    plan_id: str
    value: PricingComparisonValueResolved
    def __init__(self, plan_id: _Optional[str] = ..., value: _Optional[_Union[PricingComparisonValueResolved, _Mapping]] = ...) -> None: ...

class PricingComparisonRowResolved(_message.Message):
    __slots__ = ("key", "label", "description", "kind", "values_by_plan")
    KEY_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    VALUES_BY_PLAN_FIELD_NUMBER: _ClassVar[int]
    key: str
    label: str
    description: str
    kind: str
    values_by_plan: _containers.RepeatedCompositeFieldContainer[PricingComparisonPlanValueResolved]
    def __init__(self, key: _Optional[str] = ..., label: _Optional[str] = ..., description: _Optional[str] = ..., kind: _Optional[str] = ..., values_by_plan: _Optional[_Iterable[_Union[PricingComparisonPlanValueResolved, _Mapping]]] = ...) -> None: ...

class PricingComparisonTableResolved(_message.Message):
    __slots__ = ("enabled", "title", "description", "columns", "rows", "sticky_header", "default_expanded")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    STICKY_HEADER_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_EXPANDED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    title: str
    description: str
    columns: _containers.RepeatedScalarFieldContainer[str]
    rows: _containers.RepeatedCompositeFieldContainer[PricingComparisonRowResolved]
    sticky_header: bool
    default_expanded: bool
    def __init__(self, enabled: bool = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., columns: _Optional[_Iterable[str]] = ..., rows: _Optional[_Iterable[_Union[PricingComparisonRowResolved, _Mapping]]] = ..., sticky_header: bool = ..., default_expanded: bool = ...) -> None: ...

class PricingFaqItemResolved(_message.Message):
    __slots__ = ("key", "question", "answer", "category")
    KEY_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    key: str
    question: str
    answer: str
    category: str
    def __init__(self, key: _Optional[str] = ..., question: _Optional[str] = ..., answer: _Optional[str] = ..., category: _Optional[str] = ...) -> None: ...

class PricingFaqSectionResolved(_message.Message):
    __slots__ = ("enabled", "title", "items")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    title: str
    items: _containers.RepeatedCompositeFieldContainer[PricingFaqItemResolved]
    def __init__(self, enabled: bool = ..., title: _Optional[str] = ..., items: _Optional[_Iterable[_Union[PricingFaqItemResolved, _Mapping]]] = ...) -> None: ...

class PricingTrustItemResolved(_message.Message):
    __slots__ = ("key", "title", "description", "icon")
    KEY_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    key: str
    title: str
    description: str
    icon: str
    def __init__(self, key: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., icon: _Optional[str] = ...) -> None: ...

class PricingTrustSectionResolved(_message.Message):
    __slots__ = ("title", "items", "note")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    title: str
    items: _containers.RepeatedCompositeFieldContainer[PricingTrustItemResolved]
    note: str
    def __init__(self, title: _Optional[str] = ..., items: _Optional[_Iterable[_Union[PricingTrustItemResolved, _Mapping]]] = ..., note: _Optional[str] = ...) -> None: ...

class PricingThemeResolved(_message.Message):
    __slots__ = ("mode", "accent_color", "accent_text_color", "surface_color", "surface_muted_color", "border_color", "hero_background", "featured_ring_color", "radius_scale", "font_family_heading", "font_family_body", "compact")
    MODE_FIELD_NUMBER: _ClassVar[int]
    ACCENT_COLOR_FIELD_NUMBER: _ClassVar[int]
    ACCENT_TEXT_COLOR_FIELD_NUMBER: _ClassVar[int]
    SURFACE_COLOR_FIELD_NUMBER: _ClassVar[int]
    SURFACE_MUTED_COLOR_FIELD_NUMBER: _ClassVar[int]
    BORDER_COLOR_FIELD_NUMBER: _ClassVar[int]
    HERO_BACKGROUND_FIELD_NUMBER: _ClassVar[int]
    FEATURED_RING_COLOR_FIELD_NUMBER: _ClassVar[int]
    RADIUS_SCALE_FIELD_NUMBER: _ClassVar[int]
    FONT_FAMILY_HEADING_FIELD_NUMBER: _ClassVar[int]
    FONT_FAMILY_BODY_FIELD_NUMBER: _ClassVar[int]
    COMPACT_FIELD_NUMBER: _ClassVar[int]
    mode: str
    accent_color: str
    accent_text_color: str
    surface_color: str
    surface_muted_color: str
    border_color: str
    hero_background: str
    featured_ring_color: str
    radius_scale: str
    font_family_heading: str
    font_family_body: str
    compact: bool
    def __init__(self, mode: _Optional[str] = ..., accent_color: _Optional[str] = ..., accent_text_color: _Optional[str] = ..., surface_color: _Optional[str] = ..., surface_muted_color: _Optional[str] = ..., border_color: _Optional[str] = ..., hero_background: _Optional[str] = ..., featured_ring_color: _Optional[str] = ..., radius_scale: _Optional[str] = ..., font_family_heading: _Optional[str] = ..., font_family_body: _Optional[str] = ..., compact: bool = ...) -> None: ...

class PricingPageResponse(_message.Message):
    __slots__ = ("business_id", "page_key", "locale", "default_locale", "revision", "hero", "billing_toggle", "plans", "comparison_table", "faq", "bottom_ctas", "trust_section", "footer_note", "theme", "purchase_mode")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_LOCALE_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    HERO_FIELD_NUMBER: _ClassVar[int]
    BILLING_TOGGLE_FIELD_NUMBER: _ClassVar[int]
    PLANS_FIELD_NUMBER: _ClassVar[int]
    COMPARISON_TABLE_FIELD_NUMBER: _ClassVar[int]
    FAQ_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_CTAS_FIELD_NUMBER: _ClassVar[int]
    TRUST_SECTION_FIELD_NUMBER: _ClassVar[int]
    FOOTER_NOTE_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_MODE_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    page_key: str
    locale: str
    default_locale: str
    revision: PricingRevisionInfo
    hero: PricingHeroResolved
    billing_toggle: PricingBillingToggleResolved
    plans: _containers.RepeatedCompositeFieldContainer[PricingPlanResolved]
    comparison_table: PricingComparisonTableResolved
    faq: PricingFaqSectionResolved
    bottom_ctas: _containers.RepeatedCompositeFieldContainer[PricingCtaResolved]
    trust_section: PricingTrustSectionResolved
    footer_note: str
    theme: PricingThemeResolved
    purchase_mode: str
    def __init__(self, business_id: _Optional[str] = ..., page_key: _Optional[str] = ..., locale: _Optional[str] = ..., default_locale: _Optional[str] = ..., revision: _Optional[_Union[PricingRevisionInfo, _Mapping]] = ..., hero: _Optional[_Union[PricingHeroResolved, _Mapping]] = ..., billing_toggle: _Optional[_Union[PricingBillingToggleResolved, _Mapping]] = ..., plans: _Optional[_Iterable[_Union[PricingPlanResolved, _Mapping]]] = ..., comparison_table: _Optional[_Union[PricingComparisonTableResolved, _Mapping]] = ..., faq: _Optional[_Union[PricingFaqSectionResolved, _Mapping]] = ..., bottom_ctas: _Optional[_Iterable[_Union[PricingCtaResolved, _Mapping]]] = ..., trust_section: _Optional[_Union[PricingTrustSectionResolved, _Mapping]] = ..., footer_note: _Optional[str] = ..., theme: _Optional[_Union[PricingThemeResolved, _Mapping]] = ..., purchase_mode: _Optional[str] = ...) -> None: ...

from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from stew.api.v1 import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PaymentProviderKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAYMENT_PROVIDER_KIND_UNSPECIFIED: _ClassVar[PaymentProviderKind]
    PAYMENT_PROVIDER_KIND_STRIPE: _ClassVar[PaymentProviderKind]
    PAYMENT_PROVIDER_KIND_CREEM: _ClassVar[PaymentProviderKind]

class PaymentOrderStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAYMENT_ORDER_STATUS_UNSPECIFIED: _ClassVar[PaymentOrderStatus]
    PAYMENT_ORDER_STATUS_PENDING: _ClassVar[PaymentOrderStatus]
    PAYMENT_ORDER_STATUS_PAID: _ClassVar[PaymentOrderStatus]
    PAYMENT_ORDER_STATUS_FAILED: _ClassVar[PaymentOrderStatus]
    PAYMENT_ORDER_STATUS_REFUNDED: _ClassVar[PaymentOrderStatus]
    PAYMENT_ORDER_STATUS_CANCELED: _ClassVar[PaymentOrderStatus]
    PAYMENT_ORDER_STATUS_EXPIRED: _ClassVar[PaymentOrderStatus]

class PaymentBillingInterval(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAYMENT_BILLING_INTERVAL_UNSPECIFIED: _ClassVar[PaymentBillingInterval]
    PAYMENT_BILLING_INTERVAL_ONE_TIME: _ClassVar[PaymentBillingInterval]
    PAYMENT_BILLING_INTERVAL_MONTHLY: _ClassVar[PaymentBillingInterval]
    PAYMENT_BILLING_INTERVAL_QUARTERLY: _ClassVar[PaymentBillingInterval]
    PAYMENT_BILLING_INTERVAL_YEARLY: _ClassVar[PaymentBillingInterval]

class PaymentEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAYMENT_EVENT_TYPE_UNSPECIFIED: _ClassVar[PaymentEventType]
    PAYMENT_EVENT_TYPE_CHECKOUT_COMPLETED: _ClassVar[PaymentEventType]
    PAYMENT_EVENT_TYPE_PAYMENT_SUCCEEDED: _ClassVar[PaymentEventType]
    PAYMENT_EVENT_TYPE_PAYMENT_FAILED: _ClassVar[PaymentEventType]
    PAYMENT_EVENT_TYPE_SUBSCRIPTION_CREATED: _ClassVar[PaymentEventType]
    PAYMENT_EVENT_TYPE_SUBSCRIPTION_RENEWED: _ClassVar[PaymentEventType]
    PAYMENT_EVENT_TYPE_SUBSCRIPTION_CANCELED: _ClassVar[PaymentEventType]
    PAYMENT_EVENT_TYPE_REFUND_CREATED: _ClassVar[PaymentEventType]
    PAYMENT_EVENT_TYPE_CHARGE_DISPUTED: _ClassVar[PaymentEventType]

class RefundRequestStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REFUND_REQUEST_STATUS_UNSPECIFIED: _ClassVar[RefundRequestStatus]
    REFUND_REQUEST_STATUS_PENDING_APPROVAL: _ClassVar[RefundRequestStatus]
    REFUND_REQUEST_STATUS_APPROVED: _ClassVar[RefundRequestStatus]
    REFUND_REQUEST_STATUS_REJECTED: _ClassVar[RefundRequestStatus]
    REFUND_REQUEST_STATUS_CANCELED: _ClassVar[RefundRequestStatus]
    REFUND_REQUEST_STATUS_PROCESSING: _ClassVar[RefundRequestStatus]
    REFUND_REQUEST_STATUS_SUCCEEDED: _ClassVar[RefundRequestStatus]
    REFUND_REQUEST_STATUS_FAILED: _ClassVar[RefundRequestStatus]
PAYMENT_PROVIDER_KIND_UNSPECIFIED: PaymentProviderKind
PAYMENT_PROVIDER_KIND_STRIPE: PaymentProviderKind
PAYMENT_PROVIDER_KIND_CREEM: PaymentProviderKind
PAYMENT_ORDER_STATUS_UNSPECIFIED: PaymentOrderStatus
PAYMENT_ORDER_STATUS_PENDING: PaymentOrderStatus
PAYMENT_ORDER_STATUS_PAID: PaymentOrderStatus
PAYMENT_ORDER_STATUS_FAILED: PaymentOrderStatus
PAYMENT_ORDER_STATUS_REFUNDED: PaymentOrderStatus
PAYMENT_ORDER_STATUS_CANCELED: PaymentOrderStatus
PAYMENT_ORDER_STATUS_EXPIRED: PaymentOrderStatus
PAYMENT_BILLING_INTERVAL_UNSPECIFIED: PaymentBillingInterval
PAYMENT_BILLING_INTERVAL_ONE_TIME: PaymentBillingInterval
PAYMENT_BILLING_INTERVAL_MONTHLY: PaymentBillingInterval
PAYMENT_BILLING_INTERVAL_QUARTERLY: PaymentBillingInterval
PAYMENT_BILLING_INTERVAL_YEARLY: PaymentBillingInterval
PAYMENT_EVENT_TYPE_UNSPECIFIED: PaymentEventType
PAYMENT_EVENT_TYPE_CHECKOUT_COMPLETED: PaymentEventType
PAYMENT_EVENT_TYPE_PAYMENT_SUCCEEDED: PaymentEventType
PAYMENT_EVENT_TYPE_PAYMENT_FAILED: PaymentEventType
PAYMENT_EVENT_TYPE_SUBSCRIPTION_CREATED: PaymentEventType
PAYMENT_EVENT_TYPE_SUBSCRIPTION_RENEWED: PaymentEventType
PAYMENT_EVENT_TYPE_SUBSCRIPTION_CANCELED: PaymentEventType
PAYMENT_EVENT_TYPE_REFUND_CREATED: PaymentEventType
PAYMENT_EVENT_TYPE_CHARGE_DISPUTED: PaymentEventType
REFUND_REQUEST_STATUS_UNSPECIFIED: RefundRequestStatus
REFUND_REQUEST_STATUS_PENDING_APPROVAL: RefundRequestStatus
REFUND_REQUEST_STATUS_APPROVED: RefundRequestStatus
REFUND_REQUEST_STATUS_REJECTED: RefundRequestStatus
REFUND_REQUEST_STATUS_CANCELED: RefundRequestStatus
REFUND_REQUEST_STATUS_PROCESSING: RefundRequestStatus
REFUND_REQUEST_STATUS_SUCCEEDED: RefundRequestStatus
REFUND_REQUEST_STATUS_FAILED: RefundRequestStatus

class CheckoutLineItem(_message.Message):
    __slots__ = ("name", "description", "amount_minor", "quantity", "external_product_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    amount_minor: int
    quantity: int
    external_product_id: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., amount_minor: _Optional[int] = ..., quantity: _Optional[int] = ..., external_product_id: _Optional[str] = ...) -> None: ...

class CreateCheckoutRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "provider", "customer_email", "currency", "line_items", "billing_interval", "success_url", "cancel_url", "metadata", "idempotency_key")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    LINE_ITEMS_FIELD_NUMBER: _ClassVar[int]
    BILLING_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_URL_FIELD_NUMBER: _ClassVar[int]
    CANCEL_URL_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    provider: PaymentProviderKind
    customer_email: str
    currency: str
    line_items: _containers.RepeatedCompositeFieldContainer[CheckoutLineItem]
    billing_interval: PaymentBillingInterval
    success_url: str
    cancel_url: str
    metadata: _containers.ScalarMap[str, str]
    idempotency_key: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., provider: _Optional[_Union[PaymentProviderKind, str]] = ..., customer_email: _Optional[str] = ..., currency: _Optional[str] = ..., line_items: _Optional[_Iterable[_Union[CheckoutLineItem, _Mapping]]] = ..., billing_interval: _Optional[_Union[PaymentBillingInterval, str]] = ..., success_url: _Optional[str] = ..., cancel_url: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class CreateCheckoutResponse(_message.Message):
    __slots__ = ("order_id", "provider_session_id", "checkout_url", "provider")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    CHECKOUT_URL_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    provider_session_id: str
    checkout_url: str
    provider: PaymentProviderKind
    def __init__(self, order_id: _Optional[str] = ..., provider_session_id: _Optional[str] = ..., checkout_url: _Optional[str] = ..., provider: _Optional[_Union[PaymentProviderKind, str]] = ...) -> None: ...

class GetPaymentOrderRequest(_message.Message):
    __slots__ = ("order_id",)
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    def __init__(self, order_id: _Optional[str] = ...) -> None: ...

class PaymentOrderResponse(_message.Message):
    __slots__ = ("id", "business_id", "subject_id", "provider", "provider_session_id", "status", "currency", "total_amount_minor", "billing_interval", "metadata", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    BILLING_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    business_id: str
    subject_id: str
    provider: PaymentProviderKind
    provider_session_id: str
    status: PaymentOrderStatus
    currency: str
    total_amount_minor: int
    billing_interval: str
    metadata: _struct_pb2.Struct
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., provider: _Optional[_Union[PaymentProviderKind, str]] = ..., provider_session_id: _Optional[str] = ..., status: _Optional[_Union[PaymentOrderStatus, str]] = ..., currency: _Optional[str] = ..., total_amount_minor: _Optional[int] = ..., billing_interval: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class ListPaymentOrdersRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "status", "page_size", "page_token")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    status: PaymentOrderStatus
    page_size: int
    page_token: str
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., status: _Optional[_Union[PaymentOrderStatus, str]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListPaymentOrdersResponse(_message.Message):
    __slots__ = ("orders", "next_page_token")
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    orders: _containers.RepeatedCompositeFieldContainer[PaymentOrderResponse]
    next_page_token: str
    def __init__(self, orders: _Optional[_Iterable[_Union[PaymentOrderResponse, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class RefundPaymentRequest(_message.Message):
    __slots__ = ("order_id", "amount_minor", "reason", "idempotency_key")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    amount_minor: int
    reason: str
    idempotency_key: str
    def __init__(self, order_id: _Optional[str] = ..., amount_minor: _Optional[int] = ..., reason: _Optional[str] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class RefundPaymentResponse(_message.Message):
    __slots__ = ("refund_id", "provider_refund_id", "amount_minor", "status")
    REFUND_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_REFUND_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    refund_id: str
    provider_refund_id: str
    amount_minor: int
    status: str
    def __init__(self, refund_id: _Optional[str] = ..., provider_refund_id: _Optional[str] = ..., amount_minor: _Optional[int] = ..., status: _Optional[str] = ...) -> None: ...

class SubmitRefundRequestRequest(_message.Message):
    __slots__ = ("order_id", "amount_minor", "reason", "request_channel", "requested_by", "requested_by_display_name", "metadata", "idempotency_key")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_BY_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_BY_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    amount_minor: int
    reason: str
    request_channel: str
    requested_by: str
    requested_by_display_name: str
    metadata: _containers.ScalarMap[str, str]
    idempotency_key: str
    def __init__(self, order_id: _Optional[str] = ..., amount_minor: _Optional[int] = ..., reason: _Optional[str] = ..., request_channel: _Optional[str] = ..., requested_by: _Optional[str] = ..., requested_by_display_name: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class GetRefundRequestRequest(_message.Message):
    __slots__ = ("refund_request_id",)
    REFUND_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    refund_request_id: str
    def __init__(self, refund_request_id: _Optional[str] = ...) -> None: ...

class ListRefundRequestsRequest(_message.Message):
    __slots__ = ("business_id", "subject_id", "order_id", "status", "page_size", "page_token", "business_ids", "subject_ids", "order_ids", "statuses")
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_IDS_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_IDS_FIELD_NUMBER: _ClassVar[int]
    ORDER_IDS_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    business_id: str
    subject_id: str
    order_id: str
    status: RefundRequestStatus
    page_size: int
    page_token: str
    business_ids: _containers.RepeatedScalarFieldContainer[str]
    subject_ids: _containers.RepeatedScalarFieldContainer[str]
    order_ids: _containers.RepeatedScalarFieldContainer[str]
    statuses: _containers.RepeatedScalarFieldContainer[RefundRequestStatus]
    def __init__(self, business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., order_id: _Optional[str] = ..., status: _Optional[_Union[RefundRequestStatus, str]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., business_ids: _Optional[_Iterable[str]] = ..., subject_ids: _Optional[_Iterable[str]] = ..., order_ids: _Optional[_Iterable[str]] = ..., statuses: _Optional[_Iterable[_Union[RefundRequestStatus, str]]] = ...) -> None: ...

class RefundReviewLogRecord(_message.Message):
    __slots__ = ("id", "refund_request_id", "action", "actor_id", "actor_display_name", "comment", "from_status", "to_status", "metadata", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    REFUND_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ACTOR_ID_FIELD_NUMBER: _ClassVar[int]
    ACTOR_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    FROM_STATUS_FIELD_NUMBER: _ClassVar[int]
    TO_STATUS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    refund_request_id: str
    action: str
    actor_id: str
    actor_display_name: str
    comment: str
    from_status: str
    to_status: str
    metadata: _struct_pb2.Struct
    created_at: str
    def __init__(self, id: _Optional[str] = ..., refund_request_id: _Optional[str] = ..., action: _Optional[str] = ..., actor_id: _Optional[str] = ..., actor_display_name: _Optional[str] = ..., comment: _Optional[str] = ..., from_status: _Optional[str] = ..., to_status: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., created_at: _Optional[str] = ...) -> None: ...

class ListRefundReviewLogsRequest(_message.Message):
    __slots__ = ("refund_request_id",)
    REFUND_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    refund_request_id: str
    def __init__(self, refund_request_id: _Optional[str] = ...) -> None: ...

class ListRefundReviewLogsResponse(_message.Message):
    __slots__ = ("review_logs",)
    REVIEW_LOGS_FIELD_NUMBER: _ClassVar[int]
    review_logs: _containers.RepeatedCompositeFieldContainer[RefundReviewLogRecord]
    def __init__(self, review_logs: _Optional[_Iterable[_Union[RefundReviewLogRecord, _Mapping]]] = ...) -> None: ...

class RefundRequestRecord(_message.Message):
    __slots__ = ("id", "order_id", "business_id", "subject_id", "status", "requested_amount_minor", "approved_amount_minor", "currency", "reason", "request_channel", "requested_by", "requested_by_display_name", "reviewer_id", "reviewer_display_name", "review_comment", "provider_refund_id", "payment_refund_id", "error_message", "metadata", "created_at", "updated_at", "reviewed_at", "processed_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    APPROVED_AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_BY_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_BY_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    REVIEWER_ID_FIELD_NUMBER: _ClassVar[int]
    REVIEWER_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    REVIEW_COMMENT_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_REFUND_ID_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_REFUND_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    REVIEWED_AT_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    order_id: str
    business_id: str
    subject_id: str
    status: RefundRequestStatus
    requested_amount_minor: int
    approved_amount_minor: int
    currency: str
    reason: str
    request_channel: str
    requested_by: str
    requested_by_display_name: str
    reviewer_id: str
    reviewer_display_name: str
    review_comment: str
    provider_refund_id: str
    payment_refund_id: str
    error_message: str
    metadata: _struct_pb2.Struct
    created_at: str
    updated_at: str
    reviewed_at: str
    processed_at: str
    def __init__(self, id: _Optional[str] = ..., order_id: _Optional[str] = ..., business_id: _Optional[str] = ..., subject_id: _Optional[str] = ..., status: _Optional[_Union[RefundRequestStatus, str]] = ..., requested_amount_minor: _Optional[int] = ..., approved_amount_minor: _Optional[int] = ..., currency: _Optional[str] = ..., reason: _Optional[str] = ..., request_channel: _Optional[str] = ..., requested_by: _Optional[str] = ..., requested_by_display_name: _Optional[str] = ..., reviewer_id: _Optional[str] = ..., reviewer_display_name: _Optional[str] = ..., review_comment: _Optional[str] = ..., provider_refund_id: _Optional[str] = ..., payment_refund_id: _Optional[str] = ..., error_message: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., reviewed_at: _Optional[str] = ..., processed_at: _Optional[str] = ...) -> None: ...

class ListRefundRequestsResponse(_message.Message):
    __slots__ = ("refund_requests", "next_page_token")
    REFUND_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    refund_requests: _containers.RepeatedCompositeFieldContainer[RefundRequestRecord]
    next_page_token: str
    def __init__(self, refund_requests: _Optional[_Iterable[_Union[RefundRequestRecord, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class CancelRefundRequestRequest(_message.Message):
    __slots__ = ("refund_request_id", "canceled_by", "cancel_comment")
    REFUND_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CANCELED_BY_FIELD_NUMBER: _ClassVar[int]
    CANCEL_COMMENT_FIELD_NUMBER: _ClassVar[int]
    refund_request_id: str
    canceled_by: str
    cancel_comment: str
    def __init__(self, refund_request_id: _Optional[str] = ..., canceled_by: _Optional[str] = ..., cancel_comment: _Optional[str] = ...) -> None: ...

class ApproveRefundRequestRequest(_message.Message):
    __slots__ = ("refund_request_id", "approved_amount_minor", "reviewer_id", "reviewer_display_name", "review_comment")
    REFUND_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    APPROVED_AMOUNT_MINOR_FIELD_NUMBER: _ClassVar[int]
    REVIEWER_ID_FIELD_NUMBER: _ClassVar[int]
    REVIEWER_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    REVIEW_COMMENT_FIELD_NUMBER: _ClassVar[int]
    refund_request_id: str
    approved_amount_minor: int
    reviewer_id: str
    reviewer_display_name: str
    review_comment: str
    def __init__(self, refund_request_id: _Optional[str] = ..., approved_amount_minor: _Optional[int] = ..., reviewer_id: _Optional[str] = ..., reviewer_display_name: _Optional[str] = ..., review_comment: _Optional[str] = ...) -> None: ...

class RejectRefundRequestRequest(_message.Message):
    __slots__ = ("refund_request_id", "reviewer_id", "reviewer_display_name", "review_comment")
    REFUND_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REVIEWER_ID_FIELD_NUMBER: _ClassVar[int]
    REVIEWER_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    REVIEW_COMMENT_FIELD_NUMBER: _ClassVar[int]
    refund_request_id: str
    reviewer_id: str
    reviewer_display_name: str
    review_comment: str
    def __init__(self, refund_request_id: _Optional[str] = ..., reviewer_id: _Optional[str] = ..., reviewer_display_name: _Optional[str] = ..., review_comment: _Optional[str] = ...) -> None: ...

class PaymentWebhookRequest(_message.Message):
    __slots__ = ("provider", "raw_body", "signature")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    RAW_BODY_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    provider: PaymentProviderKind
    raw_body: bytes
    signature: str
    def __init__(self, provider: _Optional[_Union[PaymentProviderKind, str]] = ..., raw_body: _Optional[bytes] = ..., signature: _Optional[str] = ...) -> None: ...

class PaymentWebhookResponse(_message.Message):
    __slots__ = ("accepted", "event_type", "provider_event_id", "order_id")
    ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    accepted: bool
    event_type: str
    provider_event_id: str
    order_id: str
    def __init__(self, accepted: bool = ..., event_type: _Optional[str] = ..., provider_event_id: _Optional[str] = ..., order_id: _Optional[str] = ...) -> None: ...

class ListPaymentProvidersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListPaymentProvidersResponse(_message.Message):
    __slots__ = ("providers",)
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    providers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, providers: _Optional[_Iterable[str]] = ...) -> None: ...

import asyncio

from stew import PaymentClient, PaymentError, SyncPaymentClient
from stew.api.v1 import payment_model as payment_model
from stew.api.v1 import payment_pb2 as payment_pb2


def test_payment_client_is_exported() -> None:
    assert PaymentClient is not None
    assert SyncPaymentClient is not None
    assert PaymentError is not None


def test_create_checkout_separates_scope_business_id_from_header_business_id() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def CreateCheckout(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            assert timeout == 30.0
            return payment_pb2.CreateCheckoutResponse(
                order_id="order-1",
                checkout_url="https://pay.example/checkout/1",
            )

    client = PaymentClient(
        "127.0.0.1:3012",
        app_secret="ak_pay",
        default_metadata=[("x-sdk-source", "python")],
    )
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.create_checkout(
            scope_business_id="ledger-biz",
            subject_id="subject-1",
            currency="USD",
            line_items=[
                payment_model.CheckoutLineItem(
                    name="Plan",
                    amount_minor=9900,
                    quantity=1,
                )
            ],
            business_id="header-biz",
            extra_metadata=[("x-request-id", "req-1")],
        )
    )

    request = captured["request"]
    assert request.business_id == "ledger-biz"
    assert request.subject_id == "subject-1"
    assert len(request.line_items) == 1
    assert request.line_items[0].name == "Plan"
    assert captured["metadata"] == [
        ("x-api-key", "ak_pay"),
        ("x-sdk-source", "python"),
        ("x-business-id", "header-biz"),
        ("x-request-id", "req-1"),
    ]
    assert isinstance(result, payment_model.CreateCheckoutResponse)
    assert result.order_id == "order-1"


def test_payment_operator_review_methods_are_not_sdk_surface() -> None:
    client = PaymentClient("127.0.0.1:3012", app_secret="ak_pay")
    sync_client = SyncPaymentClient("127.0.0.1:3012", app_secret="ak_pay")

    for name in ["refund_payment", "approve_refund_request", "reject_refund_request"]:
        assert not hasattr(client, name)
        assert not hasattr(sync_client, name)

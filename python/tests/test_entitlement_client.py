import asyncio

from stew import EntitlementClient, EntitlementError, SyncEntitlementClient
from stew.api.v1 import entitlement_model as ent_model
from stew.api.v1 import entitlement_pb2 as ent_pb


def test_entitlement_client_is_exported() -> None:
    assert EntitlementClient is not None
    assert SyncEntitlementClient is not None
    assert EntitlementError is not None


def test_get_my_entitlement_separates_scope_business_id_from_header_business_id() -> (
    None
):
    captured: dict[str, object] = {}

    class Stub:
        async def GetMyEntitlement(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            return ent_pb.ResolvedEntitlementResponse(
                subscription=ent_pb.Subscription(
                    business_id=request.business_id,
                    subject_id=request.subject_id,
                    plan_id="pro",
                )
            )

    client = EntitlementClient("127.0.0.1:3012", app_secret="ak_ent")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.get_my_entitlement(
            scope_business_id="biz-scope",
            subject_id="subject-1",
            business_id="biz-header",
        )
    )

    assert captured["request"].business_id == "biz-scope"
    assert captured["metadata"] == [
        ("x-api-key", "ak_ent"),
        ("x-business-id", "biz-header"),
    ]
    assert isinstance(result, ent_model.ResolvedEntitlementResponse)
    assert result.subscription is not None
    assert result.subscription.plan_id == "pro"


def test_entitlement_management_methods_are_not_sdk_surface() -> None:
    client = EntitlementClient("127.0.0.1:3012", app_secret="ak_ent")
    sync_client = SyncEntitlementClient("127.0.0.1:3012", app_secret="ak_ent")

    for name in [
        "create_plan",
        "get_plan",
        "list_plans",
        "update_plan",
        "delete_plan",
        "upsert_plan_feature",
        "delete_plan_feature",
        "upsert_plan_quota",
        "delete_plan_quota",
        "create_subscription",
        "get_subscription",
        "get_subscription_by_subject",
        "update_subscription",
        "cancel_subscription",
        "delete_subscription",
        "restore_subscription",
        "list_subscriptions",
        "admin_renew_subscriptions",
        "internal_renew_subscriptions",
        "change_plan",
        "list_plan_changes",
        "cancel_plan_change",
    ]:
        assert not hasattr(client, name)
        assert not hasattr(sync_client, name)

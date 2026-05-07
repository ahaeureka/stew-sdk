import asyncio

from stew import EntitlementClient, EntitlementError, SyncEntitlementClient
from stew.api.v1 import entitlement_model as ent_model
from stew.api.v1 import entitlement_pb2 as ent_pb


def test_entitlement_client_is_exported() -> None:
    assert EntitlementClient is not None
    assert SyncEntitlementClient is not None
    assert EntitlementError is not None


def test_create_plan_supports_nested_feature_and_quota() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def CreatePlan(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            assert timeout == 30.0
            return ent_pb.EntitlementPlan(
                business_id=request.business_id,
                name=request.name,
                features=request.features,
                quotas=request.quotas,
            )

    client = EntitlementClient("127.0.0.1:3012", app_secret="ak_ent")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.create_plan(
            scope_business_id="biz-scope",
            name="Pro",
            features=[ent_model.PlanFeature(feature_key="feature.a", enabled=True)],
            quotas=[ent_model.PlanQuota(quota_key="credits.monthly", quota_limit=1000)],
            business_id="biz-header",
            extra_metadata=[("x-request-id", "req-1")],
        )
    )

    request = captured["request"]
    assert request.business_id == "biz-scope"
    assert request.features[0].feature_key == "feature.a"
    assert request.quotas[0].quota_key == "credits.monthly"
    assert captured["metadata"] == [
        ("x-api-key", "ak_ent"),
        ("x-business-id", "biz-header"),
        ("x-request-id", "req-1"),
    ]
    assert isinstance(result, ent_model.EntitlementPlan)
    assert result.name == "Pro"


def test_get_my_entitlement_separates_scope_business_id_from_header_business_id() -> None:
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


def test_change_plan_returns_change_record() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def ChangePlan(self, request, metadata, timeout):
            captured["request"] = request
            captured["metadata"] = list(metadata)
            return ent_pb.ChangePlanResponse(
                subscription=ent_pb.Subscription(
                    id=request.subscription_id,
                    business_id=request.business_id,
                    plan_id=request.new_plan_id,
                ),
                change_record=ent_pb.PlanChangeRecord(
                    subscription_id=request.subscription_id,
                    new_plan_id=request.new_plan_id,
                ),
            )

    client = EntitlementClient("127.0.0.1:3012", app_secret="ak_ent")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.change_plan(
            scope_business_id="biz-scope",
            subscription_id="sub-1",
            subject_id="subject-1",
            new_plan_id="enterprise",
            change_mode="immediate",
        )
    )

    assert captured["request"].subscription_id == "sub-1"
    assert captured["request"].new_plan_id == "enterprise"
    assert captured["metadata"] == [("x-api-key", "ak_ent")]
    assert isinstance(result, ent_model.ChangePlanResponse)
    assert result.change_record is not None
    assert result.change_record.new_plan_id == "enterprise"
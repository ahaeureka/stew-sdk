import asyncio

from stew.billing_internal_client import BillingInternalClient
from stew.api.v1 import billing_common_model as billing_model


async def main() -> None:
    usage_totals = billing_model.BillingUsageTotals()
    setattr(
        usage_totals,
        "meters",
        {"feature_units": 120, "processing_units": 80, "overhead_units": 1},
    )

    cost_breakdown = billing_model.BillingCostBreakdown(total_cost_micros=20100)
    setattr(
        cost_breakdown,
        "line_items",
        {"feature_units": 12000, "processing_units": 8000, "overhead_units": 100},
    )

    async with BillingInternalClient(
        "127.0.0.1:3012",
        app_secret="ak_worker",
        business_id="example-business",
    ) as billing_internal:
        result = await billing_internal.submit_billing_report(
            report=billing_model.BillingReport(
                business_id="example-business",
                authorization_id="auth_123",
                request_id="req_123",
                user_id="user_123",
                usage_source=billing_model.BillingUsageSource.BILLING_USAGE_SOURCE_ACTUAL,
                final_status=billing_model.BillingFinalStatus.BILLING_FINAL_STATUS_SUCCESS,
                dedupe_key="job-42",
                raw_usage_totals=usage_totals,
                cost_breakdown=cost_breakdown,
            ),
            delivery_request_id="worker-attempt-1",
            source_service="your.service.v1.AsyncWorker",
            labels={"attempt": "1"},
            extra_metadata=[("x-request-id", "req_123")],
        )

        print("deduped:", result.deduped)
        print("settled points:", result.decision.points if result.decision else 0)


if __name__ == "__main__":
    asyncio.run(main())

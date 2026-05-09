import asyncio

from stew import BillingClient
from stew.api.v1 import billing_model


async def main() -> None:
    async with BillingClient(
        "127.0.0.1:3012",
        app_secret="ak_worker",
        business_id="skillforge",
    ) as billing:
        reservation = await billing.get_reservation(
            scope_business_id="skillforge",
            authorization_id="auth_123",
        )

        if reservation.status != billing_model.BillingReservationStatus.BILLING_RESERVATION_STATUS_AWAITING_REPORT:
            print("reservation is not awaiting report")
            return

        result = await billing.submit_billing_report(
            report=billing_model.BillingReport(
                business_id="skillforge",
                authorization_id="auth_123",
                request_id="req_123",
                user_id="user_123",
                usage_source=billing_model.BillingUsageSource.BILLING_USAGE_SOURCE_ACTUAL,
                final_status=billing_model.BillingFinalStatus.BILLING_FINAL_STATUS_SUCCESS,
                billed_points_candidate=42,
                dedupe_key="job-42",
            ),
            delivery_request_id="worker-attempt-1",
            source_service="stew.api.v1.ExtractionWorker",
            labels={"job_id": "job-42"},
            extra_metadata=[("x-request-id", "req_123")],
        )

        print("deduped:", result.deduped)
        print("settled points:", result.decision.points if result.decision else 0)


if __name__ == "__main__":
    asyncio.run(main())
import asyncio

from stew import BillingAdminClient, BillingReservationTroubleshooter
from stew.api.v1 import billing_common_model as billing_model


async def main() -> None:
    async with BillingAdminClient(
        "127.0.0.1:3012",
        app_secret="ak_worker",
        business_id="example-business",
    ) as billing_admin:
        troubleshooter = BillingReservationTroubleshooter(billing_admin)

        page = await troubleshooter.query_records(
            scope_business_id="example-business",
            request_id="req_123",
            status=billing_model.BillingReservationStatus.BILLING_RESERVATION_STATUS_AWAITING_REPORT,
            page_size=50,
        )

        for item in page.items:
            print(item.model_dump(mode="json"))

        record = await troubleshooter.get_record(
            scope_business_id="example-business",
            authorization_id="auth_123",
        )
        print(record.model_dump(mode="json"))


if __name__ == "__main__":
    asyncio.run(main())

"""Compatibility billing facade backed by split billing service clients."""

from __future__ import annotations

from typing import Any

from ._billing_client_shared import BillingError, _bill_model
from .billing_internal_client import BillingInternalClient, SyncBillingInternalClient
from .billing_public_client import BillingPublicClient, SyncBillingPublicClient
from ._discovery.helpers import SyncGatewayClientBase


class BillingClient:
    """Backward-compatible async billing client.

    This facade preserves the historical SDK entry point while routing calls to
    the split public and internal billing services.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._public_client = BillingPublicClient(*args, **kwargs)
        self._internal_client = BillingInternalClient(*args, **kwargs)

    @property
    def public(self) -> BillingPublicClient:
        return self._public_client

    @property
    def internal(self) -> BillingInternalClient:
        return self._internal_client

    async def connect(self) -> None:
        await self._public_client.connect()
        try:
            await self._internal_client.connect()
        except Exception:
            await self._public_client.close()
            raise

    async def close(self) -> None:
        await self._internal_client.close()
        await self._public_client.close()

    async def __aenter__(self) -> BillingClient:
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: Any,
    ) -> None:
        await self.close()

    async def estimate_charge(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.EstimateChargeResponse:
        return await self._internal_client.estimate_charge(*args, **kwargs)

    async def authorize(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.BillingAuthorizationResponse:
        return await self._internal_client.authorize(*args, **kwargs)

    async def finalize(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.SettlementDecision:
        return await self._internal_client.finalize(*args, **kwargs)

    async def release(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.SettlementDecision:
        return await self._internal_client.release(*args, **kwargs)

    async def refund(self, *args: Any, **kwargs: Any) -> _bill_model.SettlementDecision:
        return await self._internal_client.refund(*args, **kwargs)

    async def query_balance(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.BalanceSnapshot:
        return await self._public_client.query_balance(*args, **kwargs)

    async def list_grants(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.ListGrantsResponse:
        return await self._public_client.list_grants(*args, **kwargs)

    async def get_transaction(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.BillingTransaction:
        return await self._public_client.get_transaction(*args, **kwargs)

    async def query_transactions(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.QueryTransactionsResponse:
        return await self._public_client.query_transactions(*args, **kwargs)

    async def query_snapshot(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.BillingSettlementSnapshot:
        return await self._public_client.query_snapshot(*args, **kwargs)

    async def submit_billing_report(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.SubmitBillingReportResponse:
        return await self._internal_client.submit_billing_report(*args, **kwargs)


class SyncBillingClient(SyncGatewayClientBase[BillingClient]):
    """Synchronous facade over :class:`BillingClient`."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(BillingClient, *args, **kwargs)

    def estimate_charge(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.EstimateChargeResponse:
        return self._run(self._client.estimate_charge(*args, **kwargs))

    def authorize(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.BillingAuthorizationResponse:
        return self._run(self._client.authorize(*args, **kwargs))

    def finalize(self, *args: Any, **kwargs: Any) -> _bill_model.SettlementDecision:
        return self._run(self._client.finalize(*args, **kwargs))

    def release(self, *args: Any, **kwargs: Any) -> _bill_model.SettlementDecision:
        return self._run(self._client.release(*args, **kwargs))

    def refund(self, *args: Any, **kwargs: Any) -> _bill_model.SettlementDecision:
        return self._run(self._client.refund(*args, **kwargs))

    def query_balance(self, *args: Any, **kwargs: Any) -> _bill_model.BalanceSnapshot:
        return self._run(self._client.query_balance(*args, **kwargs))

    def list_grants(self, *args: Any, **kwargs: Any) -> _bill_model.ListGrantsResponse:
        return self._run(self._client.list_grants(*args, **kwargs))

    def get_transaction(
        self, *args: Any, **kwargs: Any
    ) -> _bill_model.BillingTransaction:
        return self._run(self._client.get_transaction(*args, **kwargs))

    def query_transactions(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.QueryTransactionsResponse:
        return self._run(self._client.query_transactions(*args, **kwargs))

    def query_snapshot(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.BillingSettlementSnapshot:
        return self._run(self._client.query_snapshot(*args, **kwargs))

    def submit_billing_report(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _bill_model.SubmitBillingReportResponse:
        return self._run(self._client.submit_billing_report(*args, **kwargs))


__all__ = ["BillingClient", "BillingError", "SyncBillingClient"]

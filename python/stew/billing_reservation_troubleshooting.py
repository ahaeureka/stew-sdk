"""Shared helpers for reservation troubleshooting surfaces."""

from __future__ import annotations

import datetime
from collections.abc import Sequence
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field as _Field

from ._discovery.helpers import MetadataEntry
from .api.v1 import billing_common_model as _bill_model
from .billing_admin_client import BillingAdminClient, SyncBillingAdminClient


def _enum_name(value: Any, enum_cls: type[Enum]) -> str:
    if value is None:
        return ""
    if isinstance(value, enum_cls):
        return value.name
    if isinstance(value, int):
        try:
            return enum_cls(value).name
        except ValueError:
            return str(value)
    name = getattr(value, "name", None)
    if isinstance(name, str):
        return name
    return str(value)


class BillingReservationTroubleshootingQuery(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    scope_business_id: str = _Field(default="")
    request_id: str = _Field(default="")
    authorization_id: str = _Field(default="")
    subject_id: str = _Field(default="")
    subject_type: _bill_model.BillingSubjectType | int = _Field(
        default=_bill_model.BillingSubjectType(0)
    )
    user_id: str = _Field(default="")
    status: _bill_model.BillingReservationStatus | int = _Field(
        default=_bill_model.BillingReservationStatus(0)
    )
    start_time_epoch_seconds: int = _Field(default=0)
    end_time_epoch_seconds: int = _Field(default=0)
    page_size: int = _Field(default=0)
    page_token: str = _Field(default="")
    business_id: str = _Field(default="")


class BillingReservationTroubleshootingRecord(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    business_id: str = _Field(default="")
    user_id: str = _Field(default="")
    authorization_id: str = _Field(default="")
    request_id: str = _Field(default="")
    subject_id: str = _Field(default="")
    subject_type: str = _Field(default="")
    policy_id: str = _Field(default="")
    status: str = _Field(default="")
    held_points: int = _Field(default=0)
    captured_points: int = _Field(default=0)
    awaiting_report_timeout_action: str = _Field(default="")
    awaiting_report_deadline: datetime.datetime | None = _Field(default=None)
    created_at: datetime.datetime | None = _Field(default=None)

    @classmethod
    def from_reservation(
        cls, reservation: _bill_model.BillingReservation
    ) -> "BillingReservationTroubleshootingRecord":
        return cls(
            business_id=reservation.business_id or "",
            user_id=reservation.user_id or "",
            authorization_id=reservation.authorization_id or "",
            request_id=reservation.request_id or "",
            subject_id=reservation.subject_id or "",
            subject_type=_enum_name(
                reservation.subject_type, _bill_model.BillingSubjectType
            ),
            policy_id=reservation.policy_id or "",
            status=_enum_name(reservation.status, _bill_model.BillingReservationStatus),
            held_points=int(reservation.held_points or 0),
            captured_points=int(reservation.captured_points or 0),
            awaiting_report_timeout_action=(
                reservation.awaiting_report_timeout_action or ""
            ),
            awaiting_report_deadline=reservation.awaiting_report_deadline,
            created_at=reservation.created_at,
        )


class BillingReservationTroubleshootingPage(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    items: list[BillingReservationTroubleshootingRecord] = _Field(default_factory=list)
    next_page_token: str = _Field(default="")

    @classmethod
    def from_query_response(
        cls, response: _bill_model.QueryBillingReservationsResponse
    ) -> "BillingReservationTroubleshootingPage":
        return cls(
            items=[
                BillingReservationTroubleshootingRecord.from_reservation(item)
                for item in response.reservations or []
            ],
            next_page_token=response.next_page_token or "",
        )


class BillingReservationTroubleshooter:
    """Async facade that normalizes reservation troubleshooting payloads."""

    def __init__(self, client: BillingAdminClient) -> None:
        self._client = client

    async def get_record(
        self,
        *,
        scope_business_id: str,
        authorization_id: str,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> BillingReservationTroubleshootingRecord:
        reservation = await self._client.get_reservation(
            scope_business_id=scope_business_id,
            authorization_id=authorization_id,
            business_id=business_id,
            extra_metadata=extra_metadata,
        )
        return BillingReservationTroubleshootingRecord.from_reservation(reservation)

    async def query_records(
        self,
        request: BillingReservationTroubleshootingQuery | None = None,
        *,
        scope_business_id: str = "",
        request_id: str = "",
        authorization_id: str = "",
        subject_id: str = "",
        subject_type: _bill_model.BillingSubjectType
        | int = _bill_model.BillingSubjectType(0),
        user_id: str = "",
        status: _bill_model.BillingReservationStatus
        | int = _bill_model.BillingReservationStatus(0),
        start_time_epoch_seconds: int = 0,
        end_time_epoch_seconds: int = 0,
        page_size: int = 0,
        page_token: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> BillingReservationTroubleshootingPage:
        query = request or BillingReservationTroubleshootingQuery(
            scope_business_id=scope_business_id,
            request_id=request_id,
            authorization_id=authorization_id,
            subject_id=subject_id,
            subject_type=subject_type,
            user_id=user_id,
            status=status,
            start_time_epoch_seconds=start_time_epoch_seconds,
            end_time_epoch_seconds=end_time_epoch_seconds,
            page_size=page_size,
            page_token=page_token,
            business_id=business_id,
        )
        response = await self._client.query_reservations(
            scope_business_id=query.scope_business_id,
            request_id=query.request_id,
            authorization_id=query.authorization_id,
            subject_id=query.subject_id,
            subject_type=query.subject_type,
            user_id=query.user_id,
            status=query.status,
            start_time_epoch_seconds=query.start_time_epoch_seconds,
            end_time_epoch_seconds=query.end_time_epoch_seconds,
            page_size=query.page_size,
            page_token=query.page_token,
            business_id=query.business_id,
            extra_metadata=extra_metadata,
        )
        return BillingReservationTroubleshootingPage.from_query_response(response)


class SyncBillingReservationTroubleshooter:
    """Sync facade that normalizes reservation troubleshooting payloads."""

    def __init__(self, client: SyncBillingAdminClient) -> None:
        self._client = client

    def get_record(
        self,
        *,
        scope_business_id: str,
        authorization_id: str,
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> BillingReservationTroubleshootingRecord:
        reservation = self._client.get_reservation(
            scope_business_id=scope_business_id,
            authorization_id=authorization_id,
            business_id=business_id,
            extra_metadata=extra_metadata,
        )
        return BillingReservationTroubleshootingRecord.from_reservation(reservation)

    def query_records(
        self,
        request: BillingReservationTroubleshootingQuery | None = None,
        *,
        scope_business_id: str = "",
        request_id: str = "",
        authorization_id: str = "",
        subject_id: str = "",
        subject_type: _bill_model.BillingSubjectType
        | int = _bill_model.BillingSubjectType(0),
        user_id: str = "",
        status: _bill_model.BillingReservationStatus
        | int = _bill_model.BillingReservationStatus(0),
        start_time_epoch_seconds: int = 0,
        end_time_epoch_seconds: int = 0,
        page_size: int = 0,
        page_token: str = "",
        business_id: str = "",
        extra_metadata: Sequence[MetadataEntry] = (),
    ) -> BillingReservationTroubleshootingPage:
        query = request or BillingReservationTroubleshootingQuery(
            scope_business_id=scope_business_id,
            request_id=request_id,
            authorization_id=authorization_id,
            subject_id=subject_id,
            subject_type=subject_type,
            user_id=user_id,
            status=status,
            start_time_epoch_seconds=start_time_epoch_seconds,
            end_time_epoch_seconds=end_time_epoch_seconds,
            page_size=page_size,
            page_token=page_token,
            business_id=business_id,
        )
        response = self._client.query_reservations(
            scope_business_id=query.scope_business_id,
            request_id=query.request_id,
            authorization_id=query.authorization_id,
            subject_id=query.subject_id,
            subject_type=query.subject_type,
            user_id=query.user_id,
            status=query.status,
            start_time_epoch_seconds=query.start_time_epoch_seconds,
            end_time_epoch_seconds=query.end_time_epoch_seconds,
            page_size=query.page_size,
            page_token=query.page_token,
            business_id=query.business_id,
            extra_metadata=extra_metadata,
        )
        return BillingReservationTroubleshootingPage.from_query_response(response)


__all__ = [
    "BillingReservationTroubleshooter",
    "BillingReservationTroubleshootingPage",
    "BillingReservationTroubleshootingQuery",
    "BillingReservationTroubleshootingRecord",
    "SyncBillingReservationTroubleshooter",
]

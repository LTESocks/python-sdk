from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.payment_history_record_status import PaymentHistoryRecordStatus
from ..types import UNSET, Unset
from typing import cast
import datetime


T = TypeVar("T", bound="PaymentHistoryRecord")


@_attrs_define
class PaymentHistoryRecord:
    date: datetime.datetime | Unset = UNSET
    status: PaymentHistoryRecordStatus | Unset = UNSET
    port: str | Unset = UNSET
    """ Port number """
    amount: int | Unset = UNSET
    """ Payment amount in cents """
    balance: int | Unset = UNSET
    """ Balance at the time of payment """
    description: str | Unset = UNSET
    """ Payment description """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date: str | Unset = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        port = self.port

        amount = self.amount

        balance = self.balance

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if status is not UNSET:
            field_dict["status"] = status
        if port is not UNSET:
            field_dict["port"] = port
        if amount is not UNSET:
            field_dict["amount"] = amount
        if balance is not UNSET:
            field_dict["balance"] = balance
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _date = d.pop("date", UNSET)
        date: datetime.datetime | Unset
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = datetime.datetime.fromisoformat(_date)

        _status = d.pop("status", UNSET)
        status: PaymentHistoryRecordStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = PaymentHistoryRecordStatus(_status)

        port = d.pop("port", UNSET)

        amount = d.pop("amount", UNSET)

        balance = d.pop("balance", UNSET)

        description = d.pop("description", UNSET)

        payment_history_record = cls(
            date=date,
            status=status,
            port=port,
            amount=amount,
            balance=balance,
            description=description,
        )

        payment_history_record.additional_properties = d
        return payment_history_record

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

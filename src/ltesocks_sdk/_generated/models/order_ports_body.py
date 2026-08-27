from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.plan_tarification import PlanTarification


T = TypeVar("T", bound="OrderPortsBody")


@_attrs_define
class OrderPortsBody:
    plan: str | Unset = UNSET
    """ Plan ID """
    tarification: PlanTarification | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.plan_tarification import PlanTarification

        plan = self.plan

        tarification: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tarification, Unset):
            tarification = self.tarification.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if plan is not UNSET:
            field_dict["plan"] = plan
        if tarification is not UNSET:
            field_dict["tarification"] = tarification

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plan_tarification import PlanTarification

        d = dict(src_dict)
        plan = d.pop("plan", UNSET)

        _tarification = d.pop("tarification", UNSET)
        tarification: PlanTarification | Unset
        if isinstance(_tarification, Unset):
            tarification = UNSET
        else:
            tarification = PlanTarification.from_dict(_tarification)

        order_ports_body = cls(
            plan=plan,
            tarification=tarification,
        )

        order_ports_body.additional_properties = d
        return order_ports_body

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

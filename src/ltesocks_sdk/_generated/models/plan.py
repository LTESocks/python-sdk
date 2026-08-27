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


T = TypeVar("T", bound="Plan")


@_attrs_define
class Plan:
    id: str | Unset = UNSET
    name: str | Unset = UNSET
    available: bool | Unset = UNSET
    available_ports: int | Unset = UNSET
    description: str | Unset = UNSET
    country_code: str | Unset = UNSET
    vpn_access: bool | Unset = UNSET
    tarifications: list[PlanTarification] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.plan_tarification import PlanTarification

        id = self.id

        name = self.name

        available = self.available

        available_ports = self.available_ports

        description = self.description

        country_code = self.country_code

        vpn_access = self.vpn_access

        tarifications: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tarifications, Unset):
            tarifications = []
            for tarifications_item_data in self.tarifications:
                tarifications_item = tarifications_item_data.to_dict()
                tarifications.append(tarifications_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if available is not UNSET:
            field_dict["available"] = available
        if available_ports is not UNSET:
            field_dict["availablePorts"] = available_ports
        if description is not UNSET:
            field_dict["description"] = description
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if vpn_access is not UNSET:
            field_dict["vpnAccess"] = vpn_access
        if tarifications is not UNSET:
            field_dict["tarifications"] = tarifications

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plan_tarification import PlanTarification

        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        available = d.pop("available", UNSET)

        available_ports = d.pop("availablePorts", UNSET)

        description = d.pop("description", UNSET)

        country_code = d.pop("countryCode", UNSET)

        vpn_access = d.pop("vpnAccess", UNSET)

        _tarifications = d.pop("tarifications", UNSET)
        tarifications: list[PlanTarification] | Unset = UNSET
        if _tarifications is not UNSET:
            tarifications = []
            for tarifications_item_data in _tarifications:
                tarifications_item = PlanTarification.from_dict(tarifications_item_data)

                tarifications.append(tarifications_item)

        plan = cls(
            id=id,
            name=name,
            available=available,
            available_ports=available_ports,
            description=description,
            country_code=country_code,
            vpn_access=vpn_access,
            tarifications=tarifications,
        )

        plan.additional_properties = d
        return plan

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

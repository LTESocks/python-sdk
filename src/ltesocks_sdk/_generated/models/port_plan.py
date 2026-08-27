from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.plan_tarification import PlanTarification


T = TypeVar("T", bound="PortPlan")


@_attrs_define
class PortPlan:
    id: str | Unset = UNSET
    """ Plan ID """
    name: str | Unset = UNSET
    """ Plan title """
    country_code: str | Unset = UNSET
    """ Plan country code """
    enabled: bool | Unset = UNSET
    """ Indicates whether plan is active """
    auto_renew: bool | Unset = UNSET
    """ Indicates whether plan auto renewal is active """
    activated_at: datetime.datetime | Unset = UNSET
    """ Plan activation time """
    expires_at: datetime.datetime | Unset = UNSET
    """ Plan expiration time """
    traffic_remains: int | Unset = UNSET
    """ Remaining traffic amount in megabytes """
    tarification: PlanTarification | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.plan_tarification import PlanTarification

        id = self.id

        name = self.name

        country_code = self.country_code

        enabled = self.enabled

        auto_renew = self.auto_renew

        activated_at: str | Unset = UNSET
        if not isinstance(self.activated_at, Unset):
            activated_at = self.activated_at.isoformat()

        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        traffic_remains = self.traffic_remains

        tarification: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tarification, Unset):
            tarification = self.tarification.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if auto_renew is not UNSET:
            field_dict["autoRenew"] = auto_renew
        if activated_at is not UNSET:
            field_dict["activatedAt"] = activated_at
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if traffic_remains is not UNSET:
            field_dict["trafficRemains"] = traffic_remains
        if tarification is not UNSET:
            field_dict["tarification"] = tarification

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plan_tarification import PlanTarification

        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        country_code = d.pop("countryCode", UNSET)

        enabled = d.pop("enabled", UNSET)

        auto_renew = d.pop("autoRenew", UNSET)

        _activated_at = d.pop("activatedAt", UNSET)
        activated_at: datetime.datetime | Unset
        if isinstance(_activated_at, Unset):
            activated_at = UNSET
        else:
            activated_at = datetime.datetime.fromisoformat(_activated_at)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = datetime.datetime.fromisoformat(_expires_at)

        traffic_remains = d.pop("trafficRemains", UNSET)

        _tarification = d.pop("tarification", UNSET)
        tarification: PlanTarification | Unset
        if isinstance(_tarification, Unset):
            tarification = UNSET
        else:
            tarification = PlanTarification.from_dict(_tarification)

        port_plan = cls(
            id=id,
            name=name,
            country_code=country_code,
            enabled=enabled,
            auto_renew=auto_renew,
            activated_at=activated_at,
            expires_at=expires_at,
            traffic_remains=traffic_remains,
            tarification=tarification,
        )

        port_plan.additional_properties = d
        return port_plan

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

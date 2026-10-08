from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="ChangeResidentialSubuserTrafficBody")


@_attrs_define
class ChangeResidentialSubuserTrafficBody:
    traffic_bytes: int | Unset = UNSET
    """ Required for add and subtract; omitted for reset. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        traffic_bytes = self.traffic_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if traffic_bytes is not UNSET:
            field_dict["traffic_bytes"] = traffic_bytes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        traffic_bytes = d.pop("traffic_bytes", UNSET)

        change_residential_subuser_traffic_body = cls(
            traffic_bytes=traffic_bytes,
        )

        change_residential_subuser_traffic_body.additional_properties = d
        return change_residential_subuser_traffic_body

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

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="UpdatePortAutoresetBody")


@_attrs_define
class UpdatePortAutoresetBody:
    auto_reset_interval: int | Unset = UNSET
    """ Auto reset interval in seconds, 0 means disabled """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        auto_reset_interval = self.auto_reset_interval

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_reset_interval is not UNSET:
            field_dict["autoResetInterval"] = auto_reset_interval

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        auto_reset_interval = d.pop("autoResetInterval", UNSET)

        update_port_autoreset_body = cls(
            auto_reset_interval=auto_reset_interval,
        )

        update_port_autoreset_body.additional_properties = d
        return update_port_autoreset_body

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

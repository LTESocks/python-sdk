from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID


T = TypeVar("T", bound="ResidentialPackageResponseData")


@_attrs_define
class ResidentialPackageResponseData:
    id: UUID | Unset = UNSET
    package_id: UUID | Unset = UNSET
    traffic_bytes: int | None | Unset = UNSET
    used_bytes: int | None | Unset = UNSET
    remaining_bytes: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: str | Unset = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        package_id: str | Unset = UNSET
        if not isinstance(self.package_id, Unset):
            package_id = str(self.package_id)

        traffic_bytes: int | None | Unset
        if isinstance(self.traffic_bytes, Unset):
            traffic_bytes = UNSET
        else:
            traffic_bytes = self.traffic_bytes

        used_bytes: int | None | Unset
        if isinstance(self.used_bytes, Unset):
            used_bytes = UNSET
        else:
            used_bytes = self.used_bytes

        remaining_bytes = self.remaining_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if package_id is not UNSET:
            field_dict["package_id"] = package_id
        if traffic_bytes is not UNSET:
            field_dict["traffic_bytes"] = traffic_bytes
        if used_bytes is not UNSET:
            field_dict["used_bytes"] = used_bytes
        if remaining_bytes is not UNSET:
            field_dict["remaining_bytes"] = remaining_bytes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: UUID | Unset
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        _package_id = d.pop("package_id", UNSET)
        package_id: UUID | Unset
        if isinstance(_package_id, Unset):
            package_id = UNSET
        else:
            package_id = UUID(_package_id)

        def _parse_traffic_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        traffic_bytes = _parse_traffic_bytes(d.pop("traffic_bytes", UNSET))

        def _parse_used_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        used_bytes = _parse_used_bytes(d.pop("used_bytes", UNSET))

        remaining_bytes = d.pop("remaining_bytes", UNSET)

        residential_package_response_data = cls(
            id=id,
            package_id=package_id,
            traffic_bytes=traffic_bytes,
            used_bytes=used_bytes,
            remaining_bytes=remaining_bytes,
        )

        residential_package_response_data.additional_properties = d
        return residential_package_response_data

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

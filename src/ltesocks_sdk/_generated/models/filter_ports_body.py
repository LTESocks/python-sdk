from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="FilterPortsBody")


@_attrs_define
class FilterPortsBody:
    plan: str | Unset = UNSET
    """ Plan ID (exact) """
    country_code: str | Unset = UNSET
    tags: list[str] | Unset = UNSET
    page: int | Unset = UNSET
    page_size: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan = self.plan

        country_code = self.country_code

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        page = self.page

        page_size = self.page_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if plan is not UNSET:
            field_dict["plan"] = plan
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if tags is not UNSET:
            field_dict["tags"] = tags
        if page is not UNSET:
            field_dict["page"] = page
        if page_size is not UNSET:
            field_dict["pageSize"] = page_size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plan = d.pop("plan", UNSET)

        country_code = d.pop("countryCode", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        page = d.pop("page", UNSET)

        page_size = d.pop("pageSize", UNSET)

        filter_ports_body = cls(
            plan=plan,
            country_code=country_code,
            tags=tags,
            page=page,
            page_size=page_size,
        )

        filter_ports_body.additional_properties = d
        return filter_ports_body

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

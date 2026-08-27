from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset


T = TypeVar("T", bound="GeoIP")


@_attrs_define
class GeoIP:
    continent_code: str | Unset = UNSET
    continent_name: str | Unset = UNSET
    country_code_2: str | Unset = UNSET
    country_code_3: str | Unset = UNSET
    state_prov: str | Unset = UNSET
    district: str | Unset = UNSET
    city: str | Unset = UNSET
    zipcode: str | Unset = UNSET
    latitude: str | Unset = UNSET
    longitude: str | Unset = UNSET
    isp: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        continent_code = self.continent_code

        continent_name = self.continent_name

        country_code_2 = self.country_code_2

        country_code_3 = self.country_code_3

        state_prov = self.state_prov

        district = self.district

        city = self.city

        zipcode = self.zipcode

        latitude = self.latitude

        longitude = self.longitude

        isp = self.isp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if continent_code is not UNSET:
            field_dict["continentCode"] = continent_code
        if continent_name is not UNSET:
            field_dict["continentName"] = continent_name
        if country_code_2 is not UNSET:
            field_dict["countryCode2"] = country_code_2
        if country_code_3 is not UNSET:
            field_dict["countryCode3"] = country_code_3
        if state_prov is not UNSET:
            field_dict["stateProv"] = state_prov
        if district is not UNSET:
            field_dict["district"] = district
        if city is not UNSET:
            field_dict["city"] = city
        if zipcode is not UNSET:
            field_dict["zipcode"] = zipcode
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if isp is not UNSET:
            field_dict["isp"] = isp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        continent_code = d.pop("continentCode", UNSET)

        continent_name = d.pop("continentName", UNSET)

        country_code_2 = d.pop("countryCode2", UNSET)

        country_code_3 = d.pop("countryCode3", UNSET)

        state_prov = d.pop("stateProv", UNSET)

        district = d.pop("district", UNSET)

        city = d.pop("city", UNSET)

        zipcode = d.pop("zipcode", UNSET)

        latitude = d.pop("latitude", UNSET)

        longitude = d.pop("longitude", UNSET)

        isp = d.pop("isp", UNSET)

        geo_ip = cls(
            continent_code=continent_code,
            continent_name=continent_name,
            country_code_2=country_code_2,
            country_code_3=country_code_3,
            state_prov=state_prov,
            district=district,
            city=city,
            zipcode=zipcode,
            latitude=latitude,
            longitude=longitude,
            isp=isp,
        )

        geo_ip.additional_properties = d
        return geo_ip

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

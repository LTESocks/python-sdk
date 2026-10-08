from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime


T = TypeVar("T", bound="ResidentialSubuser")


@_attrs_define
class ResidentialSubuser:
    id: UUID
    login: str
    status: str
    package_id: UUID
    remaining_bytes: int
    email: None | str | Unset = UNSET
    first_name: None | str | Unset = UNSET
    last_name: None | str | Unset = UNSET
    traffic_bytes: int | None | Unset = UNSET
    used_bytes: int | None | Unset = UNSET
    allowed_ips: list[str] | Unset = UNSET
    blocked_domains: list[str] | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        login = self.login

        status = self.status

        package_id = str(self.package_id)

        remaining_bytes = self.remaining_bytes

        email: None | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        else:
            email = self.email

        first_name: None | str | Unset
        if isinstance(self.first_name, Unset):
            first_name = UNSET
        else:
            first_name = self.first_name

        last_name: None | str | Unset
        if isinstance(self.last_name, Unset):
            last_name = UNSET
        else:
            last_name = self.last_name

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

        allowed_ips: list[str] | Unset = UNSET
        if not isinstance(self.allowed_ips, Unset):
            allowed_ips = self.allowed_ips

        blocked_domains: list[str] | Unset = UNSET
        if not isinstance(self.blocked_domains, Unset):
            blocked_domains = self.blocked_domains

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "login": login,
                "status": status,
                "package_id": package_id,
                "remaining_bytes": remaining_bytes,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if traffic_bytes is not UNSET:
            field_dict["traffic_bytes"] = traffic_bytes
        if used_bytes is not UNSET:
            field_dict["used_bytes"] = used_bytes
        if allowed_ips is not UNSET:
            field_dict["allowed_ips"] = allowed_ips
        if blocked_domains is not UNSET:
            field_dict["blocked_domains"] = blocked_domains
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        login = d.pop("login")

        status = d.pop("status")

        package_id = UUID(d.pop("package_id"))

        remaining_bytes = d.pop("remaining_bytes")

        def _parse_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_first_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        first_name = _parse_first_name(d.pop("first_name", UNSET))

        def _parse_last_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_name = _parse_last_name(d.pop("last_name", UNSET))

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

        allowed_ips = cast(list[str], d.pop("allowed_ips", UNSET))

        blocked_domains = cast(list[str], d.pop("blocked_domains", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        residential_subuser = cls(
            id=id,
            login=login,
            status=status,
            package_id=package_id,
            remaining_bytes=remaining_bytes,
            email=email,
            first_name=first_name,
            last_name=last_name,
            traffic_bytes=traffic_bytes,
            used_bytes=used_bytes,
            allowed_ips=allowed_ips,
            blocked_domains=blocked_domains,
            created_at=created_at,
        )

        residential_subuser.additional_properties = d
        return residential_subuser

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

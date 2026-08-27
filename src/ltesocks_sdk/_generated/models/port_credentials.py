from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.port_credentials_password_item import PortCredentialsPasswordItem


T = TypeVar("T", bound="PortCredentials")


@_attrs_define
class PortCredentials:
    ip: list[str] | Unset = UNSET
    password: list[PortCredentialsPasswordItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.port_credentials_password_item import PortCredentialsPasswordItem

        ip: list[str] | Unset = UNSET
        if not isinstance(self.ip, Unset):
            ip = self.ip

        password: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.password, Unset):
            password = []
            for password_item_data in self.password:
                password_item = password_item_data.to_dict()
                password.append(password_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ip is not UNSET:
            field_dict["ip"] = ip
        if password is not UNSET:
            field_dict["password"] = password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.port_credentials_password_item import PortCredentialsPasswordItem

        d = dict(src_dict)
        ip = cast(list[str], d.pop("ip", UNSET))

        _password = d.pop("password", UNSET)
        password: list[PortCredentialsPasswordItem] | Unset = UNSET
        if _password is not UNSET:
            password = []
            for password_item_data in _password:
                password_item = PortCredentialsPasswordItem.from_dict(password_item_data)

                password.append(password_item)

        port_credentials = cls(
            ip=ip,
            password=password,
        )

        port_credentials.additional_properties = d
        return port_credentials

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

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.user_preferences_proxy_protocol import UserPreferencesProxyProtocol
from ..types import UNSET, Unset


T = TypeVar("T", bound="UserPreferences")


@_attrs_define
class UserPreferences:
    vpn_server: str | Unset = UNSET
    """ Default server hostname to connect via OpenVPN """
    proxy_server: str | Unset = UNSET
    """ Default server hostname to connect via proxy """
    proxy_protocol: UserPreferencesProxyProtocol | Unset = UNSET
    """ Default proxy protocol """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vpn_server = self.vpn_server

        proxy_server = self.proxy_server

        proxy_protocol: str | Unset = UNSET
        if not isinstance(self.proxy_protocol, Unset):
            proxy_protocol = self.proxy_protocol.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if vpn_server is not UNSET:
            field_dict["vpnServer"] = vpn_server
        if proxy_server is not UNSET:
            field_dict["proxyServer"] = proxy_server
        if proxy_protocol is not UNSET:
            field_dict["proxyProtocol"] = proxy_protocol

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        vpn_server = d.pop("vpnServer", UNSET)

        proxy_server = d.pop("proxyServer", UNSET)

        _proxy_protocol = d.pop("proxyProtocol", UNSET)
        proxy_protocol: UserPreferencesProxyProtocol | Unset
        if isinstance(_proxy_protocol, Unset):
            proxy_protocol = UNSET
        else:
            proxy_protocol = UserPreferencesProxyProtocol(_proxy_protocol)

        user_preferences = cls(
            vpn_server=vpn_server,
            proxy_server=proxy_server,
            proxy_protocol=proxy_protocol,
        )

        user_preferences.additional_properties = d
        return user_preferences

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

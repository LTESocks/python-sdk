from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.list_servers_response_200_proxy_protocols_item import (
    ListServersResponse200ProxyProtocolsItem,
)
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.server import Server


T = TypeVar("T", bound="ListServersResponse200")


@_attrs_define
class ListServersResponse200:
    vpn_servers: list[Server] | Unset = UNSET
    proxy_servers: list[Server] | Unset = UNSET
    proxy_protocols: list[ListServersResponse200ProxyProtocolsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.server import Server

        vpn_servers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.vpn_servers, Unset):
            vpn_servers = []
            for vpn_servers_item_data in self.vpn_servers:
                vpn_servers_item = vpn_servers_item_data.to_dict()
                vpn_servers.append(vpn_servers_item)

        proxy_servers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.proxy_servers, Unset):
            proxy_servers = []
            for proxy_servers_item_data in self.proxy_servers:
                proxy_servers_item = proxy_servers_item_data.to_dict()
                proxy_servers.append(proxy_servers_item)

        proxy_protocols: list[str] | Unset = UNSET
        if not isinstance(self.proxy_protocols, Unset):
            proxy_protocols = []
            for proxy_protocols_item_data in self.proxy_protocols:
                proxy_protocols_item = proxy_protocols_item_data.value
                proxy_protocols.append(proxy_protocols_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if vpn_servers is not UNSET:
            field_dict["vpnServers"] = vpn_servers
        if proxy_servers is not UNSET:
            field_dict["proxyServers"] = proxy_servers
        if proxy_protocols is not UNSET:
            field_dict["proxyProtocols"] = proxy_protocols

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.server import Server

        d = dict(src_dict)
        _vpn_servers = d.pop("vpnServers", UNSET)
        vpn_servers: list[Server] | Unset = UNSET
        if _vpn_servers is not UNSET:
            vpn_servers = []
            for vpn_servers_item_data in _vpn_servers:
                vpn_servers_item = Server.from_dict(vpn_servers_item_data)

                vpn_servers.append(vpn_servers_item)

        _proxy_servers = d.pop("proxyServers", UNSET)
        proxy_servers: list[Server] | Unset = UNSET
        if _proxy_servers is not UNSET:
            proxy_servers = []
            for proxy_servers_item_data in _proxy_servers:
                proxy_servers_item = Server.from_dict(proxy_servers_item_data)

                proxy_servers.append(proxy_servers_item)

        _proxy_protocols = d.pop("proxyProtocols", UNSET)
        proxy_protocols: list[ListServersResponse200ProxyProtocolsItem] | Unset = UNSET
        if _proxy_protocols is not UNSET:
            proxy_protocols = []
            for proxy_protocols_item_data in _proxy_protocols:
                proxy_protocols_item = ListServersResponse200ProxyProtocolsItem(
                    proxy_protocols_item_data
                )

                proxy_protocols.append(proxy_protocols_item)

        list_servers_response_200 = cls(
            vpn_servers=vpn_servers,
            proxy_servers=proxy_servers,
            proxy_protocols=proxy_protocols,
        )

        list_servers_response_200.additional_properties = d
        return list_servers_response_200

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

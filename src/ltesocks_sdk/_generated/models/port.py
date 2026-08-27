from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.port_status import PortStatus
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.geo_ip import GeoIP
    from ..models.port_credentials import PortCredentials
    from ..models.port_plan import PortPlan


T = TypeVar("T", bound="Port")


@_attrs_define
class Port:
    port: str | Unset = UNSET
    """ Port number """
    ip: str | Unset = UNSET
    """ Port current IP address (0.0.0.0 if not available) """
    geoip: GeoIP | Unset = UNSET
    status: PortStatus | Unset = UNSET
    """ Port status """
    reset_token: str | Unset = UNSET
    """ Port reset token """
    signature: str | Unset = UNSET
    """ Port signature """
    vpn_access: bool | Unset = UNSET
    """ Indicates whether port has access to the VPN server """
    auto_reset_interval: int | Unset = UNSET
    """ Port auto reset interval in seconds, 0 means disabled """
    tags: list[str] | Unset = UNSET
    """ Port tags """
    plan: PortPlan | Unset = UNSET
    credentials: PortCredentials | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.geo_ip import GeoIP
        from ..models.port_credentials import PortCredentials
        from ..models.port_plan import PortPlan

        port = self.port

        ip = self.ip

        geoip: dict[str, Any] | Unset = UNSET
        if not isinstance(self.geoip, Unset):
            geoip = self.geoip.to_dict()

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        reset_token = self.reset_token

        signature = self.signature

        vpn_access = self.vpn_access

        auto_reset_interval = self.auto_reset_interval

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        plan: dict[str, Any] | Unset = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.to_dict()

        credentials: dict[str, Any] | Unset = UNSET
        if not isinstance(self.credentials, Unset):
            credentials = self.credentials.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if port is not UNSET:
            field_dict["port"] = port
        if ip is not UNSET:
            field_dict["ip"] = ip
        if geoip is not UNSET:
            field_dict["geoip"] = geoip
        if status is not UNSET:
            field_dict["status"] = status
        if reset_token is not UNSET:
            field_dict["resetToken"] = reset_token
        if signature is not UNSET:
            field_dict["signature"] = signature
        if vpn_access is not UNSET:
            field_dict["vpnAccess"] = vpn_access
        if auto_reset_interval is not UNSET:
            field_dict["autoResetInterval"] = auto_reset_interval
        if tags is not UNSET:
            field_dict["tags"] = tags
        if plan is not UNSET:
            field_dict["plan"] = plan
        if credentials is not UNSET:
            field_dict["credentials"] = credentials

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.geo_ip import GeoIP
        from ..models.port_credentials import PortCredentials
        from ..models.port_plan import PortPlan

        d = dict(src_dict)
        port = d.pop("port", UNSET)

        ip = d.pop("ip", UNSET)

        _geoip = d.pop("geoip", UNSET)
        geoip: GeoIP | Unset
        if isinstance(_geoip, Unset):
            geoip = UNSET
        else:
            geoip = GeoIP.from_dict(_geoip)

        _status = d.pop("status", UNSET)
        status: PortStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = PortStatus(_status)

        reset_token = d.pop("resetToken", UNSET)

        signature = d.pop("signature", UNSET)

        vpn_access = d.pop("vpnAccess", UNSET)

        auto_reset_interval = d.pop("autoResetInterval", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _plan = d.pop("plan", UNSET)
        plan: PortPlan | Unset
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = PortPlan.from_dict(_plan)

        _credentials = d.pop("credentials", UNSET)
        credentials: PortCredentials | Unset
        if isinstance(_credentials, Unset):
            credentials = UNSET
        else:
            credentials = PortCredentials.from_dict(_credentials)

        port = cls(
            port=port,
            ip=ip,
            geoip=geoip,
            status=status,
            reset_token=reset_token,
            signature=signature,
            vpn_access=vpn_access,
            auto_reset_interval=auto_reset_interval,
            tags=tags,
            plan=plan,
            credentials=credentials,
        )

        port.additional_properties = d
        return port

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

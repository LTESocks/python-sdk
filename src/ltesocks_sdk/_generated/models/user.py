from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.user_preferences import UserPreferences


T = TypeVar("T", bound="User")


@_attrs_define
class User:
    login: str | Unset = UNSET
    """ User login """
    email: str | Unset = UNSET
    """ User email address """
    balance: int | Unset = UNSET
    """ User balance in cents (100$ = 10000) """
    ports_count: int | Unset = UNSET
    """ Total ports number """
    ports_limit: int | Unset = UNSET
    """ Maximum allowed ports number """
    discount_percent: int | Unset = UNSET
    """ User discount in percentage """
    preferences: UserPreferences | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_preferences import UserPreferences

        login = self.login

        email = self.email

        balance = self.balance

        ports_count = self.ports_count

        ports_limit = self.ports_limit

        discount_percent = self.discount_percent

        preferences: dict[str, Any] | Unset = UNSET
        if not isinstance(self.preferences, Unset):
            preferences = self.preferences.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if login is not UNSET:
            field_dict["login"] = login
        if email is not UNSET:
            field_dict["email"] = email
        if balance is not UNSET:
            field_dict["balance"] = balance
        if ports_count is not UNSET:
            field_dict["portsCount"] = ports_count
        if ports_limit is not UNSET:
            field_dict["portsLimit"] = ports_limit
        if discount_percent is not UNSET:
            field_dict["discountPercent"] = discount_percent
        if preferences is not UNSET:
            field_dict["preferences"] = preferences

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_preferences import UserPreferences

        d = dict(src_dict)
        login = d.pop("login", UNSET)

        email = d.pop("email", UNSET)

        balance = d.pop("balance", UNSET)

        ports_count = d.pop("portsCount", UNSET)

        ports_limit = d.pop("portsLimit", UNSET)

        discount_percent = d.pop("discountPercent", UNSET)

        _preferences = d.pop("preferences", UNSET)
        preferences: UserPreferences | Unset
        if isinstance(_preferences, Unset):
            preferences = UNSET
        else:
            preferences = UserPreferences.from_dict(_preferences)

        user = cls(
            login=login,
            email=email,
            balance=balance,
            ports_count=ports_count,
            ports_limit=ports_limit,
            discount_percent=discount_percent,
            preferences=preferences,
        )

        user.additional_properties = d
        return user

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

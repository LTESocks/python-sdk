from enum import Enum


class PortStatus(str, Enum):
    @classmethod
    def _missing_(cls, value: object):
        if not isinstance(value, str):
            return None
        member = str.__new__(cls, value)
        member._name_ = f"UNKNOWN_{value}"
        member._value_ = value
        return member

    ACTIVE = "active"
    DISCONNECTED = "disconnected"
    OUTOFTRAFFIC = "outoftraffic"
    RESET = "reset"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)

"""Official Python SDK for LTESocks."""

from importlib.metadata import PackageNotFoundError, version

from ._generated.types import UNSET, Unset
from .client import DEFAULT_BASE_URL, AsyncClient, Client
from .errors import (
    ApiError,
    ErrorKind,
    InvalidSignatureError,
    LTESocksError,
    PaginationError,
)
from .files import FileDownload
from .response import ApiResponse
from .webhooks import WebhookVerifier

try:
    __version__ = version("ltesocks-sdk")
except PackageNotFoundError:  # pragma: no cover - source tree without an installed package
    __version__ = "0.0.0"

__all__ = [
    "DEFAULT_BASE_URL",
    "UNSET",
    "ApiError",
    "ApiResponse",
    "AsyncClient",
    "Client",
    "ErrorKind",
    "FileDownload",
    "InvalidSignatureError",
    "LTESocksError",
    "PaginationError",
    "Unset",
    "WebhookVerifier",
    "__version__",
]

from __future__ import annotations

import json
from collections.abc import Mapping
from enum import StrEnum
from typing import Any


class ErrorKind(StrEnum):
    """Stable categories for HTTP, transport, and decoding failures."""

    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    PERMISSION = "permission"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    PRECONDITION = "precondition"
    RATE_LIMIT = "rate_limit"
    SERVER = "server"
    NETWORK = "network"
    UNEXPECTED = "unexpected"


class LTESocksError(Exception):
    """Base exception for the SDK."""


class ApiError(LTESocksError):
    """A normalized LTESocks API or transport failure."""

    def __init__(
        self,
        message: str,
        *,
        kind: ErrorKind,
        status_code: int | None = None,
        detail: str | None = None,
        field_errors: Mapping[str, list[str]] | None = None,
        request_id: str | None = None,
        retry_after: float | None = None,
        retry_at: str | None = None,
        content_language: str | None = None,
        current_etag: str | None = None,
        idempotency_key: str | None = None,
        headers: Mapping[str, str] | None = None,
        raw_body: bytes = b"",
        cause: BaseException | None = None,
    ) -> None:
        super().__init__(message)
        self.kind = kind
        self.status_code = status_code
        self.detail = detail
        self.field_errors = dict(field_errors or {})
        self.request_id = request_id
        self.retry_after = retry_after
        self.retry_at = retry_at
        self.content_language = content_language
        self.current_etag = current_etag
        self.idempotency_key = idempotency_key
        self.headers = dict(headers or {})
        self.raw_body = raw_body
        self.__cause__ = cause

    @classmethod
    def from_response(
        cls,
        status_code: int,
        content: bytes,
        headers: Mapping[str, str],
    ) -> ApiError:
        normalized_headers = {str(key): str(value) for key, value in headers.items()}
        payload = _json_payload(content)
        detail = _detail(payload)
        kind = _kind_for_status(status_code)
        request_id = _header(normalized_headers, "x-request-id", "x-correlation-id")
        retry_after = _float_header(normalized_headers, "retry-after")
        retry_at = _header(normalized_headers, "retry-at")
        language = _header(normalized_headers, "content-language")
        current_etag = _header(normalized_headers, "etag")
        message = detail or f"LTESocks API returned HTTP {status_code}."
        return cls(
            message,
            kind=kind,
            status_code=status_code,
            detail=detail,
            field_errors=_field_errors(payload),
            request_id=request_id,
            retry_after=retry_after,
            retry_at=retry_at,
            content_language=language,
            current_etag=current_etag,
            headers=normalized_headers,
            raw_body=content,
        )

    @classmethod
    def network(cls, cause: BaseException) -> ApiError:
        return cls(
            f"LTESocks network request failed: {cause}",
            kind=ErrorKind.NETWORK,
            cause=cause,
        )

    @classmethod
    def unexpected(cls, message: str, cause: BaseException | None = None) -> ApiError:
        return cls(message, kind=ErrorKind.UNEXPECTED, cause=cause)

    def with_idempotency_key(self, idempotency_key: str | None) -> ApiError:
        if idempotency_key is None or self.idempotency_key == idempotency_key:
            return self
        return ApiError(
            str(self),
            kind=self.kind,
            status_code=self.status_code,
            detail=self.detail,
            field_errors=self.field_errors,
            request_id=self.request_id,
            retry_after=self.retry_after,
            retry_at=self.retry_at,
            content_language=self.content_language,
            current_etag=self.current_etag,
            idempotency_key=idempotency_key,
            headers=self.headers,
            raw_body=self.raw_body,
            cause=self.__cause__,
        )


class PaginationError(LTESocksError):
    """Raised when an API page contains unsafe or inconsistent navigation data."""


class InvalidSignatureError(LTESocksError):
    """Raised when a webhook signature cannot be verified."""


def _kind_for_status(status_code: int) -> ErrorKind:
    if status_code == 400 or status_code == 422:
        return ErrorKind.VALIDATION
    if status_code == 401:
        return ErrorKind.AUTHENTICATION
    if status_code == 403:
        return ErrorKind.PERMISSION
    if status_code == 404:
        return ErrorKind.NOT_FOUND
    if status_code == 409:
        return ErrorKind.CONFLICT
    if status_code == 412:
        return ErrorKind.PRECONDITION
    if status_code == 429:
        return ErrorKind.RATE_LIMIT
    if status_code >= 500:
        return ErrorKind.SERVER
    return ErrorKind.UNEXPECTED


def _json_payload(content: bytes) -> Any:
    if not content:
        return None
    try:
        return json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def _detail(payload: Any) -> str | None:
    if isinstance(payload, str):
        return payload
    if not isinstance(payload, dict):
        return None
    for key in ("detail", "message", "error"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
        if isinstance(value, list) and value and all(isinstance(item, str) for item in value):
            return "; ".join(value)
    return None


def _field_errors(payload: Any) -> dict[str, list[str]]:
    if not isinstance(payload, dict):
        return {}
    result: dict[str, list[str]] = {}
    for key, value in payload.items():
        if key in {"detail", "message", "error"}:
            continue
        if isinstance(value, str):
            result[str(key)] = [value]
        elif isinstance(value, list) and all(isinstance(item, str) for item in value):
            result[str(key)] = value
    return result


def _header(headers: Mapping[str, str], *names: str) -> str | None:
    lowered = {key.lower(): value for key, value in headers.items()}
    for name in names:
        value = lowered.get(name)
        if value:
            return value
    return None


def _float_header(headers: Mapping[str, str], name: str) -> float | None:
    value = _header(headers, name)
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None

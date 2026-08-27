from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class ApiResponse(Generic[T]):
    """Parsed response data together with HTTP concurrency metadata."""

    data: T
    status_code: int
    headers: dict[str, str]
    etag: str | None
    idempotency_replayed: bool

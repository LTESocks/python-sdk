from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from uuid import UUID

import httpx
import pytest

from ltesocks_sdk import ApiError, AsyncClient, Client, ErrorKind, PaginationError

BASE_URL = "https://api.ltesocks.io/v2"


def test_bearer_auth_default_url_and_language() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"login": "demo"})

    http_client = httpx.Client(base_url=BASE_URL, transport=httpx.MockTransport(handler))
    client = Client.with_bearer_token("account-token", language="ru", http_client=http_client)

    user = client.user.get()

    assert user.login == "demo"
    assert requests[0].url == f"{BASE_URL}/user"
    assert requests[0].headers["Authorization"] == "Bearer account-token"
    assert requests[0].headers["Accept-Language"] == "ru"
    client.close()
    assert not http_client.is_closed
    http_client.close()


def test_errors_preserve_reset_timing_and_raw_body() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            500,
            json={"error": "Reset is cooling down"},
            headers={
                "Retry-After": "42",
                "Retry-At": "2026-08-27T12:00:00Z",
                "X-Request-ID": "request-123",
            },
        )

    http_client = httpx.Client(base_url=BASE_URL, transport=httpx.MockTransport(handler))
    client = Client.with_bearer_token("token", http_client=http_client)

    with pytest.raises(ApiError) as captured:
        client.ports.reset("10000")

    assert captured.value.kind is ErrorKind.SERVER
    assert captured.value.detail == "Reset is cooling down"
    assert captured.value.retry_after == 42
    assert captured.value.retry_at == "2026-08-27T12:00:00Z"
    assert captured.value.request_id == "request-123"
    assert captured.value.raw_body
    http_client.close()


def test_transport_retry_reuses_key_but_http_errors_are_not_retried(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("ltesocks_sdk.client.time.sleep", lambda _: None)
    keys: list[str | None] = []
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        keys.append(request.headers.get("Idempotency-Key"))
        if attempts == 1:
            raise httpx.ConnectError("connection reset", request=request)
        return httpx.Response(
            200,
            json={"port": "10000"},
            headers={"ETag": '"port-v2"', "Idempotency-Replayed": "true"},
        )

    http_client = httpx.Client(base_url=BASE_URL, transport=httpx.MockTransport(handler))
    client = Client.with_bearer_token("token", http_client=http_client)
    response = client.ports.reset_with_response("10000")

    assert len(keys) == 2
    assert keys[0] == keys[1]
    assert keys[0] is not None
    assert response.etag == '"port-v2"'
    assert response.idempotency_replayed
    http_client.close()

    error_attempts = 0

    def error_handler(_: httpx.Request) -> httpx.Response:
        nonlocal error_attempts
        error_attempts += 1
        return httpx.Response(503, json={"error": "Unavailable"})

    error_http = httpx.Client(base_url=BASE_URL, transport=httpx.MockTransport(error_handler))
    error_client = Client.with_bearer_token("token", http_client=error_http)
    with pytest.raises(ApiError):
        error_client.ports.reset("10000")
    assert error_attempts == 1
    error_http.close()


def test_explicit_idempotency_disable_and_raw_escape_hatch() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"port": "10000"})

    http_client = httpx.Client(base_url=BASE_URL, transport=httpx.MockTransport(handler))
    client = Client.with_bearer_token("token", idempotency=False, http_client=http_client)

    client.ports.reset("10000")
    client.ports.reset(
        "10000",
        idempotency_key=UUID("7c838e2d-7d52-42e7-aed1-528829cbd514"),
    )
    response = client.request("GET", "/future", params={"page": 2})

    assert requests[0].headers.get("Idempotency-Key") is None
    assert requests[1].headers["Idempotency-Key"] == "7c838e2d-7d52-42e7-aed1-528829cbd514"
    assert requests[2].url == f"{BASE_URL}/future?page=2"
    assert response.status_code == 200
    http_client.close()


def test_pagination_is_lazy_and_validates_metadata() -> None:
    calls: list[int] = []

    def fetch(*, page: int, page_size: int) -> Any:
        calls.append(page)
        data = [1, 2] if page == 1 else [3]
        return SimpleNamespace(data=data, page=page, page_size=page_size, total=3)

    with Client.anonymous() as client:
        iterator = client.paginate(fetch, page_size=2)
        assert calls == []
        assert list(iterator) == [1, 2, 3]
        assert calls == [1, 2]

        with pytest.raises(PaginationError):
            list(
                client.paginate(
                    lambda **_: SimpleNamespace(data=[1], page=2, page_size=1, total=2),
                    page_size=1,
                )
            )


@pytest.mark.asyncio
async def test_async_client_has_the_same_surface() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer async-token"
        return httpx.Response(200, json={"login": "async"})

    http_client = httpx.AsyncClient(base_url=BASE_URL, transport=httpx.MockTransport(handler))
    client = AsyncClient.with_bearer_token("async-token", http_client=http_client)
    assert (await client.user.get()).login == "async"

    async def fetch(*, page: int, page_size: int) -> Any:
        return SimpleNamespace(data=[page], page=page, page_size=page_size, total=2)

    assert [item async for item in client.paginate(fetch, page_size=1)] == [1, 2]
    await client.close()
    assert not http_client.is_closed
    await http_client.aclose()


def test_configuration_validation() -> None:
    with pytest.raises(ValueError, match="base_url"):
        Client.anonymous(base_url="ftp://example.com")
    external = httpx.Client(base_url="https://example.com")
    with pytest.raises(ValueError, match="base_url"):
        Client.anonymous(http_client=external)
    external.close()

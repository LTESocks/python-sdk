from __future__ import annotations

import asyncio
import time
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator, Mapping
from importlib.metadata import PackageNotFoundError, version
from types import TracebackType
from typing import Any, TypeVar

import httpx

from . import resources
from ._generated.client import AuthenticatedClient as GeneratedClient
from ._generated.types import UNSET, Response, Unset
from .errors import ApiError, PaginationError
from .files import FileDownload
from .response import ApiResponse

DEFAULT_BASE_URL = "https://api.ltesocks.io/v2"
T = TypeVar("T")

try:
    _PACKAGE_VERSION = version("ltesocks-sdk")
except PackageNotFoundError:  # pragma: no cover - only possible in an uninstalled source tree
    _PACKAGE_VERSION = "0.0.0"
USER_AGENT = f"ltesocks-python-sdk/{_PACKAGE_VERSION}"


def _base_url(value: str) -> str:
    normalized = value.rstrip("/")
    url = httpx.URL(normalized)
    if url.scheme not in {"http", "https"} or not url.host:
        raise ValueError("base_url must be an absolute HTTP or HTTPS URL.")
    return normalized


def _timeout(value: float | httpx.Timeout, connect_timeout: float) -> httpx.Timeout:
    return (
        value if isinstance(value, httpx.Timeout) else httpx.Timeout(value, connect=connect_timeout)
    )


def _headers(language: str, authorization: str | None, user_agent: str) -> dict[str, str]:
    if not language.strip():
        raise ValueError("language must not be empty.")
    headers = {
        "Accept": "application/json",
        "Accept-Language": language,
        "User-Agent": user_agent,
    }
    if authorization is not None:
        headers["Authorization"] = authorization
    return headers


def _authorization(bearer_token: str | None) -> str | None:
    if bearer_token is not None:
        if not bearer_token:
            raise ValueError("bearer_token must not be empty.")
        return f"Bearer {bearer_token}"
    return None


def _ensure_base_url(client: httpx.Client | httpx.AsyncClient, base_url: str) -> None:
    configured = str(client.base_url).rstrip("/")
    if configured != base_url:
        raise ValueError(f"The injected httpx client must use base_url={base_url!r}.")


def _apply_headers(client: httpx.Client | httpx.AsyncClient, headers: Mapping[str, str]) -> None:
    client.headers.update(headers)
    if "Authorization" not in headers:
        client.headers.pop("Authorization", None)


def _response_value(response: Response[Any]) -> Any:
    status_code = int(response.status_code)
    if not 200 <= status_code < 300:
        raise ApiError.from_response(status_code, response.content, response.headers)
    if response.parsed is None and response.content and status_code not in {204, 205}:
        raise ApiError.unexpected(f"LTESocks returned an unreadable HTTP {status_code} response.")
    return response.parsed


def _api_response(response: Response[Any], data: T) -> ApiResponse[T]:
    headers = {str(key).lower(): str(value) for key, value in response.headers.items()}
    return ApiResponse(
        data=data,
        status_code=int(response.status_code),
        headers=headers,
        etag=headers.get("etag"),
        idempotency_replayed=headers.get("idempotency-replayed", "").lower() == "true",
    )


def _prepare_idempotency_key(
    kwargs: dict[str, Any], *, idempotent: bool, enabled: bool
) -> str | None:
    if not idempotent:
        return None
    value = kwargs.get("idempotency_key", UNSET)
    if isinstance(value, Unset):
        if not enabled:
            return None
        value = str(uuid.uuid4())
        kwargs["idempotency_key"] = value
    elif isinstance(value, uuid.UUID):
        value = str(value)
        kwargs["idempotency_key"] = value
    return value if isinstance(value, str) and value else None


def _retry_delay(error: ApiError, attempt: int) -> float | None:
    if error.kind.value == "network":
        return 0.1 if attempt == 0 else 0.2
    return None


def _page_values(value: Any) -> tuple[list[Any], int, int]:
    data = getattr(value, "data", None)
    page = getattr(value, "page", None)
    total = getattr(value, "total", None)
    if not isinstance(data, list) or not isinstance(page, int) or not isinstance(total, int):
        raise PaginationError("A page must expose data, page, and total fields.")
    return data, page, total


class Client:
    """Synchronous LTESocks API client."""

    def __init__(
        self,
        *,
        bearer_token: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        language: str = "en",
        timeout: float | httpx.Timeout = 15.0,
        connect_timeout: float = 5.0,
        verify: bool = True,
        follow_redirects: bool = False,
        idempotency: bool = True,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.base_url = _base_url(base_url)
        self.idempotency = idempotency
        authorization = _authorization(bearer_token)
        default_headers = _headers(language, authorization, USER_AGENT)
        self._owns_http_client = http_client is None
        if http_client is None:
            http_client = httpx.Client(
                base_url=self.base_url,
                headers=default_headers,
                timeout=_timeout(timeout, connect_timeout),
                verify=verify,
                follow_redirects=follow_redirects,
            )
        else:
            _ensure_base_url(http_client, self.base_url)
            _apply_headers(http_client, default_headers)
        self._http_client = http_client
        self._generated = GeneratedClient(base_url=self.base_url, token="")
        self._generated.set_httpx_client(http_client)
        self._closed = False
        self._attach_resources()

    @classmethod
    def with_bearer_token(cls, token: str, **options: Any) -> Client:
        return cls(bearer_token=token, **options)

    @classmethod
    def anonymous(cls, **options: Any) -> Client:
        return cls(**options)

    def _attach_resources(self) -> None:
        self.user = resources.UserResource(self)
        self.ports = resources.PortsResource(self)
        self.payments = resources.PaymentsResource(self)
        self.general = resources.GeneralResource(self)

    def _call(
        self,
        endpoint: Callable[..., Response[Any]],
        *,
        _idempotent: bool = False,
        **kwargs: Any,
    ) -> Any:
        return self._call_with_response(endpoint, _idempotent=_idempotent, **kwargs).data

    def _call_with_response(
        self,
        endpoint: Callable[..., Response[Any]],
        *,
        _idempotent: bool = False,
        **kwargs: Any,
    ) -> ApiResponse[Any]:
        idempotency_key = _prepare_idempotency_key(
            kwargs, idempotent=_idempotent, enabled=self.idempotency
        )
        for attempt in range(3):
            try:
                response = endpoint(client=self._generated, **kwargs)
                return _api_response(response, _response_value(response))
            except httpx.HTTPError as error:
                api_error = ApiError.network(error).with_idempotency_key(idempotency_key)
            except ApiError as error:
                api_error = error.with_idempotency_key(idempotency_key)
            except Exception as error:
                raise ApiError.unexpected(
                    "Unable to decode the LTESocks API response.", error
                ) from error
            delay = _retry_delay(api_error, attempt)
            if attempt >= 2 or idempotency_key is None or delay is None:
                raise api_error
            time.sleep(delay)
        raise ApiError.unexpected("Unable to complete the LTESocks API call.")

    def _download(self, endpoint: Callable[..., Response[Any]], **kwargs: Any) -> FileDownload:
        return self._download_with_response(endpoint, **kwargs).data

    def _download_with_response(
        self, endpoint: Callable[..., Response[Any]], **kwargs: Any
    ) -> ApiResponse[FileDownload]:
        try:
            response = endpoint(client=self._generated, **kwargs)
            _response_value(response)
            download = FileDownload.from_response(response.content, response.headers)
            return _api_response(response, download)
        except ApiError:
            raise
        except httpx.HTTPError as error:
            raise ApiError.network(error) from error

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        headers: Mapping[str, str] | None = None,
        **options: Any,
    ) -> httpx.Response:
        try:
            response = self._http_client.request(
                method.upper(), path, params=params, json=json, headers=headers, **options
            )
        except httpx.HTTPError as error:
            raise ApiError.network(error) from error
        if not response.is_success:
            raise ApiError.from_response(response.status_code, response.content, response.headers)
        return response

    def paginate(
        self,
        page_fetcher: Callable[..., Any],
        *,
        page_size: int = 100,
        start_page: int = 1,
        max_pages: int = 10_000,
        **filters: Any,
    ) -> Iterator[Any]:
        if not 1 <= page_size <= 100 or start_page <= 0 or max_pages <= 0:
            raise ValueError("page_size must be 1..100; start_page and max_pages must be positive.")
        current_page = start_page
        for _ in range(max_pages):
            result = page_fetcher(page=current_page, page_size=page_size, **filters)
            data, response_page, total = _page_values(result)
            if response_page != current_page:
                raise PaginationError("The API returned an unexpected page number.")
            yield from data
            if current_page * page_size >= total or not data:
                return
            current_page += 1
        raise PaginationError("Pagination stopped after the configured maximum number of pages.")

    def download_port_vpn(self, port_id: str) -> FileDownload:
        return self.ports.download_vpn(port_id)

    def close(self) -> None:
        if not self._closed and self._owns_http_client:
            self._http_client.close()
        self._closed = True

    def __enter__(self) -> Client:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()


class AsyncClient:
    """Asynchronous LTESocks API client."""

    def __init__(
        self,
        *,
        bearer_token: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        language: str = "en",
        timeout: float | httpx.Timeout = 15.0,
        connect_timeout: float = 5.0,
        verify: bool = True,
        follow_redirects: bool = False,
        idempotency: bool = True,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.base_url = _base_url(base_url)
        self.idempotency = idempotency
        authorization = _authorization(bearer_token)
        default_headers = _headers(language, authorization, USER_AGENT)
        self._owns_http_client = http_client is None
        if http_client is None:
            http_client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=default_headers,
                timeout=_timeout(timeout, connect_timeout),
                verify=verify,
                follow_redirects=follow_redirects,
            )
        else:
            _ensure_base_url(http_client, self.base_url)
            _apply_headers(http_client, default_headers)
        self._http_client = http_client
        self._generated = GeneratedClient(base_url=self.base_url, token="")
        self._generated.set_async_httpx_client(http_client)
        self._closed = False
        self._attach_resources()

    @classmethod
    def with_bearer_token(cls, token: str, **options: Any) -> AsyncClient:
        return cls(bearer_token=token, **options)

    @classmethod
    def anonymous(cls, **options: Any) -> AsyncClient:
        return cls(**options)

    def _attach_resources(self) -> None:
        self.user = resources.AsyncUserResource(self)
        self.ports = resources.AsyncPortsResource(self)
        self.payments = resources.AsyncPaymentsResource(self)
        self.general = resources.AsyncGeneralResource(self)

    async def _call(
        self,
        endpoint: Callable[..., Awaitable[Response[Any]]],
        *,
        _idempotent: bool = False,
        **kwargs: Any,
    ) -> Any:
        return (await self._call_with_response(endpoint, _idempotent=_idempotent, **kwargs)).data

    async def _call_with_response(
        self,
        endpoint: Callable[..., Awaitable[Response[Any]]],
        *,
        _idempotent: bool = False,
        **kwargs: Any,
    ) -> ApiResponse[Any]:
        idempotency_key = _prepare_idempotency_key(
            kwargs, idempotent=_idempotent, enabled=self.idempotency
        )
        for attempt in range(3):
            try:
                response = await endpoint(client=self._generated, **kwargs)
                return _api_response(response, _response_value(response))
            except httpx.HTTPError as error:
                api_error = ApiError.network(error).with_idempotency_key(idempotency_key)
            except ApiError as error:
                api_error = error.with_idempotency_key(idempotency_key)
            except Exception as error:
                raise ApiError.unexpected(
                    "Unable to decode the LTESocks API response.", error
                ) from error
            delay = _retry_delay(api_error, attempt)
            if attempt >= 2 or idempotency_key is None or delay is None:
                raise api_error
            await asyncio.sleep(delay)
        raise ApiError.unexpected("Unable to complete the LTESocks API call.")

    async def _download(
        self,
        endpoint: Callable[..., Awaitable[Response[Any]]],
        **kwargs: Any,
    ) -> FileDownload:
        return (await self._download_with_response(endpoint, **kwargs)).data

    async def _download_with_response(
        self,
        endpoint: Callable[..., Awaitable[Response[Any]]],
        **kwargs: Any,
    ) -> ApiResponse[FileDownload]:
        try:
            response = await endpoint(client=self._generated, **kwargs)
            _response_value(response)
            download = FileDownload.from_response(response.content, response.headers)
            return _api_response(response, download)
        except ApiError:
            raise
        except httpx.HTTPError as error:
            raise ApiError.network(error) from error

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        headers: Mapping[str, str] | None = None,
        **options: Any,
    ) -> httpx.Response:
        try:
            response = await self._http_client.request(
                method.upper(), path, params=params, json=json, headers=headers, **options
            )
        except httpx.HTTPError as error:
            raise ApiError.network(error) from error
        if not response.is_success:
            raise ApiError.from_response(response.status_code, response.content, response.headers)
        return response

    async def paginate(
        self,
        page_fetcher: Callable[..., Awaitable[Any]],
        *,
        page_size: int = 100,
        start_page: int = 1,
        max_pages: int = 10_000,
        **filters: Any,
    ) -> AsyncIterator[Any]:
        if not 1 <= page_size <= 100 or start_page <= 0 or max_pages <= 0:
            raise ValueError("page_size must be 1..100; start_page and max_pages must be positive.")
        current_page = start_page
        for _ in range(max_pages):
            result = await page_fetcher(page=current_page, page_size=page_size, **filters)
            data, response_page, total = _page_values(result)
            if response_page != current_page:
                raise PaginationError("The API returned an unexpected page number.")
            for item in data:
                yield item
            if current_page * page_size >= total or not data:
                return
            current_page += 1
        raise PaginationError("Pagination stopped after the configured maximum number of pages.")

    async def download_port_vpn(self, port_id: str) -> FileDownload:
        return await self.ports.download_vpn(port_id)

    async def close(self) -> None:
        if not self._closed and self._owns_http_client:
            await self._http_client.aclose()
        self._closed = True

    async def __aenter__(self) -> AsyncClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()

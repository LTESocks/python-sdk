from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.residential_package_response import ResidentialPackageResponse
from typing import cast
from uuid import UUID


def _get_kwargs(
    child_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/proxies/residential/subusers/{child_id}/package".format(
            child_id=quote(str(child_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ResidentialPackageResponse | None:
    if response.status_code == 200:
        response_200 = ResidentialPackageResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | ResidentialPackageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    child_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Error | ResidentialPackageResponse]:
    """Get package and traffic allocation

    Args:
        child_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ResidentialPackageResponse]
    """

    kwargs = _get_kwargs(
        child_id=child_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    child_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Error | ResidentialPackageResponse | None:
    """Get package and traffic allocation

    Args:
        child_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ResidentialPackageResponse
    """

    return sync_detailed(
        child_id=child_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    child_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Error | ResidentialPackageResponse]:
    """Get package and traffic allocation

    Args:
        child_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ResidentialPackageResponse]
    """

    kwargs = _get_kwargs(
        child_id=child_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    child_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Error | ResidentialPackageResponse | None:
    """Get package and traffic allocation

    Args:
        child_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ResidentialPackageResponse
    """

    return (
        await asyncio_detailed(
            child_id=child_id,
            client=client,
        )
    ).parsed

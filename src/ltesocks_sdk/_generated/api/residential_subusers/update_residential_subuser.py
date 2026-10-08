from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.residential_subuser_response import ResidentialSubuserResponse
from ...models.update_residential_subuser import UpdateResidentialSubuser
from typing import cast
from uuid import UUID


def _get_kwargs(
    child_id: UUID,
    *,
    body: UpdateResidentialSubuser,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/proxies/residential/subusers/{child_id}".format(
            child_id=quote(str(child_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ResidentialSubuserResponse | None:
    if response.status_code == 200:
        response_200 = ResidentialSubuserResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | ResidentialSubuserResponse]:
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
    body: UpdateResidentialSubuser,
) -> Response[Error | ResidentialSubuserResponse]:
    """Update sub-user details and access rules

    Args:
        child_id (UUID):
        body (UpdateResidentialSubuser):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ResidentialSubuserResponse]
    """

    kwargs = _get_kwargs(
        child_id=child_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    child_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateResidentialSubuser,
) -> Error | ResidentialSubuserResponse | None:
    """Update sub-user details and access rules

    Args:
        child_id (UUID):
        body (UpdateResidentialSubuser):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ResidentialSubuserResponse
    """

    return sync_detailed(
        child_id=child_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    child_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateResidentialSubuser,
) -> Response[Error | ResidentialSubuserResponse]:
    """Update sub-user details and access rules

    Args:
        child_id (UUID):
        body (UpdateResidentialSubuser):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ResidentialSubuserResponse]
    """

    kwargs = _get_kwargs(
        child_id=child_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    child_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateResidentialSubuser,
) -> Error | ResidentialSubuserResponse | None:
    """Update sub-user details and access rules

    Args:
        child_id (UUID):
        body (UpdateResidentialSubuser):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ResidentialSubuserResponse
    """

    return (
        await asyncio_detailed(
            child_id=child_id,
            client=client,
            body=body,
        )
    ).parsed

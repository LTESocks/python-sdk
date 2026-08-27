from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from ltesocks_sdk import AsyncClient, Client

BASE_URL = "https://api.ltesocks.io/v2"
ZIP = b"PK\x03\x04example"


def response(_: httpx.Request) -> httpx.Response:
    return httpx.Response(
        200,
        content=ZIP,
        headers={
            "Content-Type": "application/zip",
            "Content-Disposition": 'attachment; filename="vpn.zip"',
        },
    )


def test_vpn_download_and_safe_save(tmp_path: Path) -> None:
    http_client = httpx.Client(base_url=BASE_URL, transport=httpx.MockTransport(response))
    client = Client.with_bearer_token("token", http_client=http_client)
    download = client.download_port_vpn("10000")

    assert download.content == ZIP
    assert download.filename == "vpn.zip"
    assert download.content_type == "application/zip"
    destination = download.save(tmp_path)
    assert destination.read_bytes() == ZIP
    with pytest.raises(FileExistsError):
        download.save(destination)
    http_client.close()


@pytest.mark.asyncio
async def test_async_vpn_download() -> None:
    http_client = httpx.AsyncClient(base_url=BASE_URL, transport=httpx.MockTransport(response))
    client = AsyncClient.with_bearer_token("token", http_client=http_client)
    download = await client.download_port_vpn("10000")
    assert download.content == ZIP
    await http_client.aclose()

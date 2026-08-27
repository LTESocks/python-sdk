# LTESocks Python SDK

[![CI](https://github.com/LTESocks/python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/LTESocks/python-sdk/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-%3E%3D3.11-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![Typed](https://img.shields.io/badge/typing-py.typed-3776AB)](src/ltesocks_sdk/py.typed)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

The official synchronous and asynchronous Python client for the [LTESocks Public API v2](https://docs.ltesocks.io/). It covers account preferences, mobile proxy ports, payments, plans, servers, and network signatures with generated typed models.

> Package publication has not started yet. The repository is ready, but `ltesocks-sdk` is intentionally not available on PyPI until the first release is approved.

## Installation for development

```bash
git clone https://github.com/LTESocks/python-sdk.git
cd python-sdk
uv sync --all-groups
```

After the first PyPI release, installation will be:

```bash
pip install ltesocks-sdk
```

## Quick start

```python
import os

from ltesocks_sdk import Client

with Client.with_bearer_token(os.environ["LTESOCKS_API_TOKEN"]) as client:
    user = client.user.get()
    plans = client.general.list_plans()
    ports = client.ports.list()
    print(user.login, plans.plans, ports.total)
```

Async code uses the same resources and method names:

```python
from ltesocks_sdk import AsyncClient

async with AsyncClient.with_bearer_token(token) as client:
    port = await client.ports.get("10000")
```

The default endpoint is `https://api.ltesocks.io/v2`. Both clients accept `base_url`, `language`, timeouts, TLS settings, and an injected `httpx.Client`/`httpx.AsyncClient`.

## Resources

| Resource | Purpose |
| --- | --- |
| `client.user` | Read the account and update preferences |
| `client.ports` | List, filter, order, update, reset, delete, and download VPN archives |
| `client.payments` | List/filter history and access reserved payment operations |
| `client.general` | List plans, servers, and signatures |

Every operation also has a `_with_response()` variant with status, headers, ETag, and replay metadata. See the generated [API resource reference](docs/reference/api.md) and [model reference](docs/reference/models.md).

## Typed request models

```python
from ltesocks_sdk.models import OrderPortsBody, PlanTarification

port = client.ports.order(
    body=OrderPortsBody(
        plan="plan-id",
        tarification=PlanTarification(time=2_592_000, price=10_000),
    )
)
```

Fields follow Python `snake_case`; `to_dict()` and `from_dict()` translate to the API JSON names.

## Idempotency and retries

The SDK creates a UUID for every supported idempotent mutation. It retries at most twice, with the same key, only when no HTTP response was received. It does not automatically retry a `4xx` or `5xx` response.

```python
response = client.ports.reset_with_response("10000")
print(response.idempotency_replayed, response.headers.get("retry-at"))
```

Pass `idempotency_key=UUID(...)` for a stored logical request, or set `idempotency=False`. Read [idempotency, errors, and reset timing](docs/guides/idempotency-errors-and-reset.md).

## Errors

```python
from ltesocks_sdk import ApiError

try:
    client.ports.reset("10000")
except ApiError as error:
    print(error.status_code, error.kind, error.detail)
    print(error.retry_after, error.retry_at, error.idempotency_key)
```

Errors retain normalized headers and raw bytes. `client.request()` is the raw escape hatch for endpoints added before the next generated version.

## VPN archives

```python
archive = client.ports.download_vpn("10000")
archive.save_to("ltesocks-vpn.zip")
```

## Webhooks

Verify the exact request body before decoding it. `X-Signature` is `Base64(HMAC-SHA256(webhook_secret, raw_body))`.

```python
from ltesocks_sdk import WebhookVerifier

event = WebhookVerifier.decode_verified_json(raw_body, signature, webhook_secret)
```

See [webhook verification](docs/guides/webhooks.md).

## Development

```bash
uv sync --all-groups
uv run python scripts/check_generated.py
uv run ruff check .
uv run mypy
uv run pytest
uv build
uv run twine check dist/*
```

The generated surface is pinned to [`openapi/openapi.yaml`](openapi/openapi.yaml). Use `uv run python scripts/sync_openapi.py ../../site/docs/openapi.yaml` and regenerate after canonical contract changes.

## Links

- [Documentation](https://docs.ltesocks.io/)
- [API reference](https://docs.ltesocks.io/api-reference/)
- [OpenAPI YAML](https://docs.ltesocks.io/openapi.yaml)
- [JavaScript SDK](https://github.com/LTESocks/javascript-sdk)
- [PHP SDK](https://github.com/LTESocks/php-sdk)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

Licensed under the [MIT License](LICENSE).

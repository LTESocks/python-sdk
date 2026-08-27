# Idempotency, errors, and port reset timing

The sync and async clients automatically create UUIDs for the ten mutations that accept `Idempotency-Key`. A protected call can make at most three attempts, only when no HTTP response was received. HTTP errors are never retried automatically.

Use an application-owned UUID when a logical request must survive a process restart:

```python
from uuid import UUID

client.ports.reset(
    "10000",
    idempotency_key=UUID("7c838e2d-7d52-42e7-aed1-528829cbd514"),
)
```

## Reset timing

- HTTP `200` acknowledges the reset; it does not prove a new IP is ready.
- The minimum user-triggered cooldown is 60 seconds, and a pool can require longer.
- Respect `ApiError.retry_after` and `ApiError.retry_at`; when both exist, wait until the later deadline.
- Prefer `port.ip_changed`; otherwise poll `client.ports.get()` with bounded backoff and compare `ip`.
- Use `auto_reset_interval=0` to disable scheduling or at least 180 seconds for a supported interval. Values `1..179` are below the scheduler threshold.

See [Port reset and readiness](https://docs.ltesocks.io/guides/port-reset-and-readiness/).

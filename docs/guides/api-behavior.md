# API behavior

- Filtered ports, logs, and payments use `page` and `page_size` request-model fields; `page_size` is capped at 100.
- Default service limits are 60 GET requests/minute and 10 mutation requests/minute. Deployments can override them; handle `429` explicitly.
- `payments.list_currencies()` and `payments.request()` cover reserved contract operations that are still under development and have no normal success payload.
- Prefer `ports.delete()` and `ports.download_vpn()`; `_compat` methods represent POST compatibility routes.
- Use `Port.port` in port routes. `reset_token` only identifies the token lookup route and is not authentication.

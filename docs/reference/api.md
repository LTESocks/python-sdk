# API resource reference

All methods exist on both `Client` and `AsyncClient`; async calls must be awaited.

## `general`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `list_plans()` | `GET /plans` | `ListPlansResponse200` |
| `list_servers()` | `GET /servers` | `ListServersResponse200` |
| `list_signatures()` | `GET /signatures` | `ListSignaturesResponse200` |

## `payments`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `filter()` | `POST /payments` | `FilterPaymentsResponse200` |
| `list()` | `GET /payments` | `ListPaymentsResponse200` |
| `list_currencies()` | `GET /payments/currencies` | `None` |
| `request()` | `POST /payments/request` | `None` |

## `ports`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `change_plan()` | `POST /ports/{id}/plan` | `Port` |
| `delete()` | `DELETE /ports/{id}` | `None` |
| `delete_compat()` | `POST /ports/{id}/delete` | `None` |
| `download_vpn()` | `GET /ports/{id}/vpn` | `FileDownload` |
| `download_vpn_compat()` | `POST /ports/{id}/vpn` | `FileDownload` |
| `extend()` | `POST /ports/{id}/extend` | `Port` |
| `filter()` | `POST /ports` | `FilterPortsResponse200` |
| `filter_log()` | `POST /ports/{id}/log` | `FilterPortLogResponse200` |
| `get()` | `GET /ports/{id}` | `Port` |
| `get_log()` | `GET /ports/{id}/log` | `GetPortLogResponse200` |
| `list()` | `GET /ports` | `ListPortsResponse200` |
| `order()` | `POST /ports/order` | `Port` |
| `reset()` | `POST /ports/{id}/reset` | `Port` |
| `resolve_reset_token()` | `GET /tokens/{token}` | `Port` |
| `set_auto_renew()` | `POST /ports/{id}/autorenew` | `Port` |
| `set_auto_reset_interval()` | `POST /ports/{id}/autoreset` | `Port` |
| `update_credentials()` | `POST /ports/{id}/credentials` | `Port` |
| `update_signature()` | `POST /ports/{id}/signature` | `Port` |
| `update_tags()` | `POST /ports/{id}/tags` | `Port` |

## `residential_subusers`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `change_traffic()` | `POST /proxies/residential/subusers/{childId}/traffic/{action}` | `ResidentialSubuserResponse` |
| `create()` | `POST /proxies/residential/subusers` | `ResidentialSubuserResponse` |
| `delete()` | `DELETE /proxies/residential/subusers/{childId}` | `None` |
| `get()` | `GET /proxies/residential/subusers/{childId}` | `ResidentialSubuserResponse` |
| `get_credentials()` | `GET /proxies/residential/subusers/{childId}/credentials` | `ResidentialCredentialsResponse` |
| `get_package()` | `GET /proxies/residential/subusers/{childId}/package` | `ResidentialPackageResponse` |
| `list()` | `GET /proxies/residential/subusers` | `ResidentialSubuserListResponse` |
| `update()` | `PATCH /proxies/residential/subusers/{childId}` | `ResidentialSubuserResponse` |

## `user`

| Method | HTTP endpoint | Returns |
| --- | --- | --- |
| `get()` | `GET /user` | `User` |
| `update_preferences()` | `POST /user/preferences` | `User` |

# Webhook verification

`X-Signature` contains `Base64(HMAC-SHA256(webhook_secret, raw_request_body))`. Verify the exact bytes before JSON decoding:

```python
event = WebhookVerifier.decode_verified_json(raw_body, signature, webhook_secret)
```

Store the event `id` before side effects and return `2xx` for a duplicate without reprocessing it. A delivery can occur up to four times under the default policy (initial attempt plus three retries, 10 seconds apart, with 5-second network timeouts).

See the [webhook contract](https://docs.ltesocks.io/webhooks/).

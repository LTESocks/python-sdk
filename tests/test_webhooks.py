from __future__ import annotations

import base64
import hashlib
import hmac

import pytest

from ltesocks_sdk import InvalidSignatureError, WebhookVerifier


def signature(body: bytes, secret: str) -> str:
    return base64.b64encode(hmac.new(secret.encode(), body, hashlib.sha256).digest()).decode()


def test_valid_signature_and_verified_json() -> None:
    body = b'{"id":"evt-1","type":"port.ip_changed"}'
    header = signature(body, "secret")
    assert WebhookVerifier.verify(body, header, "secret")
    assert WebhookVerifier.decode_verified_json(body, header, "secret")["id"] == "evt-1"


def test_tampering_and_invalid_payloads_are_rejected() -> None:
    body = b"{}"
    header = signature(body, "secret")
    assert not WebhookVerifier.verify(body + b" ", header, "secret")
    assert not WebhookVerifier.verify(body, "invalid", "secret")
    with pytest.raises(InvalidSignatureError):
        WebhookVerifier.verify_or_raise(body, header, "wrong")

    array_body = b"[]"
    with pytest.raises(ValueError, match="JSON object"):
        WebhookVerifier.decode_verified_json(array_body, signature(array_body, "secret"), "secret")

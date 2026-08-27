from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
from typing import Any

from .errors import InvalidSignatureError


class WebhookVerifier:
    """Verify X-Signature against the exact raw request body."""

    @staticmethod
    def verify(raw_body: bytes | str, signature: str, secret: str) -> bool:
        if not signature or not secret:
            return False
        body = raw_body.encode() if isinstance(raw_body, str) else raw_body
        expected = hmac.new(secret.encode(), body, hashlib.sha256).digest()
        try:
            received = base64.b64decode(signature.strip(), validate=True)
        except (binascii.Error, ValueError):
            return False
        return hmac.compare_digest(expected, received)

    @staticmethod
    def verify_or_raise(raw_body: bytes | str, signature: str, secret: str) -> None:
        if not WebhookVerifier.verify(raw_body, signature, secret):
            raise InvalidSignatureError("The LTESocks webhook signature is invalid.")

    @staticmethod
    def decode_verified_json(raw_body: bytes | str, signature: str, secret: str) -> dict[str, Any]:
        WebhookVerifier.verify_or_raise(raw_body, signature, secret)
        try:
            payload = json.loads(raw_body)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("The verified webhook body is not valid JSON.") from error
        if not isinstance(payload, dict) or not all(isinstance(key, str) for key in payload):
            raise ValueError("The verified webhook payload must be a JSON object.")
        return payload

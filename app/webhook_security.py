from __future__ import annotations

import hashlib
import hmac
from typing import Optional


def verify_meta_signature(
    raw_body: bytes,
    signature_header: Optional[str],
    app_secret: str,
) -> bool:
    """
    Verifica el header X-Hub-Signature-256 (sha256=<hexdigest>) de Meta.
    Si no hay app_secret configurado, se considera "no verificado".
    """
    if not app_secret:
        return True

    if not signature_header:
        return False

    if not signature_header.startswith("sha256="):
        return False

    received = signature_header.split("=", 1)[1].strip()
    expected = hmac.new(app_secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(received, expected)


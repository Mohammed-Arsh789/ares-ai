"""
ARES URL Validation
"""

from __future__ import annotations

from urllib.parse import urlparse


ALLOWED_SCHEMES = {
    "http",
    "https",
}


def validate_url(
    url: str,
) -> bool:

    if not isinstance(
        url,
        str,
    ):

        return False

    url = url.strip()

    if not url:

        return False

    if len(url) > 2048:

        return False

    try:

        parsed = urlparse(url)

    except Exception:

        return False

    if parsed.scheme.lower() not in ALLOWED_SCHEMES:

        return False

    if not parsed.netloc:

        return False

    # Reject credentials embedded in URLs.
    if parsed.username or parsed.password:

        return False

    return True
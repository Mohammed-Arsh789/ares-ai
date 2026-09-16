"""
ARES Web Page Fetcher
"""

from __future__ import annotations

import requests

from .url_validator import validate_url
from .web_config import WebConfig
from .web_retry import retry


class WebFetcher:

    def __init__(
        self,
        config: WebConfig | None = None,
    ):

        self.config = (
            config
            or WebConfig()
        )

    def fetch(
        self,
        url: str,
    ) -> dict:

        if not validate_url(url):

            raise ValueError(
                "Only valid HTTP/HTTPS URLs are allowed."
            )

        def request():

            response = requests.get(
                url,
                timeout=self.config.timeout_seconds,
                headers={
                    "User-Agent":
                        self.config.user_agent,
                },
            )

            response.raise_for_status()

            return response

        response = retry(
            request,
            attempts=3,
        )

        content = response.text[
            :self.config.max_content_chars
        ]

        return {
            "url": url,
            "status_code":
                response.status_code,
            "content": content,
            "content_type":
                response.headers.get(
                    "content-type",
                    "",
                ),
        }
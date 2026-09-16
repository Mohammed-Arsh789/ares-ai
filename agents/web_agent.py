"""
ARES Web Agent

High-level interface over WebIntelligence.

Future research agents can use this instead of
calling low-level web tools directly.
"""

from __future__ import annotations

from tools.web_intelligence import WebIntelligence


class WebAgent:

    name = "web_agent"

    def __init__(
        self,
        web: WebIntelligence | None = None,
    ):

        self.web = (
            web
            or WebIntelligence()
        )

    def search(
        self,
        query: str,
        max_results: int = 5,
    ):

        return self.web.search(
            query=query,
            max_results=max_results,
        )

    def open(
        self,
        url: str,
    ):

        return self.web.fetch_url(
            url
        )
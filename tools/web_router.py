"""
ARES Web Router
"""

from __future__ import annotations

from tools.web_query import (
    classify_web_query,
    WebQueryType,
)


class WebRouter:

    def route(
        self,
        query: str,
    ) -> dict:

        query_type = classify_web_query(
            query
        )

        if query_type == WebQueryType.URL:

            action = "fetch_url"

        elif query_type == WebQueryType.CURRENT:

            action = "search_current"

        else:

            action = "search"

        return {
            "system": "web",
            "action": action,
            "query": query.strip(),
        }
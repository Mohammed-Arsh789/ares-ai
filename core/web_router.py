"""
ARES Web Router

Routes web-related requests without executing them.

The router decides WHAT should happen.
The executor decides HOW it is executed.
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

        query = query.strip()

        if not query:
            raise ValueError(
                "Web query cannot be empty."
            )

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
            "query": query,
        }
"""
ARES Web Intelligence Tool

Step 184

Provides controlled public-web search.

This tool:
- validates the query
- limits result count
- handles search failures
- returns structured ToolResult
"""

from __future__ import annotations

from typing import Any

from tools.base import Tool
from tools.result import ToolResult


class WebTool(Tool):

    name = "web"

    description = (
        "Search the public web for current information."
    )

    dangerous = False

    requires_confirmation = False

    DEFAULT_RESULTS = 5

    MAX_RESULTS = 10

    def run(
        self,
        query: str,
        max_results: int = DEFAULT_RESULTS,
    ) -> ToolResult:

        try:

            query = query.strip()

            if not query:

                return ToolResult.fail(
                    self.name,
                    "Search query cannot be empty.",
                )

            max_results = int(
                max_results
            )

            max_results = max(
                1,
                min(
                    max_results,
                    self.MAX_RESULTS,
                ),
            )

            from ddgs import DDGS

            results: list[dict[str, Any]] = []

            with DDGS() as ddgs:

                search_results = ddgs.text(
                    query,
                    max_results=max_results,
                )

                for item in search_results:

                    results.append(
                        {
                            "title": item.get(
                                "title",
                                "",
                            ),
                            "url": item.get(
                                "href",
                                "",
                            ),
                            "snippet": item.get(
                                "body",
                                "",
                            ),
                        }
                    )

            return ToolResult.ok(
                self.name,
                {
                    "query": query,
                    "results": results,
                },
            )

        except Exception as error:

            return ToolResult.fail(
                self.name,
                f"Web search failed: {error}",
            )
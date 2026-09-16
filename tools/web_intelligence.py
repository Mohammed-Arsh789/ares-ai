"""
ARES Web Intelligence Controller

Unified entry point for web operations.

Responsibilities:
    - classify web requests
    - search
    - rank results
    - create structured sources
    - fetch direct URLs
"""

from __future__ import annotations

from .source import Source
from .web import WebTool
from .web_fetch import WebFetcher
from .web_query import (
    WebQueryType,
    classify_web_query,
)
from .web_ranker import WebRanker
from .web_response import WebResponse
from .web_result import WebResult


class WebIntelligence:

    def __init__(
        self,
        web_tool: WebTool | None = None,
        fetcher: WebFetcher | None = None,
    ):

        self.web = (
            web_tool
            or WebTool()
        )

        self.fetcher = (
            fetcher
            or WebFetcher()
        )

        self.ranker = WebRanker()

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> WebResponse:

        query = query.strip()

        if not query:

            return WebResponse.failure(
                query,
                "Search query cannot be empty.",
            )

        query_type = classify_web_query(
            query
        )

        if query_type == WebQueryType.URL:

            return self.fetch_url(query)

        response = self.web.run(
            query=query,
            max_results=max_results,
        )

        if not response.success:

            return WebResponse.failure(
                query,
                response.error
                or "Unknown web error.",
            )

        raw_results = (
            response.data.get(
                "results",
                [],
            )
            if isinstance(
                response.data,
                dict,
            )
            else []
        )

        results = []

        for item in raw_results:

            results.append(
                WebResult(
                    title=item.get(
                        "title",
                        "",
                    ),
                    url=item.get(
                        "url",
                        "",
                    ),
                    snippet=item.get(
                        "snippet",
                        "",
                    ),
                )
            )

        ranked = self.ranker.rank(
            query,
            results,
        )

        sources = []

        for result in ranked:

            sources.append(
                Source(
                    title=result.title,
                    url=result.url,
                    snippet=result.snippet,
                ).to_dict()
            )

        return WebResponse(
            query=query,
            success=True,
            results=[
                result.to_dict()
                for result in ranked
            ],
            sources=sources,
            metadata={
                "query_type":
                    query_type.value,
                "result_count":
                    len(ranked),
            },
        )

    def fetch_url(
        self,
        url: str,
    ) -> WebResponse:

        try:

            page = self.fetcher.fetch(
                url
            )

            content = page.get(
                "content",
                "",
            )

            snippet = content[:500]

            return WebResponse(
                query=url,
                success=True,
                results=[
                    {
                        "title": url,
                        "url": url,
                        "snippet": snippet,
                    }
                ],
                sources=[
                    {
                        "title": url,
                        "url": url,
                        "snippet": snippet,
                        "source_type":
                            "web_page",
                    }
                ],
                metadata={
                    "status_code":
                        page.get(
                            "status_code"
                        ),
                    "content_type":
                        page.get(
                            "content_type",
                            "",
                        ),
                },
            )

        except Exception as error:

            return WebResponse.failure(
                url,
                str(error),
            )
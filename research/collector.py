from .models import ResearchSource
from .sources import SourceManager


class ResearchCollector:
    """
    Collects research results from an injected search function.

    The search function can later connect to WebIntelligence.
    """

    def __init__(
        self,
        search_function=None,
        source_manager: SourceManager | None = None,
    ):
        self.search_function = search_function
        self.source_manager = (
            source_manager or SourceManager()
        )

    def collect(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[ResearchSource]:
        if self.search_function is None:
            return []

        raw_results = self.search_function(
            query,
            max_results=max_results,
        )

        if isinstance(raw_results, dict):
            raw_results = raw_results.get(
                "results",
                [],
            )

        sources = []

        for item in raw_results or []:
            if not isinstance(item, dict):
                continue

            url = item.get("url") or item.get("link")

            if not url:
                continue

            sources.append(
                self.source_manager.create_source(
                    title=item.get("title", ""),
                    url=url,
                    snippet=item.get("snippet", ""),
                )
            )

        return self.source_manager.deduplicate(sources)
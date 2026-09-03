from tools.base import Tool
from tools.result import ToolResult


class WebTool(Tool):
    name = "web"
    description = "Searches the public web for information."

    def run(
        self,
        query,
        max_results=5,
    ):
        try:
            from ddgs import DDGS

            if not query or not query.strip():
                raise ValueError(
                    "Search query is empty."
                )

            results = []

            with DDGS() as ddgs:
                search_results = ddgs.text(
                    query,
                    max_results=max_results,
                )

                for item in search_results:
                    results.append(
                        {
                            "title": item.get(
                                "title"
                            ),
                            "url": item.get(
                                "href"
                            ),
                            "snippet": item.get(
                                "body"
                            ),
                        }
                    )

            return ToolResult.ok(
                self.name,
                results,
            )

        except Exception as error:
            return ToolResult.fail(
                self.name,
                error,
            )
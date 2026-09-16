"""
ARES Document Search
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import Document


@dataclass
class SearchMatch:

    line_number: int

    text: str

    score: int

    def to_dict(self):

        return {
            "line_number":
                self.line_number,

            "text":
                self.text,

            "score":
                self.score,
        }


def search_document(
    document: Document,
    query: str,
    max_results: int = 10,
) -> list[SearchMatch]:

    query = query.strip().lower()

    if not query:

        return []

    matches = []

    for index, line in enumerate(
        document.content.splitlines(),
        start=1,
    ):

        lower_line = line.lower()

        if query in lower_line:

            score = lower_line.count(
                query
            )

            matches.append(
                SearchMatch(
                    line_number=index,
                    text=line,
                    score=score,
                )
            )

    matches.sort(
        key=lambda item: item.score,
        reverse=True,
    )

    return matches[:max_results]
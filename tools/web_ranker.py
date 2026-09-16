"""
ARES Web Result Ranker

Lightweight ranking before we eventually add
LLM/semantic ranking.
"""

from __future__ import annotations

import re

from .web_result import WebResult


class WebRanker:

    def rank(
        self,
        query: str,
        results: list[WebResult],
    ) -> list[WebResult]:

        query_words = set(
            self._words(query)
        )

        for result in results:

            text = (
                result.title
                + " "
                + result.snippet
            ).lower()

            result_words = set(
                self._words(text)
            )

            overlap = (
                query_words
                & result_words
            )

            result.score = (
                len(overlap)
                / max(
                    len(query_words),
                    1,
                )
            )

        results.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return results

    @staticmethod
    def _words(text: str):

        return re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text.lower(),
        )
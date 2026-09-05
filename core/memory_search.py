"""
ARES Memory Search
Step 157

Lightweight keyword retrieval.

No embeddings.
No vector database.
No large dependencies.

This keeps ARES disk-friendly while establishing
the retrieval interface that can later support
semantic/vector search.
"""

from __future__ import annotations

import re
from typing import Any


class MemorySearch:

    def __init__(self, memory_store):

        self.memory_store = memory_store

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        query = query.strip().lower()

        if not query:
            return []

        query_words = self._tokenize(query)

        results = []

        for memory in self.memory_store.all():

            content = str(
                memory.get("content", "")
            ).lower()

            memory_words = self._tokenize(content)

            if not memory_words:
                continue

            overlap = (
                query_words & memory_words
            )

            if not overlap:
                continue

            score = (
                len(overlap)
                / max(len(query_words), 1)
            )

            score += (
                float(
                    memory.get(
                        "importance",
                        0.5,
                    )
                )
                * 0.25
            )

            results.append(
                {
                    "memory": memory,
                    "score": score,
                }
            )

        results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        selected = results[:limit]

        for item in selected:

            self.memory_store.touch(
                item["memory"]["id"]
            )

        return selected

    @staticmethod
    def _tokenize(text: str) -> set[str]:

        words = re.findall(
            r"\b[a-zA-Z0-9_]+\b",
            text.lower(),
        )

        return set(words)
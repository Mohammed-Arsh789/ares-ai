"""
ARES Unified Web Response

A predictable structure for the frontend,
brain and future agents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WebResponse:

    query: str

    success: bool

    results: list[dict[str, Any]] = field(
        default_factory=list
    )

    sources: list[dict[str, Any]] = field(
        default_factory=list
    )

    error: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self):

        return {
            "query": self.query,
            "success": self.success,
            "results": self.results,
            "sources": self.sources,
            "error": self.error,
            "metadata": self.metadata,
        }

    @classmethod
    def failure(
        cls,
        query: str,
        error: str,
    ):

        return cls(
            query=query,
            success=False,
            error=error,
        )
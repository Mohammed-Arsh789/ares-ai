"""
ARES Web Result Model
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WebResult:

    title: str

    url: str

    snippet: str = ""

    score: float = 0.0

    source: str = "web"

    def to_dict(self):

        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "score": self.score,
            "source": self.source,
        }
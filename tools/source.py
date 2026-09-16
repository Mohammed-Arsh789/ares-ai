"""
ARES Source Model
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Source:

    title: str

    url: str

    snippet: str = ""

    source_type: str = "web"

    def to_dict(self):

        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source_type":
                self.source_type,
        }
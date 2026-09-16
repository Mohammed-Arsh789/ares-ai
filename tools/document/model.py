"""
ARES Document Model

Common representation for documents regardless
of their original file format.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:

    name: str

    path: str

    extension: str

    content: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    pages: int | None = None

    word_count: int = 0

    character_count: int = 0

    def __post_init__(self):

        self.word_count = len(
            self.content.split()
        )

        self.character_count = len(
            self.content
        )

    def to_dict(self):

        return {
            "name": self.name,
            "path": self.path,
            "extension": self.extension,
            "content": self.content,
            "metadata": self.metadata,
            "pages": self.pages,
            "word_count": self.word_count,
            "character_count":
                self.character_count,
        }
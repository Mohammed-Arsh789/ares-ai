"""
ARES Document Analyzer
"""

from __future__ import annotations

import re

from .model import Document


class DocumentAnalyzer:

    def analyze(
        self,
        document: Document,
    ) -> dict:

        text = document.content

        sentences = [
            sentence.strip()
            for sentence in re.split(
                r"[.!?]+",
                text,
            )
            if sentence.strip()
        ]

        return {
            "name":
                document.name,

            "format":
                document.extension,

            "characters":
                len(text),

            "words":
                len(text.split()),

            "lines":
                len(
                    text.splitlines()
                ),

            "sentences":
                len(sentences),

            "pages":
                document.pages,

            "size_bytes":
                document.metadata.get(
                    "size_bytes",
                    0,
                ),
        }
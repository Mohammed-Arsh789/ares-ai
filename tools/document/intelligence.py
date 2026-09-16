"""
ARES Document Intelligence

High-level document interface.
"""

from __future__ import annotations

from .analyzer import DocumentAnalyzer
from .model import Document
from .reader import DocumentReader
from .search import search_document


class DocumentIntelligence:

    def __init__(self):

        self.reader = DocumentReader()

        self.analyzer = (
            DocumentAnalyzer()
        )

    def load(
        self,
        path: str,
    ) -> Document:

        return self.reader.read(
            path
        )

    def analyze(
        self,
        document: Document,
    ) -> dict:

        return self.analyzer.analyze(
            document
        )

    def search(
        self,
        document: Document,
        query: str,
        max_results: int = 10,
    ):

        return search_document(
            document,
            query,
            max_results,
        )

    def inspect(
        self,
        path: str,
    ) -> dict:

        document = self.load(
            path
        )

        return {
            "document":
                document.to_dict(),

            "analysis":
                self.analyze(
                    document
                ),
        }
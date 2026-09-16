"""
ARES Document Intelligence Package
"""

from .analyzer import DocumentAnalyzer
from .intelligence import DocumentIntelligence
from .model import Document
from .reader import DocumentReader
from .search import SearchMatch, search_document


__all__ = [
    "Document",
    "DocumentReader",
    "DocumentAnalyzer",
    "DocumentIntelligence",
    "SearchMatch",
    "search_document",
]
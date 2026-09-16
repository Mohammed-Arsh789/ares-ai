"""
ARES Web Query Classification

Determines whether a request looks like:
- a normal search
- a current-information request
- a direct URL request
"""

from __future__ import annotations

from enum import Enum
from urllib.parse import urlparse


class WebQueryType(str, Enum):

    SEARCH = "search"

    URL = "url"

    CURRENT = "current"


def classify_web_query(
    query: str,
) -> WebQueryType:

    query = query.strip()

    if not query:
        return WebQueryType.SEARCH

    parsed = urlparse(query)

    if (
        parsed.scheme.lower()
        in {"http", "https"}
        and parsed.netloc
    ):

        return WebQueryType.URL

    lowered = query.lower()

    current_terms = (
        "latest",
        "today",
        "current",
        "recent",
        "news",
        "right now",
        "this week",
    )

    if any(
        term in lowered
        for term in current_terms
    ):

        return WebQueryType.CURRENT

    return WebQueryType.SEARCH
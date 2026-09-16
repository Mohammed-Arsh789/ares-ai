"""
ARES Web Configuration
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class WebConfig:

    timeout_seconds: float = 10.0

    max_results: int = 5

    max_content_chars: int = 20000

    max_snippet_chars: int = 500

    max_url_length: int = 2048

    user_agent: str = (
        "ARES/0.1 "
        "Public Web Intelligence Client"
    )
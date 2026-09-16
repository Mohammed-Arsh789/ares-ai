"""
ARES Voice Models
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Transcript:
    text: str
    language: str = "unknown"
    confidence: float | None = None
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(
                timezone.utc
            ).isoformat()

    def to_dict(self):
        return {
            "text": self.text,
            "language": self.language,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
        }
"""
ARES Context Engine Foundation
Step 159
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ContextItem:

    role: str
    content: str
    timestamp: str = field(
        default_factory=lambda:
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


class ContextManager:

    def __init__(
        self,
        max_items: int = 20,
    ):

        self.max_items = max_items
        self.items: list[ContextItem] = []

    def add(
        self,
        role: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ):

        self.items.append(
            ContextItem(
                role=role,
                content=content,
                metadata=metadata or {},
            )
        )

        self._trim()

    def _trim(self):

        if len(self.items) > self.max_items:

            excess = (
                len(self.items)
                - self.max_items
            )

            del self.items[:excess]

    def recent(
        self,
        limit: int | None = None,
    ):

        if limit is None:
            return list(self.items)

        return self.items[-limit:]

    def clear(self):

        self.items.clear()

    def as_messages(self):

        return [
            {
                "role": item.role,
                "content": item.content,
            }
            for item in self.items
        ]
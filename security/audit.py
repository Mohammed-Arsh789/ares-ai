"""
ARES Security Audit Log
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class AuditLogger:

    def __init__(self):

        self.events: list[
            dict[str, Any]
        ] = []

    def record(
        self,
        event: str,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        entry = {
            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "event":
                event,

            "details":
                details or {},
        }

        self.events.append(entry)

        return entry

    def list_events(self):

        return list(self.events)

    def clear(self):

        self.events.clear()
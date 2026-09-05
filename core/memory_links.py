"""
ARES Linked Memory Foundation
Step 163
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class MemoryLinks:

    def __init__(self, memory_store):

        self.memory_store = memory_store

    def link(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        strength: float = 1.0,
    ) -> bool:

        source = self.memory_store.get(
            source_id
        )

        target = self.memory_store.get(
            target_id
        )

        if source is None or target is None:
            return False

        links = source.setdefault(
            "links",
            []
        )

        for link in links:

            if (
                link.get("target_id")
                == target_id
                and link.get("relation")
                == relation
            ):
                return True

        links.append(
            {
                "target_id": target_id,
                "relation": relation,
                "strength": max(
                    0.0,
                    min(1.0, strength),
                ),
                "created_at":
                    datetime.now(
                        timezone.utc
                    ).isoformat(),
            }
        )

        self.memory_store._atomic_write()

        return True

    def related(
        self,
        memory_id: str,
    ) -> list[dict[str, Any]]:

        memory = self.memory_store.get(
            memory_id
        )

        if memory is None:
            return []

        return memory.get(
            "links",
            []
        )
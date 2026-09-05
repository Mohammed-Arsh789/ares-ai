"""
ARES Memory Manager
Step 152

Higher-level interface around MemoryStore.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .memory_store import MemoryStore


class MemoryManager:

    def __init__(
        self,
        file_path: str | Path = "memory.json",
    ):
        self.store = MemoryStore(file_path)

    def remember(
        self,
        content: str,
        memory_type: str = "general",
        importance: float = 0.5,
        source: str = "user",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        return self.store.add(
            content=content,
            memory_type=memory_type,
            importance=importance,
            source=source,
            metadata=metadata,
        )

    def forget(self, memory_id: str) -> bool:

        return self.store.delete(memory_id)

    def get(self, memory_id: str):

        return self.store.get(memory_id)

    def all(self):

        return self.store.all()

    def stats(self):

        return self.store.stats()

    def update(
        self,
        memory_id: str,
        **changes: Any,
    ):

        return self.store.update(
            memory_id,
            **changes,
        )
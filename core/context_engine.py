"""
ARES Context Engine
Step 160

Combines short-term conversation context
with relevant long-term memories.
"""

from __future__ import annotations

from .context import ContextManager
from .memory_manager import MemoryManager
from .memory_search import MemorySearch


class ContextEngine:

    def __init__(
        self,
        memory_manager: MemoryManager,
        max_recent_messages: int = 12,
    ):

        self.memory = memory_manager

        self.context = ContextManager(
            max_items=max_recent_messages
        )

        self.search = MemorySearch(
            self.memory.store
        )

    def add_user_message(
        self,
        content: str,
    ):

        self.context.add(
            role="user",
            content=content,
        )

    def add_assistant_message(
        self,
        content: str,
    ):

        self.context.add(
            role="assistant",
            content=content,
        )

    def build(
        self,
        query: str,
    ) -> dict:

        memories = self.search.search(
            query,
            limit=5,
        )

        return {
            "recent_messages": (
                self.context.as_messages()
            ),
            "relevant_memories": memories,
        }

    def clear_conversation(self):

        self.context.clear()
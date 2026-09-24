from __future__ import annotations

from core.cognitive_context import CognitiveContext
from core.context_manager import ContextManager
from core.memory_bridge import MemoryBridge


class FakeMemory:
    def search(
        self,
        query: str,
        limit: int = 8,
    ):
        return [
            {
                "content": "User likes F1."
            },
            {
                "content": "User is building ARES."
            },
        ]


class FakeConversation:
    def recent(
        self,
        limit: int = 10,
    ):
        return [
            {
                "role": "user",
                "content": "We are working on ARES.",
            }
        ]


class FakeRegistry:
    def names(self):
        return [
            "calculator",
            "weather",
            "web_search",
        ]


class FakeWritableMemory:
    def __init__(self):
        self.entries = []

    def store(self, entry):
        self.entries.append(entry)


def test_cognitive_context_serializes():
    context = CognitiveContext(
        user_input="hello",
        memories=[
            {
                "content": "test memory"
            }
        ],
    )

    data = context.to_dict()

    assert data["user_input"] == "hello"
    assert len(data["memories"]) == 1


def test_context_manager_collects_context():
    manager = ContextManager(
        memory=FakeMemory(),
        conversation=FakeConversation(),
        tool_registry=FakeRegistry(),
    )

    context = manager.build(
        "what are we working on?"
    )

    assert len(
        context.memories
    ) == 2

    assert len(
        context.recent_messages
    ) == 1

    assert "calculator" in (
        context.available_tools
    )


def test_memory_bridge_stores_interaction():
    memory = FakeWritableMemory()

    bridge = MemoryBridge(
        memory=memory
    )

    stored = bridge.remember(
        user_input="hello",
        response="Hi!",
    )

    assert stored
    assert len(
        memory.entries
    ) == 1

    assert (
        memory.entries[0]["user_input"]
        == "hello"
    )


def test_context_limits_memories():
    manager = ContextManager(
        memory=FakeMemory(),
        max_memories=1,
    )

    context = manager.build(
        "test"
    )

    assert len(
        context.memories
    ) == 1
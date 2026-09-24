from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class CognitiveContext:
    """
    Information supplied to the Cognitive Core for one turn.

    This combines immediate context, conversation context,
    retrieved long-term memory, and available capabilities.
    """

    user_input: str

    recent_messages: list[dict[str, Any]] = field(
        default_factory=list
    )

    memories: list[dict[str, Any]] = field(
        default_factory=list
    )

    session_context: dict[str, Any] = field(
        default_factory=dict
    )

    intent: Any = None

    available_tools: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the cognitive context into a serializable
        dictionary for the model layer.
        """

        return asdict(self)

    def add_memory(
        self,
        memory: dict[str, Any],
    ) -> None:
        """
        Add one retrieved memory.
        """

        if isinstance(memory, dict):
            self.memories.append(memory)

    def add_message(
        self,
        role: str,
        content: str,
    ) -> None:
        """
        Add a conversation message.
        """

        self.recent_messages.append(
            {
                "role": role,
                "content": content,
            }
        )
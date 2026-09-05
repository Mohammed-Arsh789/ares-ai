"""
ARES Intent System
Step 166

Defines the structured representation of a user's intent.

This layer deliberately does not execute anything.
It only describes what ARES believes the user wants.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class IntentType(str, Enum):

    CHAT = "chat"

    QUESTION = "question"

    SEARCH = "search"

    WEATHER = "weather"

    FILE_OPERATION = "file_operation"

    APPLICATION = "application"

    CODING = "coding"

    VISION = "vision"

    VOICE = "voice"

    AUTOMATION = "automation"

    STUDY = "study"

    RESEARCH = "research"

    WRITING = "writing"

    ANALYSIS = "analysis"

    SYSTEM = "system"

    UNKNOWN = "unknown"


@dataclass
class Intent:

    type: IntentType

    confidence: float

    raw_input: str

    entities: dict[str, Any] = field(
        default_factory=dict
    )

    requires_tool: bool = False

    requires_confirmation: bool = False

    reason: str = ""

    def to_dict(self) -> dict[str, Any]:

        return {
            "type": self.type.value,
            "confidence": self.confidence,
            "raw_input": self.raw_input,
            "entities": self.entities,
            "requires_tool":
                self.requires_tool,
            "requires_confirmation":
                self.requires_confirmation,
            "reason": self.reason,
        }
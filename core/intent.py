from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class IntentName(str, Enum):
    CONVERSATION = "conversation"
    CALCULATOR = "calculator"
    MEMORY_STORE = "memory_store"
    MEMORY_SEARCH = "memory_search"
    WEATHER = "weather"
    WEB_SEARCH = "web_search"
    WEB_FETCH = "web_fetch"
    OPEN_APP = "open_app"
    FILE_OPERATION = "file_operation"
    DOCUMENT_ANALYSIS = "document_analysis"
    VISION = "vision"
    CODING = "coding"
    RESEARCH = "research"
    STUDY = "study"
    REVIEW = "review"
    AUTOMATION = "automation"
    WORKSPACE = "workspace"
    PLUGIN = "plugin"
    HELP = "help"
    UNKNOWN = "unknown"


# Backward compatibility for older code
IntentType = IntentName


@dataclass
class Intent:
    """
    Structured representation of what the user wants ARES to do.
    """

    name: IntentName | str
    confidence: float = 0.0
    raw_text: str = ""
    entities: Dict[str, Any] = field(default_factory=dict)
    requires_tool: bool = False
    requires_confirmation: bool = False
    target: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if isinstance(self.name, str):
            try:
                self.name = IntentName(self.name.lower())
            except ValueError:
                self.name = IntentName.UNKNOWN

        self.confidence = max(0.0, min(1.0, float(self.confidence)))

        if self.target and "target" not in self.entities:
            self.entities["target"] = self.target

    @property
    def value(self) -> str:
        return self.name.value

    @property
    def intent(self) -> str:
        return self.name.value

    def is_name(self, value: IntentName | str) -> bool:
        if isinstance(value, IntentName):
            return self.name == value

        return self.name.value == str(value).lower()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name.value,
            "confidence": self.confidence,
            "raw_text": self.raw_text,
            "entities": dict(self.entities),
            "requires_tool": self.requires_tool,
            "requires_confirmation": self.requires_confirmation,
            "target": self.target,
            "metadata": dict(self.metadata),
        }

    def __str__(self) -> str:
        return self.name.value

    def __repr__(self) -> str:
        return (
            f"Intent(name={self.name.value!r}, "
            f"confidence={self.confidence:.2f}, "
            f"entities={self.entities!r})"
        )
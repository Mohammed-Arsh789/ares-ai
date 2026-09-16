"""
ARES Action Request

Represents a proposed operation before execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ActionRequest:

    tool: str

    action: str

    arguments: dict[str, Any] = field(
        default_factory=dict
    )

    reason: str = ""

    source: str = "ares"

    def to_dict(self):

        return {
            "tool": self.tool,
            "action": self.action,
            "arguments": self.arguments,
            "reason": self.reason,
            "source": self.source,
        }
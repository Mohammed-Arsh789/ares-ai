"""
ARES Tool Interface

All executable ARES capabilities must implement this interface.

A tool is:
    registered
    described
    permission-checked
    executed
    wrapped in ToolResult
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):

    name: str = "unnamed"

    description: str = ""

    dangerous: bool = False

    requires_confirmation: bool = False

    @abstractmethod
    def run(
        self,
        **kwargs: Any,
    ) -> Any:
        """
        Execute the tool.

        Concrete tools implement this method.
        """

        raise NotImplementedError

    def describe(self) -> dict[str, Any]:

        return {
            "name": self.name,
            "description": self.description,
            "dangerous": self.dangerous,
            "requires_confirmation":
                self.requires_confirmation,
        }
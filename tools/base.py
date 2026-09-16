"""
ARES Universal Tool Contract.

Every ARES tool must follow this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """
    Canonical interface for every ARES tool.

    Tools must:
    - Have a unique name
    - Have a description
    - Implement run()
    """

    name: str = "unnamed_tool"
    description: str = "No description provided."
    dangerous: bool = False
    requires_confirmation: bool = False

    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        """
        Execute the tool.
        """
        raise NotImplementedError

    def execute(self, **kwargs: Any) -> Any:
        """
        Compatibility alias.

        Older code may call execute(), while the official API
        uses run().
        """
        return self.run(**kwargs)

    def describe(self) -> dict[str, Any]:
        """
        Return machine-readable tool metadata.
        """
        return {
            "name": self.name,
            "description": self.description,
            "dangerous": self.dangerous,
            "requires_confirmation": self.requires_confirmation,
        }

    def __repr__(self) -> str:
        return f"<Tool name={self.name!r}>"
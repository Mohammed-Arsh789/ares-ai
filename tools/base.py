"""
ARES Tool Interface
Step 173

Every ARES tool will eventually implement this interface.

Tools must be explicitly registered.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):

    name: str = "unnamed"

    description: str = ""

    dangerous: bool = False

    @abstractmethod
    def execute(
        self,
        **kwargs: Any,
    ) -> Any:
        """
        Execute the tool.

        Concrete tools must implement this.
        """
        raise NotImplementedError

    def describe(self) -> dict[str, Any]:

        return {
            "name": self.name,
            "description": self.description,
            "dangerous": self.dangerous,
        }
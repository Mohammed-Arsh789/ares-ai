"""
ARES Tool Registry
Step 174
"""

from __future__ import annotations

from typing import Any

from .base import Tool


class ToolRegistry:

    def __init__(self):

        self._tools: dict[str, Tool] = {}

    def register(
        self,
        tool: Tool,
    ) -> None:

        if not isinstance(tool, Tool):

            raise TypeError(
                "Only Tool instances can be registered."
            )

        if not tool.name:

            raise ValueError(
                "Tool must have a name."
            )

        if tool.name in self._tools:

            raise ValueError(
                f"Tool already registered: {tool.name}"
            )

        self._tools[tool.name] = tool

    def get(
        self,
        name: str,
    ) -> Tool | None:

        return self._tools.get(name)

    def has(
        self,
        name: str,
    ) -> bool:

        return name in self._tools

    def list_tools(
        self,
    ) -> list[dict[str, Any]]:

        return [
            tool.describe()
            for tool in self._tools.values()
        ]

    def names(self) -> list[str]:

        return list(self._tools.keys())
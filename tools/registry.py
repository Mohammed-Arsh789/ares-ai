"""
ARES Tool Registry

Single source of truth for registered tools.
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

        name = tool.name.strip()

        if not name:

            raise ValueError(
                "Tool must have a non-empty name."
            )

        if name in self._tools:

            raise ValueError(
                f"Tool already registered: {name}"
            )

        self._tools[name] = tool

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

    def names(self) -> list[str]:

        return list(self._tools.keys())

    def list_tools(self) -> list[dict[str, Any]]:

        return [
            tool.describe()
            for tool in self._tools.values()
        ]

    def descriptions(self) -> dict[str, str]:

        return {
            name: tool.description
            for name, tool in self._tools.items()
        }
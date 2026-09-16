"""
Canonical ARES Tool Registry.

Supports:
- Tool objects
- Legacy function registration
- Safe lookup
- Standard execution
"""

from __future__ import annotations

from typing import Any, Iterable, Optional

from .base import Tool
from .adapters import FunctionTool
from .result import ToolResult


class ToolRegistry:
    """
    Central registry for all ARES tools.
    """

    def __init__(self, tools: Optional[Iterable[Tool]] = None):
        self._tools: dict[str, Tool] = {}

        if tools:
            for tool in tools:
                self.register(tool)

    def register(
        self,
        tool_or_name: Tool | str,
        description: Optional[str] = None,
        function: Any = None,
    ) -> Tool:
        """
        Register either:

        registry.register(tool_object)

        or legacy:

        registry.register("calculator", "Description", calculate)
        """

        if isinstance(tool_or_name, Tool):
            tool = tool_or_name

        elif isinstance(tool_or_name, str):
            if function is None:
                raise TypeError(
                    "Legacy registration requires a function argument."
                )

            tool = FunctionTool(
                name=tool_or_name,
                description=description or "",
                function=function,
            )

        else:
            raise TypeError(
                "register() expects a Tool object or tool name string."
            )

        if not tool.name:
            raise ValueError("Tool must have a non-empty name.")

        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")

        self._tools[tool.name] = tool
        return tool

    def unregister(self, name: str) -> bool:
        return self._tools.pop(name, None) is not None

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")

        return self._tools[name]

    def has(self, name: str) -> bool:
        return name in self._tools

    def names(self) -> list[str]:
        return list(self._tools.keys())

    def list_tools(self) -> list[str]:
        return self.names()

    def descriptions(self) -> dict[str, str]:
        return {
            name: tool.description
            for name, tool in self._tools.items()
        }

    def execute(self, name: str, **kwargs: Any) -> Any:
        """
        Execute a tool.

        Existing code expects raw values, so this method returns
        the underlying tool output rather than forcing ToolResult
        on legacy callers.
        """
        tool = self.get(name)

        try:
            return tool.run(**kwargs)
        except Exception as error:
            raise RuntimeError(
                f"Tool '{name}' failed: {error}"
            ) from error

    def execute_result(self, name: str, **kwargs: Any) -> ToolResult:
        """
        Execute a tool and always return ToolResult.
        """
        tool = self.get(name)

        try:
            output = tool.run(**kwargs)

            if isinstance(output, ToolResult):
                return output

            return ToolResult.ok(name, output)

        except Exception as error:
            return ToolResult.fail(name, str(error))

    def clear(self) -> None:
        self._tools.clear()

    def __len__(self) -> int:
        return len(self._tools)

    def __contains__(self, name: str) -> bool:
        return self.has(name)

    def __repr__(self) -> str:
        return f"<ToolRegistry tools={self.names()!r}>"
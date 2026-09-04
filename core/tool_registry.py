from typing import Callable, Any


class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, dict[str, Any]] = {}

    def register(
        self,
        name: str,
        description: str,
        function: Callable[..., Any]
    ):
        """Register a tool with its name, description, and function."""

        self.tools[name] = {
            "description": description,
            "function": function,
        }

    def execute(self, tool_name: str, **kwargs):
        """Execute a registered tool."""

        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        function = self.tools[tool_name]["function"]

        return function(**kwargs)

    def has(self, tool_name: str) -> bool:
        """Check whether a tool is registered."""

        return tool_name in self.tools

    def list_tools(self) -> list[str]:
        """Return the names of all registered tools."""

        return list(self.tools.keys())

    def get_description(self, tool_name: str) -> str:
        """Return a tool's description."""

        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        return self.tools[tool_name]["description"]

    def get_tools(self) -> dict[str, dict[str, Any]]:
        """Return all registered tools."""

        return self.tools
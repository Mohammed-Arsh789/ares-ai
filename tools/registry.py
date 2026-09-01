from tools.base import Tool


class ToolRegistry:
    """
    Central registry for ARES tools.
    """

    def __init__(self):
        self._tools = {}

    def register(self, tool: Tool):
        if not isinstance(tool, Tool):
            raise TypeError("Tool must inherit from Tool.")

        self._tools[tool.name] = tool

    def get(self, name: str):
        return self._tools.get(name)

    def has(self, name: str) -> bool:
        return name in self._tools

    def list_tools(self):
        return list(self._tools.values())

    def descriptions(self):
        return {
            tool.name: tool.description
            for tool in self._tools.values()
        }
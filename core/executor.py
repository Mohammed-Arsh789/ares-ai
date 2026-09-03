from core.permissions import PermissionManager
from tools.result import ToolResult


class ToolExecutor:
    def __init__(self, manager):
        self.manager = manager
        self.permissions = PermissionManager()

    def execute(
        self,
        tool_name,
        arguments,
    ):
        if not self.manager.has(tool_name):
            return ToolResult.fail(
                tool_name,
                "Tool is not registered.",
            )

        tool = self.manager.get(
            tool_name
        )

        try:
            result = tool.run(
                **arguments
            )

            if isinstance(
                result,
                ToolResult,
            ):
                return result

            return ToolResult.ok(
                tool_name,
                result,
            )

        except Exception as error:
            return ToolResult.fail(
                tool_name,
                error,
            )
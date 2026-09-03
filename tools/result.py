from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    success: bool
    data: Any = None
    error: str | None = None
    tool: str | None = None

    def to_dict(self):
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "tool": self.tool,
        }

    @classmethod
    def ok(cls, tool, data):
        return cls(
            success=True,
            data=data,
            tool=tool,
        )

    @classmethod
    def fail(cls, tool, error):
        return cls(
            success=False,
            error=str(error),
            tool=tool,
        )
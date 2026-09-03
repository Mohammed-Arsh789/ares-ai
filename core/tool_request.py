from dataclasses import dataclass
from typing import Any


@dataclass
class ToolRequest:
    tool: str
    arguments: dict[str, Any]

    def is_valid(self):
        return bool(
            self.tool
            and isinstance(
                self.arguments,
                dict,
            )
        )
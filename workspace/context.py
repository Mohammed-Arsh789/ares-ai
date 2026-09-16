"""
ARES Workspace Context

Stores temporary context associated with a workspace.
"""

from __future__ import annotations

from typing import Any


class WorkspaceContext:

    def __init__(self):
        self.data: dict[str, Any] = {}

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.data[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.data.get(
            key,
            default,
        )

    def remove(
        self,
        key: str,
    ) -> None:

        self.data.pop(
            key,
            None,
        )

    def clear(self) -> None:

        self.data.clear()

    def snapshot(self) -> dict[str, Any]:

        return dict(self.data)
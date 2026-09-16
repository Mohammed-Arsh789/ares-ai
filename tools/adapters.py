"""
Adapters allowing old function-style tools to use the universal Tool API.
"""

from __future__ import annotations

from typing import Any, Callable

from .base import Tool


class FunctionTool(Tool):
    """
    Wraps a normal Python function as a canonical ARES Tool.
    """

    def __init__(
        self,
        name: str,
        description: str,
        function: Callable[..., Any],
        dangerous: bool = False,
        requires_confirmation: bool = False,
    ):
        self.name = name
        self.description = description
        self.function = function
        self.dangerous = dangerous
        self.requires_confirmation = requires_confirmation

    def run(self, **kwargs: Any) -> Any:
        return self.function(**kwargs)
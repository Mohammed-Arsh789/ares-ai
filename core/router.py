"""
ARES Intelligent Router
Step 177
"""

from __future__ import annotations

from .intent import Intent
from .planner import Planner
from tools.registry import ToolRegistry


class Router:

    def __init__(
        self,
        registry: ToolRegistry,
    ):

        self.registry = registry

        self.planner = Planner()

    def route(
        self,
        user_input: str,
        intent: Intent,
    ):

        task = self.planner.create_plan(
            user_input,
            intent,
        )

        return task

    def available_tools(self):

        return self.registry.list_tools()
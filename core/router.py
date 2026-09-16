"""
ARES Intelligent Router

Compatibility-first routing layer.

Supports:

1. Legacy interface:
       router = Router()
       router.route("calculate 5 + 5")
       -> "calculator"

2. Registry-aware interface:
       router = Router(registry)
       router.available_tools()

3. Planning interface:
       router.route(message, intent)
       -> planner-generated plan
"""

from __future__ import annotations

from typing import Any, Optional

from .planner import Planner


class Router:
    """
    Routes user requests to legacy route names or planner-generated plans.

    The router deliberately preserves compatibility with the existing
    ARES brain interface while supporting the newer planning architecture.
    """

    def __init__(self, registry: Optional[Any] = None):
        self.registry = registry
        self.planner = Planner()

    def route(
        self,
        user_input: str,
        intent: Optional[Any] = None,
    ) -> Any:
        """
        Route a user request.

        Legacy examples:

            route("calculate 5 + 5")
            -> "calculator"

            route("remember I like F1")
            -> "memory"

            route("what is the weather")
            -> "weather"

        Planning example:

            route("some request", intent)
            -> planner-created plan
        """

        if not isinstance(user_input, str):
            raise TypeError("user_input must be a string.")

        text = user_input.strip()

        if not text:
            return "conversation"

        lowered = text.lower()

        # ---------------------------------------------------------
        # Calculator
        # ---------------------------------------------------------
        if lowered.startswith(("calculate ", "calc ")):
            return "calculator"

        # ---------------------------------------------------------
        # Memory write
        # ---------------------------------------------------------
        if lowered.startswith("remember "):
            return "memory"

        # ---------------------------------------------------------
        # Memory search
        # ---------------------------------------------------------
        memory_queries = (
            "what do you remember",
            "what do you know about me",
            "show my memories",
            "recall my memories",
            "list memories",
        )

        if any(phrase in lowered for phrase in memory_queries):
            return "memory_search"

        # ---------------------------------------------------------
        # Weather
        # ---------------------------------------------------------
        weather_keywords = (
            "weather",
            "temperature outside",
            "forecast",
            "is it raining",
            "how hot is it",
            "how cold is it",
        )

        if any(keyword in lowered for keyword in weather_keywords):
            return "weather"

        # ---------------------------------------------------------
        # Application launching
        # ---------------------------------------------------------
        if lowered.startswith(("open ", "launch ", "start ")):
            return "open_app"

        # ---------------------------------------------------------
        # Help
        # ---------------------------------------------------------
        if lowered in {
            "help",
            "commands",
            "what can you do",
        }:
            return "help"

        # ---------------------------------------------------------
        # New planning system
        # ---------------------------------------------------------
        if intent is not None:
            return self.planner.create_plan(text, intent)

        # ---------------------------------------------------------
        # Default conversational route
        # ---------------------------------------------------------
        return "conversation"

    def available_tools(self) -> list[Any]:
        """
        Return available tools from the attached registry.

        Supports registries exposing either:

            list_tools()

        or:

            names()
        """

        if self.registry is None:
            return []

        list_tools = getattr(self.registry, "list_tools", None)

        if callable(list_tools):
            return list_tools()

        names = getattr(self.registry, "names", None)

        if callable(names):
            return names()

        return []
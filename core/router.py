from __future__ import annotations

from typing import Any, Optional

from .intent import Intent, IntentName
from .intent_detector import IntentDetector


class Router:
    """
    ARES routing layer.

    User input
        ↓
    IntentDetector
        ↓
    Intent
        ↓
    Stable route
    """

    def __init__(
        self,
        registry: Optional[Any] = None,
        intent_detector: Optional[IntentDetector] = None,
    ) -> None:
        self.registry = registry
        self.intent_detector = intent_detector or IntentDetector()

    def detect_intent(self, user_input: str) -> Intent:
        """
        Return the complete structured Intent.
        """
        return self.intent_detector.detect(user_input)

    def route(
        self,
        user_input: str,
        intent: Optional[Any] = None,
    ) -> str:
        """
        Convert an Intent into the route expected by ARES.
        """

        if isinstance(intent, Intent):
            detected = intent

        elif intent is not None:
            try:
                detected = Intent(
                    name=intent,
                    raw_text=user_input,
                )
            except Exception:
                detected = self.detect_intent(user_input)

        else:
            detected = self.detect_intent(user_input)

        route_map = {
            IntentName.CONVERSATION: "conversation",
            IntentName.CALCULATOR: "calculator",
            IntentName.MEMORY_STORE: "memory",
            IntentName.MEMORY_SEARCH: "memory_search",
            IntentName.WEATHER: "weather",
            IntentName.WEB_SEARCH: "web_search",
            IntentName.WEB_FETCH: "web_fetch",
            IntentName.OPEN_APP: "open_app",
            IntentName.FILE_OPERATION: "file_operation",
            IntentName.DOCUMENT_ANALYSIS: "document_analysis",
            IntentName.VISION: "vision",
            IntentName.CODING: "coding",
            IntentName.RESEARCH: "research",
            IntentName.STUDY: "study",
            IntentName.REVIEW: "review",
            IntentName.AUTOMATION: "automation",
            IntentName.WORKSPACE: "workspace",
            IntentName.PLUGIN: "plugin",
            IntentName.HELP: "help",
            IntentName.UNKNOWN: "conversation",
        }

        return route_map.get(
            detected.name,
            "conversation",
        )

    def route_intent(self, user_input: str) -> Intent:
        """
        Structured routing API for newer ARES components.
        """
        return self.detect_intent(user_input)

    def available_tools(self) -> list[str]:
        """
        Return registered tool names if a registry is attached.
        """

        if self.registry is None:
            return []

        if hasattr(self.registry, "names"):
            return list(self.registry.names())

        if hasattr(self.registry, "list_tools"):
            tools = self.registry.list_tools()

            result = []

            for item in tools:
                if isinstance(item, dict):
                    result.append(
                        item.get("name", str(item))
                    )
                else:
                    result.append(str(item))

            return result

        return []
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from .intent import Intent, IntentName
from .task import Plan, Task


class Planner:
    """
    Deterministic foundation planner for ARES.

    This is intentionally not an LLM planner yet.

    The architecture is:

        user request
            ↓
        IntentDetector
            ↓
        Planner
            ↓
        Plan
            ↓
        TaskGraph
            ↓
        Orchestrator

    Later, an LLM can propose plans, but the resulting plan must still
    pass through validation before execution.
    """

    def __init__(self, registry=None):
        self.registry = registry

    def create_plan(
        self,
        user_input: str,
        intent: Optional[Intent] = None,
    ) -> Plan:
        text = (user_input or "").strip()

        if not text:
            raise ValueError("Cannot create a plan from empty input.")

        if intent is None:
            intent = self._detect_intent(text)

        plan = Plan(
            goal=text,
            metadata={
                "intent": getattr(intent, "name", None).value
                if hasattr(getattr(intent, "name", None), "value")
                else str(getattr(intent, "name", "unknown")),
                "planner": "planner_v2",
            },
        )

        intent_name = getattr(intent, "name", None)

        if intent_name == IntentName.CALCULATOR:
            self._plan_calculator(plan, text)

        elif intent_name == IntentName.WEATHER:
            self._plan_weather(plan, text)

        elif intent_name == IntentName.MEMORY_STORE:
            self._plan_memory_store(plan, text)

        elif intent_name == IntentName.MEMORY_SEARCH:
            self._plan_memory_search(plan, text)

        elif intent_name == IntentName.WEB_SEARCH:
            self._plan_web_search(plan, text)

        elif intent_name == IntentName.WEB_FETCH:
            self._plan_web_fetch(plan, text)

        elif intent_name == IntentName.OPEN_APP:
            self._plan_open_app(plan, text)

        elif intent_name == IntentName.FILE_OPERATION:
            self._plan_file_operation(plan, text)

        elif intent_name == IntentName.DOCUMENT_ANALYSIS:
            self._plan_document(plan, text)

        elif intent_name == IntentName.VISION:
            self._plan_vision(plan, text)

        elif intent_name == IntentName.CODING:
            self._plan_agent(plan, text, "coding")

        elif intent_name == IntentName.RESEARCH:
            self._plan_agent(plan, text, "research")

        elif intent_name == IntentName.STUDY:
            self._plan_agent(plan, text, "study")

        elif intent_name == IntentName.REVIEW:
            self._plan_agent(plan, text, "review")

        elif intent_name == IntentName.AUTOMATION:
            self._plan_agent(plan, text, "automation")

        elif intent_name == IntentName.WORKSPACE:
            self._plan_agent(plan, text, "workspace")

        elif intent_name == IntentName.PLUGIN:
            self._plan_agent(plan, text, "plugin")

        elif intent_name == IntentName.HELP:
            self._plan_help(plan)

        else:
            self._plan_conversation(plan, text)

        if not plan.tasks:
            self._plan_conversation(plan, text)

        return plan

    # ------------------------------------------------------------------
    # Individual planners
    # ------------------------------------------------------------------

    def _plan_calculator(self, plan: Plan, text: str) -> None:
        expression = self._extract_expression(text)

        plan.add_task(
            Task(
                name="calculate",
                description="Evaluate the requested mathematical expression.",
                tool="calculator",
                arguments={"expression": expression},
            )
        )

    def _plan_weather(self, plan: Plan, text: str) -> None:
        location = self._extract_location(text)

        plan.add_task(
            Task(
                name="get_weather",
                description="Retrieve current weather information.",
                tool="weather",
                arguments={"location": location},
            )
        )

    def _plan_memory_store(self, plan: Plan, text: str) -> None:
        memory_text = self._extract_memory_text(text)

        plan.add_task(
            Task(
                name="store_memory",
                description="Store information in ARES long-term memory.",
                tool="memory_store",
                arguments={"text": memory_text},
            )
        )

    def _plan_memory_search(self, plan: Plan, text: str) -> None:
        query = self._extract_after_keywords(
            text,
            ["remember", "recall", "what do you know about", "what did i say"],
        )

        plan.add_task(
            Task(
                name="search_memory",
                description="Search ARES memory for relevant information.",
                tool="memory_search",
                arguments={"query": query},
            )
        )

    def _plan_web_search(self, plan: Plan, text: str) -> None:
        query = self._extract_after_keywords(
            text,
            ["search for", "search", "look up", "find"],
        )

        plan.add_task(
            Task(
                name="web_search",
                description="Search the web for the requested information.",
                tool="web_search",
                arguments={"query": query},
            )
        )

    def _plan_web_fetch(self, plan: Plan, text: str) -> None:
        url = self._extract_url(text)

        plan.add_task(
            Task(
                name="web_fetch",
                description="Fetch information from the requested URL.",
                tool="web_fetch",
                arguments={"url": url},
            )
        )

    def _plan_open_app(self, plan: Plan, text: str) -> None:
        application = self._extract_application(text)

        plan.add_task(
            Task(
                name="open_application",
                description="Open a supported desktop application.",
                tool="open_app",
                arguments={"application": application},
                requires_confirmation=False,
            )
        )

    def _plan_file_operation(self, plan: Plan, text: str) -> None:
        plan.add_task(
            Task(
                name="file_operation",
                description="Perform the requested file operation.",
                tool="file_operation",
                arguments={"request": text},
                requires_confirmation=True,
            )
        )

    def _plan_document(self, plan: Plan, text: str) -> None:
        plan.add_task(
            Task(
                name="analyze_document",
                description="Analyze the requested document.",
                tool="document_analysis",
                arguments={"request": text},
            )
        )

    def _plan_vision(self, plan: Plan, text: str) -> None:
        plan.add_task(
            Task(
                name="vision_analysis",
                description="Analyze the supplied visual input.",
                tool="vision",
                arguments={"request": text},
            )
        )

    def _plan_agent(
        self,
        plan: Plan,
        text: str,
        agent_name: str,
    ) -> None:
        plan.add_task(
            Task(
                name=f"{agent_name}_task",
                description=f"Delegate the request to the {agent_name} agent.",
                tool=f"agent:{agent_name}",
                arguments={"request": text},
            )
        )

    def _plan_help(self, plan: Plan) -> None:
        plan.add_task(
            Task(
                name="show_help",
                description="Provide information about ARES capabilities.",
                tool="help",
                arguments={},
            )
        )

    def _plan_conversation(self, plan: Plan, text: str) -> None:
        plan.add_task(
            Task(
                name="conversation",
                description="Generate a conversational response.",
                tool="conversation",
                arguments={"message": text},
            )
        )

    # ------------------------------------------------------------------
    # Extraction helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_expression(text: str) -> str:
        patterns = [
            r"(?:calculate|compute|solve|what is)\s+(.+)$",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return match.group(1).strip().rstrip("?.")

        return text.strip()

    @staticmethod
    def _extract_location(text: str) -> str:
        match = re.search(
            r"\b(?:in|at|near)\s+([A-Za-z][A-Za-z .'-]+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1).strip().rstrip("?.")

        return ""

    @staticmethod
    def _extract_memory_text(text: str) -> str:
        patterns = [
            r"remember that\s+(.+)$",
            r"remember\s+(.+)$",
            r"save this(?: that)?\s+(.+)$",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return match.group(1).strip().rstrip(".")

        return text.strip()

    @staticmethod
    def _extract_after_keywords(
        text: str,
        keywords: List[str],
    ) -> str:
        lowered = text.lower()

        for keyword in keywords:
            index = lowered.find(keyword.lower())

            if index >= 0:
                value = text[index + len(keyword):].strip()

                if value:
                    return value.rstrip("?.")

        return text.strip()

    @staticmethod
    def _extract_url(text: str) -> str:
        match = re.search(
            r"https?://[^\s]+",
            text,
            re.IGNORECASE,
        )

        return match.group(0).rstrip(".,)") if match else ""

    @staticmethod
    def _extract_application(text: str) -> str:
        match = re.search(
            r"(?:open|launch|start|run)\s+(.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1).strip().rstrip("?.")

        return text.strip()

    @staticmethod
    def _detect_intent(text: str) -> Any:
        """
        Lazy import prevents unnecessary circular imports.
        """
        from .intent_detector import IntentDetector

        return IntentDetector().detect(text)


# Compatibility aliases
PlannerV2 = Planner
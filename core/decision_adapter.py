
from __future__ import annotations

from typing import Any

from core.cognition import CognitiveDecision
from core.task import Plan, Task


class DecisionValidationError(ValueError):
    """Raised when a model decision cannot safely become a plan."""


class DecisionAdapter:
    """
    Convert validated cognitive decisions into executable plans.

    This adapter is intentionally conservative:
    - only registered tools are accepted
    - known tools have explicit argument allowlists
    - unsupported argument shapes are rejected
    - model-proposed plans never execute directly
    """

    ARGUMENTS = {
        "calculator": {"expression"},
        "weather": {"location", "latitude", "longitude"},
        "memory_store": {"text"},
        "memory_search": {"query"},
        "open_app": {"application"},
        "launch_app": {"application"},
        "web_search": {"query"},
        "web_fetch": {"url"},
        "file_operation": {"request"},
        "document_analysis": {"request"},
        "vision": {"request"},
    }

    def __init__(self, registry):
        self.registry = registry

    def to_plan(
        self,
        decision: CognitiveDecision,
    ) -> Plan:
        if decision.mode == "clarify":
            raise DecisionValidationError(
                decision.clarification
                or "The request needs clarification."
            )

        if decision.mode == "conversation":
            return self._conversation_plan(decision)

        if decision.mode != "tool":
            raise DecisionValidationError(
                f"Unsupported decision mode: {decision.mode}"
            )

        tool_name = decision.tool

        if not isinstance(tool_name, str) or not tool_name:
            raise DecisionValidationError(
                "The model did not select a valid tool."
            )

        if not self._registered(tool_name):
            raise DecisionValidationError(
                f"Tool is not registered: {tool_name}"
            )

        arguments = decision.arguments

        if not isinstance(arguments, dict):
            raise DecisionValidationError(
                "Tool arguments must be an object."
            )

        allowed = self.ARGUMENTS.get(tool_name)

        if allowed is None:
            raise DecisionValidationError(
                f"No argument policy is defined for: {tool_name}"
            )

        unexpected = set(arguments) - allowed

        if unexpected:
            raise DecisionValidationError(
                "Unexpected arguments for "
                f"{tool_name}: {sorted(unexpected)}"
            )

        self._validate_values(arguments)

        self._validate_required(tool_name, arguments)

        task = Task(
            name=f"model_{tool_name}",
            description=decision.goal,
            tool=tool_name,
            arguments=dict(arguments),
            requires_confirmation=(
                tool_name == "file_operation"
            ),
            metadata={
                "decision_source": "llm",
                "confidence": decision.confidence,
                "reasoning_summary": decision.reasoning_summary,
            },
        )

        return Plan(
            goal=decision.goal,
            tasks=[task],
            metadata={
                "planner": "decision_adapter",
                "decision_mode": decision.mode,
                "decision_source": "llm",
            },
        )

    def _registered(self, name: str) -> bool:
        if hasattr(self.registry, "has"):
            return bool(self.registry.has(name))

        if hasattr(self.registry, "names"):
            return name in self.registry.names()

        if hasattr(self.registry, "list_tools"):
            return name in self.registry.list_tools()

        return False

    @staticmethod
    def _validate_values(arguments: dict[str, Any]) -> None:
        for key, value in arguments.items():
            if not isinstance(key, str):
                raise DecisionValidationError(
                    "Argument names must be strings."
                )

            if not isinstance(value, (str, int, float, bool, type(None))):
                raise DecisionValidationError(
                    f"Unsupported value type for argument: {key}"
                )

            if isinstance(value, str) and len(value) > 2000:
                raise DecisionValidationError(
                    f"Argument is too long: {key}"
                )

    @staticmethod
    def _validate_required(
        tool_name: str,
        arguments: dict[str, Any],
    ) -> None:
        required = {
            "calculator": {"expression"},
            "memory_store": {"text"},
            "memory_search": {"query"},
            "open_app": {"application"},
            "launch_app": {"application"},
            "web_search": {"query"},
            "web_fetch": {"url"},
            "file_operation": {"request"},
            "document_analysis": {"request"},
            "vision": {"request"},
        }.get(tool_name, set())

        missing = [
            name for name in required
            if not arguments.get(name)
        ]

        if missing:
            raise DecisionValidationError(
                "Missing required arguments: "
                + ", ".join(sorted(missing))
            )

    @staticmethod
    def _conversation_plan(
        decision: CognitiveDecision,
    ) -> Plan:
        task = Task(
            name="conversation",
            description=decision.goal,
            tool="conversation",
            arguments={},
            metadata={
                "decision_source": "llm",
                "confidence": decision.confidence,
            },
        )

        return Plan(
            goal=decision.goal,
            tasks=[task],
            metadata={
                "planner": "decision_adapter",
                "decision_mode": "conversation",
                "decision_source": "llm",
            },
        )
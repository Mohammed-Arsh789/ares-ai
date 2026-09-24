from __future__ import annotations

from typing import Any

from core.cognition import CognitiveCore
from core.decision import DecisionType
from core.model_router import ModelRouter
from core.reflection import ReflectionEngine


class FakeModel:
    def __init__(self, response: str) -> None:
        self.response = response
        self.calls: list[dict[str, Any]] = []

    def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
    ) -> str:
        self.calls.append(
            {
                "prompt": prompt,
                "system": system,
            }
        )

        return self.response


def test_cognitive_conversation_decision():
    model = FakeModel(
        """
        {
            "decision_type": "conversation",
            "reasoning": "The user is asking a normal question.",
            "response": "Hello!",
            "tool_name": null,
            "tool_arguments": {},
            "confidence": 0.95,
            "needs_clarification": false,
            "clarification_question": null
        }
        """
    )

    core = CognitiveCore(
        ModelRouter(provider=model)
    )

    decision = core.decide(
        "hello",
        context={},
    )

    assert decision.decision_type == DecisionType.CONVERSATION
    assert decision.response == "Hello!"
    assert decision.confidence == 0.95


def test_cognitive_tool_decision():
    model = FakeModel(
        """
        {
            "decision_type": "tool",
            "reasoning": "The user requested a direct tool action.",
            "response": "",
            "tool_name": "calculator",
            "tool_arguments": {
                "expression": "2 + 2"
            },
            "confidence": 0.98,
            "needs_clarification": false,
            "clarification_question": null
        }
        """
    )

    core = CognitiveCore(
        ModelRouter(provider=model)
    )

    decision = core.decide(
        "calculate 2 + 2",
    )

    assert decision.decision_type == DecisionType.TOOL
    assert decision.tool_name == "calculator"
    assert decision.tool_arguments["expression"] == "2 + 2"
    assert decision.is_action


def test_cognitive_clarification():
    model = FakeModel(
        """
        {
            "decision_type": "clarification",
            "reasoning": "Required information is missing.",
            "response": "",
            "tool_name": null,
            "tool_arguments": {},
            "confidence": 0.91,
            "needs_clarification": true,
            "clarification_question": "Which file do you mean?"
        }
        """
    )

    core = CognitiveCore(
        ModelRouter(provider=model)
    )

    decision = core.decide(
        "open the file",
    )

    assert decision.decision_type == DecisionType.CLARIFICATION
    assert decision.needs_clarification
    assert decision.clarification_question == "Which file do you mean?"


def test_confidence_is_clamped():
    model = FakeModel(
        """
        {
            "decision_type": "conversation",
            "reasoning": "",
            "response": "test",
            "confidence": 900
        }
        """
    )

    core = CognitiveCore(
        ModelRouter(provider=model)
    )

    decision = core.decide("test")

    assert decision.confidence == 1.0


def test_reflection_success():
    model = FakeModel(
        """
        {
            "success": true,
            "response": "The calculation completed successfully.",
            "retry": false,
            "reason": "The tool returned a valid result.",
            "confidence": 0.97
        }
        """
    )

    reflection = ReflectionEngine(
        ModelRouter(provider=model)
    )

    result = reflection.reflect(
        user_input="calculate 2 + 2",
        action="calculator",
        result={"value": 4},
    )

    assert result.success
    assert not result.retry
    assert result.confidence == 0.97
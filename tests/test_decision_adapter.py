
import pytest

from core.cognition import CognitiveDecision
from core.decision_adapter import (
    DecisionAdapter,
    DecisionValidationError,
)


class FakeRegistry:
    def __init__(self):
        self.available = {
            "calculator",
            "weather",
            "memory_store",
        }

    def has(self, name):
        return name in self.available


def test_tool_decision_becomes_plan():
    adapter = DecisionAdapter(FakeRegistry())

    decision = CognitiveDecision(
        mode="tool",
        goal="Calculate a product",
        tool="calculator",
        arguments={"expression": "25 * 8"},
        confidence=0.9,
    )

    plan = adapter.to_plan(decision)

    assert plan.goal == "Calculate a product"
    assert len(plan.tasks) == 1
    assert plan.tasks[0].tool == "calculator"
    assert plan.tasks[0].arguments == {
        "expression": "25 * 8"
    }


def test_unknown_tool_is_rejected():
    adapter = DecisionAdapter(FakeRegistry())

    decision = CognitiveDecision(
        mode="tool",
        goal="Run something",
        tool="run_shell",
        arguments={"command": "anything"},
    )

    with pytest.raises(DecisionValidationError):
        adapter.to_plan(decision)


def test_unexpected_argument_is_rejected():
    adapter = DecisionAdapter(FakeRegistry())

    decision = CognitiveDecision(
        mode="tool",
        goal="Calculate",
        tool="calculator",
        arguments={
            "expression": "2 + 2",
            "command": "extra",
        },
    )

    with pytest.raises(DecisionValidationError):
        adapter.to_plan(decision)


def test_conversation_decision_becomes_conversation_task():
    adapter = DecisionAdapter(FakeRegistry())

    decision = CognitiveDecision(
        mode="conversation",
        goal="Explain a concept",
        confidence=0.8,
    )

    plan = adapter.to_plan(decision)

    assert len(plan.tasks) == 1
    assert plan.tasks[0].tool == "conversation"


def test_missing_required_argument_is_rejected():
    adapter = DecisionAdapter(FakeRegistry())

    decision = CognitiveDecision(
        mode="tool",
        goal="Calculate something",
        tool="calculator",
        arguments={},
    )

    with pytest.raises(DecisionValidationError):
        adapter.to_plan(decision)
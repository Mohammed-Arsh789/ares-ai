from __future__ import annotations

from typing import Any

from core.brain import ARESBrain
from core.decision import CognitiveDecision, DecisionType


class FakeCognitiveCore:
    def __init__(
        self,
        decision: CognitiveDecision,
    ) -> None:
        self.decision = decision

    def decide(
        self,
        user_input: str,
        *,
        context: dict[str, Any] | None = None,
    ) -> CognitiveDecision:
        return self.decision


class FakeReflection:
    def reflect(
        self,
        *,
        user_input: str,
        action: str,
        result: Any,
        context: dict[str, Any],
    ):
        from core.reflection import ReflectionResult

        return ReflectionResult(
            success=True,
            response="Action completed.",
            retry=False,
            reason="Successful result.",
            confidence=0.95,
        )


class FakeOrchestrator:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def execute_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        self.calls.append(
            (tool_name, arguments)
        )

        return {
            "success": True,
            "result": "done",
        }


class FakePlanner:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []

    def create_plan(
        self,
        text: str,
        intent: Any,
    ) -> dict[str, Any]:
        self.calls.append(
            (text, intent)
        )

        return {
            "tasks": [
                {
                    "name": "test_task",
                }
            ]
        }


def test_brain_handles_conversation():
    decision = CognitiveDecision.conversation(
        "Hello from ARES."
    )

    brain = ARESBrain(
        cognitive_core=FakeCognitiveCore(
            decision
        )
    )

    result = brain.process("hello")

    assert result.success
    assert not result.executed
    assert result.response == "Hello from ARES."
    assert (
        result.decision.decision_type
        == DecisionType.CONVERSATION
    )


def test_brain_handles_clarification():
    decision = CognitiveDecision.clarification(
        "Which file do you mean?"
    )

    brain = ARESBrain(
        cognitive_core=FakeCognitiveCore(
            decision
        )
    )

    result = brain.process(
        "open the file"
    )

    assert result.success
    assert result.response == "Which file do you mean?"
    assert not result.executed


def test_brain_executes_tool():
    decision = CognitiveDecision.tool(
        "calculator",
        {
            "expression": "2 + 2"
        },
    )

    orchestrator = FakeOrchestrator()

    brain = ARESBrain(
        cognitive_core=FakeCognitiveCore(
            decision
        ),
        reflection_engine=FakeReflection(),
        orchestrator=orchestrator,
    )

    result = brain.process(
        "calculate 2 + 2"
    )

    assert result.success
    assert result.executed
    assert result.response == "Action completed."

    assert orchestrator.calls == [
        (
            "calculator",
            {
                "expression": "2 + 2"
            },
        )
    ]


def test_brain_handles_plan():
    decision = CognitiveDecision.plan(
        reasoning="This requires multiple steps."
    )

    planner = FakePlanner()

    brain = ARESBrain(
        cognitive_core=FakeCognitiveCore(
            decision
        ),
        planner=planner,
    )

    result = brain.process(
        "do a multi-step task"
    )

    assert result.success
    assert not result.executed
    assert "plan" in result.metadata
    assert len(planner.calls) == 1


def test_brain_rejects_empty_input():
    decision = CognitiveDecision.conversation(
        "test"
    )

    brain = ARESBrain(
        cognitive_core=FakeCognitiveCore(
            decision
        )
    )

    try:
        brain.process("")
    except ValueError as exc:
        assert "empty input" in str(exc).lower()
    else:
        raise AssertionError(
            "Expected ValueError"
        )
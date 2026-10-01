
from __future__ import annotations

import json

from core.cognition import Cognition, CognitiveProposal


class FakeAI:
    def __init__(self, response: str):
        self.response = response
        self.calls = []

    def ask(self, message: str, *, system_prompt: str):
        self.calls.append(
            {
                "message": message,
                "system_prompt": system_prompt,
            }
        )
        return self.response


class FakeTool:
    def __init__(self, description: str):
        self.description = description


class FakeRegistry:
    def __init__(self):
        self.tools = {
            "calculator": FakeTool("Evaluate arithmetic expressions.")
        }

    def names(self):
        return list(self.tools)

    def get(self, name):
        return self.tools[name]


def response(**overrides):
    data = {
        "mode": "tool",
        "goal": "Calculate an expression",
        "tool": "calculator",
        "arguments": {"expression": "2 + 2"},
        "confidence": 0.9,
        "needs_clarification": False,
        "clarification": None,
        "reasoning_summary": "A calculator is needed.",
        "constraints": [],
    }
    data.update(overrides)
    return json.dumps(data)


def test_cognition_accepts_registered_tool():
    ai = FakeAI(response())
    cognition = Cognition(ai, FakeRegistry())

    result = cognition.decide("calculate 2 + 2")

    assert isinstance(result, CognitiveProposal)
    assert result.mode == "tool"
    assert result.tool == "calculator"
    assert result.arguments == {"expression": "2 + 2"}


def test_cognition_rejects_unknown_tool():
    ai = FakeAI(response(tool="run_shell"))
    cognition = Cognition(ai, FakeRegistry())

    result = cognition.decide("do something")

    assert result.mode == "clarify"
    assert result.needs_clarification


def test_cognition_clamps_confidence():
    ai = FakeAI(response(confidence=50))
    cognition = Cognition(ai, FakeRegistry())

    result = cognition.decide("calculate 2 + 2")

    # Invalid confidence is clamped into the allowed range.
    assert result.confidence == 1.0


def test_cognition_handles_malformed_json():
    ai = FakeAI("not json")
    cognition = Cognition(ai, FakeRegistry())

    result = cognition.decide("calculate 2 + 2")

    assert result.mode == "clarify"
    assert result.needs_clarification


def test_cognition_empty_request_does_not_call_model():
    ai = FakeAI(response())
    cognition = Cognition(ai, FakeRegistry())

    result = cognition.decide("   ")

    assert result.mode == "clarify"
    assert ai.calls == []
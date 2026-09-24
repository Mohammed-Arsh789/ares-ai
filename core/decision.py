from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DecisionType(str, Enum):
    CONVERSATION = "conversation"
    TOOL = "tool"
    PLAN = "plan"
    CLARIFICATION = "clarification"
    REFUSE = "refuse"


@dataclass(slots=True)
class CognitiveDecision:
    """
    Structured decision produced by the Cognitive Core.

    This object is deliberately model-independent so that the
    reasoning layer can work with Ollama today and another model
    provider later.
    """

    decision_type: DecisionType
    reasoning: str = ""
    response: str = ""

    tool_name: str | None = None
    tool_arguments: dict[str, Any] = field(default_factory=dict)

    confidence: float = 0.0
    needs_clarification: bool = False
    clarification_question: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_action(self) -> bool:
        return self.decision_type in {
            DecisionType.TOOL,
            DecisionType.PLAN,
        }

    @property
    def is_conversation(self) -> bool:
        return self.decision_type == DecisionType.CONVERSATION

    @classmethod
    def conversation(
        cls,
        response: str,
        *,
        reasoning: str = "",
        confidence: float = 0.0,
    ) -> "CognitiveDecision":
        return cls(
            decision_type=DecisionType.CONVERSATION,
            reasoning=reasoning,
            response=response,
            confidence=confidence,
        )

    @classmethod
    def tool(
        cls,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
        *,
        reasoning: str = "",
        confidence: float = 0.0,
    ) -> "CognitiveDecision":
        return cls(
            decision_type=DecisionType.TOOL,
            reasoning=reasoning,
            tool_name=tool_name,
            tool_arguments=arguments or {},
            confidence=confidence,
        )

    @classmethod
    def plan(
        cls,
        *,
        reasoning: str = "",
        confidence: float = 0.0,
        metadata: dict[str, Any] | None = None,
    ) -> "CognitiveDecision":
        return cls(
            decision_type=DecisionType.PLAN,
            reasoning=reasoning,
            confidence=confidence,
            metadata=metadata or {},
        )

    @classmethod
    def clarification(
        cls,
        question: str,
        *,
        reasoning: str = "",
        confidence: float = 0.0,
    ) -> "CognitiveDecision":
        return cls(
            decision_type=DecisionType.CLARIFICATION,
            reasoning=reasoning,
            clarification_question=question,
            confidence=confidence,
            needs_clarification=True,
        )

    @classmethod
    def refusal(
        cls,
        response: str,
        *,
        reasoning: str = "",
        confidence: float = 0.0,
    ) -> "CognitiveDecision":
        return cls(
            decision_type=DecisionType.REFUSE,
            reasoning=reasoning,
            response=response,
            confidence=confidence,
        )
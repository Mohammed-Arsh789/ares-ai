"""
ARES Security Decision
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DecisionType(str, Enum):

    ALLOW = "allow"

    DENY = "deny"

    CONFIRM = "confirm"


@dataclass
class SecurityDecision:

    decision: DecisionType

    reason: str

    risk_level: str

    def allowed(self) -> bool:

        return self.decision == DecisionType.ALLOW

    def needs_confirmation(self) -> bool:

        return (
            self.decision
            == DecisionType.CONFIRM
        )

    def to_dict(self):

        return {
            "decision":
                self.decision.value,

            "reason":
                self.reason,

            "risk_level":
                self.risk_level,
        }
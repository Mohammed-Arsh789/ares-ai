"""
ARES Security Risk Classifier

Initial deterministic classifier.

This is deliberately conservative.
"""

from __future__ import annotations

from .action import ActionRequest
from .risk import (
    RiskAssessment,
    RiskLevel,
)


class RiskClassifier:

    READ_ACTIONS = {
        "search",
        "fetch",
        "read",
        "list",
        "inspect",
        "analyze",
    }

    WRITE_ACTIONS = {
        "write",
        "create",
        "modify",
        "rename",
        "move",
    }

    EXECUTE_ACTIONS = {
        "execute",
        "run",
        "launch",
        "install",
    }

    DANGEROUS_ACTIONS = {
        "delete",
        "shutdown",
        "restart",
        "format",
    }

    def classify(
        self,
        request: ActionRequest,
    ) -> RiskAssessment:

        action = request.action.lower().strip()

        if action in self.DANGEROUS_ACTIONS:

            return RiskAssessment(
                RiskLevel.CRITICAL,
                "Potentially destructive system action.",
            )

        if action in self.EXECUTE_ACTIONS:

            return RiskAssessment(
                RiskLevel.HIGH,
                "Execution or application launch requested.",
            )

        if action in self.WRITE_ACTIONS:

            return RiskAssessment(
                RiskLevel.MODERATE,
                "State-changing operation requested.",
            )

        if action in self.READ_ACTIONS:

            return RiskAssessment(
                RiskLevel.SAFE,
                "Read-only operation.",
            )

        return RiskAssessment(
            RiskLevel.MODERATE,
            "Unknown action requires additional review.",
        )
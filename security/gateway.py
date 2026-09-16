"""
ARES Security Gateway

Central security boundary between ARES planning
and tool execution.

IMPORTANT:

The gateway does NOT execute tools.

It only decides whether an action is:

    ALLOW
    DENY
    CONFIRM
"""

from __future__ import annotations

from .action import ActionRequest
from .audit import AuditLogger
from .classifier import RiskClassifier
from .decision import (
    DecisionType,
    SecurityDecision,
)
from .permissions import PermissionLevel
from .risk import RiskLevel
from .store import PermissionStore


class SecurityGateway:

    def __init__(
        self,
        permission_store:
            PermissionStore | None = None,

        classifier:
            RiskClassifier | None = None,

        audit:
            AuditLogger | None = None,
    ):

        self.permissions = (
            permission_store
            or PermissionStore()
        )

        self.classifier = (
            classifier
            or RiskClassifier()
        )

        self.audit = (
            audit
            or AuditLogger()
        )

    def evaluate(
        self,
        request: ActionRequest,
    ) -> SecurityDecision:

        self.audit.record(
            "security_evaluation_started",
            request.to_dict(),
        )

        risk = self.classifier.classify(
            request
        )

        required_permission = (
            self._required_permission(
                risk.level
            )
        )

        permission_granted = (
            self.permissions.allows(
                request.tool,
                required_permission,
            )
        )

        # High-risk operations ALWAYS require
        # explicit confirmation, even if permission
        # exists.
        if risk.requires_confirmation:

            decision = SecurityDecision(
                DecisionType.CONFIRM,
                (
                    "This action requires "
                    "explicit user confirmation."
                ),
                risk.level.name,
            )

            self._audit_decision(
                request,
                decision,
            )

            return decision

        # No permission.
        if not permission_granted:

            decision = SecurityDecision(
                DecisionType.DENY,
                (
                    "Required permission has "
                    "not been granted."
                ),
                risk.level.name,
            )

            self._audit_decision(
                request,
                decision,
            )

            return decision

        # Permission exists and risk is acceptable.
        decision = SecurityDecision(
            DecisionType.ALLOW,
            "Permission and risk checks passed.",
            risk.level.name,
        )

        self._audit_decision(
            request,
            decision,
        )

        return decision

    def _audit_decision(
        self,
        request: ActionRequest,
        decision: SecurityDecision,
    ) -> None:

        self.audit.record(
            "security_decision",
            {
                "request":
                    request.to_dict(),

                "decision":
                    decision.to_dict(),
            },
        )

    @staticmethod
    def _required_permission(
        risk_level: RiskLevel,
    ) -> PermissionLevel:

        if risk_level >= RiskLevel.CRITICAL:

            return PermissionLevel.ADMIN

        if risk_level >= RiskLevel.HIGH:

            return PermissionLevel.EXECUTE

        if risk_level >= RiskLevel.MODERATE:

            return PermissionLevel.WRITE

        if risk_level >= RiskLevel.LOW:

            return PermissionLevel.USE

        return PermissionLevel.READ
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Callable


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class RecoveryDecision:
    """
    Decision describing what the recovery system should do
    after a failed action.
    """

    should_retry: bool

    attempt: int

    reason: str = ""

    modified_arguments: dict[str, Any] | None = None


class RecoveryEngine:
    """
    Controls bounded recovery attempts.

    Recovery is intentionally bounded so a broken tool cannot
    cause ARES to execute an infinite loop.
    """

    def __init__(
        self,
        *,
        max_attempts: int = 2,
    ) -> None:
        if max_attempts < 0:
            raise ValueError(
                "max_attempts cannot be negative."
            )

        self.max_attempts = max_attempts

    def decide(
        self,
        *,
        attempt: int,
        retryable: bool,
        action: str,
        arguments: dict[str, Any],
        error: str = "",
    ) -> RecoveryDecision:
        logger.info(
            "Recovery evaluation: action=%s attempt=%s",
            action,
            attempt,
        )

        if not retryable:
            return RecoveryDecision(
                should_retry=False,
                attempt=attempt,
                reason=(
                    "Failure is not marked as retryable."
                ),
            )

        if attempt >= self.max_attempts:
            return RecoveryDecision(
                should_retry=False,
                attempt=attempt,
                reason=(
                    "Maximum recovery attempts reached."
                ),
            )

        logger.warning(
            "Retrying action '%s'. Reason: %s",
            action,
            error,
        )

        return RecoveryDecision(
            should_retry=True,
            attempt=attempt + 1,
            reason=(
                "A bounded retry is available."
            ),
            modified_arguments=dict(arguments),
        )

    def execute_with_recovery(
        self,
        *,
        action: str,
        arguments: dict[str, Any],
        executor: Callable[
            [str, dict[str, Any]],
            Any,
        ],
        verifier: Callable[
            [str, Any],
            Any,
        ],
    ) -> tuple[Any, Any, int]:
        """
        Execute an action and perform bounded verification/retry.

        Returns:

            result
            verification_result
            attempts_used
        """

        current_arguments = dict(arguments)

        attempt = 0

        while True:
            result = executor(
                action,
                current_arguments,
            )

            verification = verifier(
                action,
                result,
            )

            if verification.verified:
                return (
                    result,
                    verification,
                    attempt + 1,
                )

            decision = self.decide(
                attempt=attempt,
                retryable=verification.retryable,
                action=action,
                arguments=current_arguments,
                error=verification.reason,
            )

            if not decision.should_retry:
                return (
                    result,
                    verification,
                    attempt + 1,
                )

            attempt = decision.attempt

            if decision.modified_arguments is not None:
                current_arguments = (
                    decision.modified_arguments
                )
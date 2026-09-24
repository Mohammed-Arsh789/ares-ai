from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class VerificationResult:
    """
    Result of checking whether an ARES action actually succeeded.
    """

    verified: bool

    reason: str = ""

    confidence: float = 0.0

    evidence: Any = None

    retryable: bool = False


class VerificationEngine:
    """
    Deterministic verification layer.

    The verifier does not blindly trust an LLM's statement that
    something succeeded.

    It examines the actual execution result and determines whether
    there is enough evidence to consider the action successful.
    """

    def verify(
        self,
        *,
        action: str,
        result: Any,
        expected: Any = None,
    ) -> VerificationResult:
        logger.info(
            "Verifying action: %s",
            action,
        )

        if result is None:
            return VerificationResult(
                verified=False,
                reason="No execution result was returned.",
                confidence=0.0,
                retryable=True,
            )

        if isinstance(result, bool):
            if result:
                return VerificationResult(
                    verified=True,
                    reason="Execution returned True.",
                    confidence=1.0,
                    evidence=result,
                )

            return VerificationResult(
                verified=False,
                reason="Execution returned False.",
                confidence=1.0,
                evidence=result,
                retryable=True,
            )

        if isinstance(result, dict):
            return self._verify_mapping(
                action=action,
                result=result,
                expected=expected,
            )

        if hasattr(result, "success"):
            success = getattr(
                result,
                "success",
            )

            if isinstance(success, bool):
                return VerificationResult(
                    verified=success,
                    reason=(
                        "Execution result exposed "
                        "a success flag."
                    ),
                    confidence=1.0,
                    evidence=result,
                    retryable=not success,
                )

        return VerificationResult(
            verified=True,
            reason=(
                "Execution produced a non-empty result, "
                "but no explicit success contract was available."
            ),
            confidence=0.5,
            evidence=result,
        )

    def _verify_mapping(
        self,
        *,
        action: str,
        result: dict[str, Any],
        expected: Any,
    ) -> VerificationResult:
        if "success" in result:
            success = result["success"]

            if success is True:
                return VerificationResult(
                    verified=True,
                    reason=(
                        "Execution result explicitly "
                        "reported success."
                    ),
                    confidence=1.0,
                    evidence=result,
                )

            if success is False:
                return VerificationResult(
                    verified=False,
                    reason=(
                        result.get(
                            "error",
                            "Execution explicitly reported failure.",
                        )
                    ),
                    confidence=1.0,
                    evidence=result,
                    retryable=True,
                )

        if "error" in result:
            return VerificationResult(
                verified=False,
                reason=str(result["error"]),
                confidence=1.0,
                evidence=result,
                retryable=True,
            )

        if "status" in result:
            status = str(
                result["status"]
            ).lower()

            if status in {
                "success",
                "successful",
                "completed",
                "complete",
                "ok",
                "done",
            }:
                return VerificationResult(
                    verified=True,
                    reason=(
                        f"Execution status was '{status}'."
                    ),
                    confidence=0.95,
                    evidence=result,
                )

            if status in {
                "failed",
                "failure",
                "error",
            }:
                return VerificationResult(
                    verified=False,
                    reason=(
                        f"Execution status was '{status}'."
                    ),
                    confidence=0.95,
                    evidence=result,
                    retryable=True,
                )

        if expected is not None:
            if result == expected:
                return VerificationResult(
                    verified=True,
                    reason="Result matched expected output.",
                    confidence=1.0,
                    evidence=result,
                )

            return VerificationResult(
                verified=False,
                reason="Result did not match expected output.",
                confidence=1.0,
                evidence=result,
                retryable=True,
            )

        return VerificationResult(
            verified=True,
            reason=(
                "No explicit failure evidence was found."
            ),
            confidence=0.5,
            evidence=result,
        )
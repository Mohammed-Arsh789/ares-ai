from __future__ import annotations

from core.recovery import RecoveryEngine
from core.verification import VerificationEngine


def test_verification_accepts_success_result():
    verifier = VerificationEngine()

    result = verifier.verify(
        action="calculator",
        result={
            "success": True,
            "value": 4,
        },
    )

    assert result.verified
    assert result.confidence == 1.0
    assert not result.retryable


def test_verification_detects_failure():
    verifier = VerificationEngine()

    result = verifier.verify(
        action="open_app",
        result={
            "success": False,
            "error": "Application not found.",
        },
    )

    assert not result.verified
    assert result.retryable
    assert "Application not found" in result.reason


def test_verification_detects_status():
    verifier = VerificationEngine()

    result = verifier.verify(
        action="test",
        result={
            "status": "completed",
        },
    )

    assert result.verified


def test_recovery_is_bounded():
    recovery = RecoveryEngine(
        max_attempts=2
    )

    first = recovery.decide(
        attempt=0,
        retryable=True,
        action="open_app",
        arguments={
            "app": "notepad",
        },
        error="First attempt failed.",
    )

    assert first.should_retry
    assert first.attempt == 1

    second = recovery.decide(
        attempt=1,
        retryable=True,
        action="open_app",
        arguments={
            "app": "notepad",
        },
        error="Second attempt failed.",
    )

    assert second.should_retry
    assert second.attempt == 2

    third = recovery.decide(
        attempt=2,
        retryable=True,
        action="open_app",
        arguments={
            "app": "notepad",
        },
        error="Third attempt failed.",
    )

    assert not third.should_retry


def test_recovery_execution_succeeds_after_retry():
    recovery = RecoveryEngine(
        max_attempts=2
    )

    verifier = VerificationEngine()

    calls = []

    def executor(
        action: str,
        arguments: dict,
    ):
        calls.append(arguments)

        if len(calls) == 1:
            return {
                "success": False,
                "error": "Temporary failure.",
            }

        return {
            "success": True,
            "result": "completed",
        }

    def verify(
        action: str,
        result,
    ):
        return verifier.verify(
            action=action,
            result=result,
        )

    result, verification, attempts = (
        recovery.execute_with_recovery(
            action="test_tool",
            arguments={
                "value": 123,
            },
            executor=executor,
            verifier=verify,
        )
    )

    assert verification.verified
    assert result["success"]
    assert attempts == 2
    assert len(calls) == 2
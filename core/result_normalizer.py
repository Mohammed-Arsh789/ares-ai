"""
ARES result normalization layer.

Converts arbitrary tool/agent return values into predictable
ExecutionResult objects.
"""

from __future__ import annotations

from typing import Any, Optional

from .results import (
    ToolResult,
    AgentResult,
    ExecutionResult,
    ResultStatus,
)


def normalize_tool_result(
    name: str,
    value: Any,
    task_id: Optional[str] = None,
) -> ExecutionResult:
    """
    Convert a tool output into an ExecutionResult.
    """

    if isinstance(value, ExecutionResult):
        return value

    if isinstance(value, ToolResult):
        if value.success:
            return ExecutionResult.ok(
                source="tool",
                name=name,
                output=value.data,
                task_id=task_id,
                metadata=value.metadata,
            )

        return ExecutionResult.fail(
            source="tool",
            name=name,
            error=value.error or "Tool failed",
            task_id=task_id,
            metadata=value.metadata,
        )

    if isinstance(value, AgentResult):
        if value.success:
            return ExecutionResult.ok(
                source="agent",
                name=name,
                output=value.output,
                task_id=task_id,
                metadata=value.metadata,
            )

        return ExecutionResult.fail(
            source="agent",
            name=name,
            error=value.error or "Agent failed",
            task_id=task_id,
            metadata=value.metadata,
        )

    if isinstance(value, dict):
        # Preserve explicit result-like dictionaries.
        if value.get("success") is False:
            return ExecutionResult.fail(
                source="tool",
                name=name,
                error=str(value.get("error", "Operation failed")),
                task_id=task_id,
                metadata=value.get("metadata", {}),
            )

    return ExecutionResult.ok(
        source="tool",
        name=name,
        output=value,
        task_id=task_id,
    )


def normalize_agent_result(
    name: str,
    value: Any,
    task_id: Optional[str] = None,
) -> ExecutionResult:
    """
    Convert an agent output into an ExecutionResult.
    """

    if isinstance(value, ExecutionResult):
        return value

    if isinstance(value, AgentResult):
        if value.success:
            return ExecutionResult.ok(
                source="agent",
                name=name,
                output=value.output,
                task_id=task_id,
                metadata=value.metadata,
            )

        return ExecutionResult.fail(
            source="agent",
            name=name,
            error=value.error or "Agent failed",
            task_id=task_id,
            metadata=value.metadata,
        )

    return ExecutionResult.ok(
        source="agent",
        name=name,
        output=value,
        task_id=task_id,
    )


def normalize_failure(
    source: str,
    name: str,
    error: Exception | str,
    task_id: Optional[str] = None,
) -> ExecutionResult:
    """
    Convert an exception into a standard failure result.
    """

    return ExecutionResult.fail(
        source=source,
        name=name,
        error=str(error),
        task_id=task_id,
    )
"""
ARES Unified Result System.

This module defines the standard result objects used across:
- Tools
- Agents
- Executors
- Orchestrators
- Workflows
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from datetime import datetime, timezone
import uuid


class ResultStatus(str, Enum):
    """
    Universal operation status.
    """

    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    PENDING = "pending"
    CANCELLED = "cancelled"
    DENIED = "denied"
    TIMEOUT = "timeout"


def create_trace_id() -> str:
    """
    Generate a unique trace identifier for debugging and logging.
    """
    return uuid.uuid4().hex


def utc_timestamp() -> str:
    """
    Return a timezone-aware UTC timestamp.
    """
    return datetime.now(timezone.utc).isoformat()


@dataclass
class BaseResult:
    """
    Shared result properties.
    """

    success: bool
    status: ResultStatus
    output: Any = None
    error: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)
    trace_id: str = field(default_factory=create_trace_id)
    created_at: str = field(default_factory=utc_timestamp)

    def is_success(self) -> bool:
        return self.success

    def is_failure(self) -> bool:
        return not self.success

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "status": self.status.value,
            "output": self.output,
            "error": self.error,
            "metadata": self.metadata,
            "trace_id": self.trace_id,
            "created_at": self.created_at,
        }


@dataclass
class ToolResult(BaseResult):
    """
    Standard result produced by a tool.
    """

    tool: str = ""

    @classmethod
    def ok(
        cls,
        tool: str,
        data: Any = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "ToolResult":
        return cls(
            success=True,
            status=ResultStatus.SUCCESS,
            output=data,
            tool=tool,
            metadata=metadata or {},
        )

    @classmethod
    def fail(
        cls,
        tool: str,
        error: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "ToolResult":
        return cls(
            success=False,
            status=ResultStatus.FAILURE,
            error=str(error),
            tool=tool,
            metadata=metadata or {},
        )

    @property
    def data(self) -> Any:
        """
        Backward-compatible alias used by existing tools.
        """
        return self.output

    def unwrap(self) -> Any:
        if not self.success:
            raise RuntimeError(self.error or "Tool execution failed")

        return self.output

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["tool"] = self.tool
        data["data"] = self.output
        return data


@dataclass
class AgentResult(BaseResult):
    """
    Standard result produced by an agent.
    """

    agent: str = ""

    @classmethod
    def ok(
        cls,
        agent: str,
        output: Any = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "AgentResult":
        return cls(
            success=True,
            status=ResultStatus.SUCCESS,
            output=output,
            agent=agent,
            metadata=metadata or {},
        )

    @classmethod
    def fail(
        cls,
        agent: str,
        error: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "AgentResult":
        return cls(
            success=False,
            status=ResultStatus.FAILURE,
            error=str(error),
            agent=agent,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["agent"] = self.agent
        return data


@dataclass
class ExecutionResult(BaseResult):
    """
    Standard result produced by the executor or orchestrator.
    """

    source: str = ""
    name: str = ""
    task_id: Optional[str] = None
    attempts: int = 1
    duration_ms: Optional[float] = None

    @classmethod
    def ok(
        cls,
        source: str,
        name: str,
        output: Any = None,
        task_id: Optional[str] = None,
        attempts: int = 1,
        duration_ms: Optional[float] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "ExecutionResult":
        return cls(
            success=True,
            status=ResultStatus.SUCCESS,
            output=output,
            source=source,
            name=name,
            task_id=task_id,
            attempts=attempts,
            duration_ms=duration_ms,
            metadata=metadata or {},
        )

    @classmethod
    def fail(
        cls,
        source: str,
        name: str,
        error: str,
        task_id: Optional[str] = None,
        attempts: int = 1,
        duration_ms: Optional[float] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "ExecutionResult":
        return cls(
            success=False,
            status=ResultStatus.FAILURE,
            error=str(error),
            source=source,
            name=name,
            task_id=task_id,
            attempts=attempts,
            duration_ms=duration_ms,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data.update(
            {
                "source": self.source,
                "name": self.name,
                "task_id": self.task_id,
                "attempts": self.attempts,
                "duration_ms": self.duration_ms,
            }
        )
        return data
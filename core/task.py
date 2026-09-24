from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class TaskStatus(str, Enum):
    """Lifecycle state of an ARES task."""

    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


def create_task_id() -> str:
    """Create a short unique task identifier."""
    return f"task_{uuid4().hex[:12]}"


@dataclass
class Task:
    """
    One executable unit inside an ARES plan.

    A Task describes WHAT should happen.
    The Orchestrator decides HOW and WHEN it happens.
    """

    name: str
    description: str = ""

    tool: Optional[str] = None
    arguments: Dict[str, Any] = field(default_factory=dict)

    dependencies: List[str] = field(default_factory=list)

    task_id: str = field(default_factory=create_task_id)

    status: TaskStatus = TaskStatus.PENDING

    result: Any = None
    error: Optional[str] = None

    requires_confirmation: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_complete(self) -> bool:
        """Return True when the task no longer needs execution."""
        return self.status in {
            TaskStatus.SUCCESS,
            TaskStatus.FAILURE,
            TaskStatus.SKIPPED,
            TaskStatus.CANCELLED,
        }

    def is_successful(self) -> bool:
        return self.status == TaskStatus.SUCCESS

    def is_blocked(self) -> bool:
        return self.status == TaskStatus.BLOCKED

    def mark_ready(self) -> None:
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.READY

    def mark_running(self) -> None:
        self.status = TaskStatus.RUNNING
        self.error = None

    def mark_success(self, result: Any = None) -> None:
        self.status = TaskStatus.SUCCESS
        self.result = result
        self.error = None

    def mark_failure(self, error: Any) -> None:
        self.status = TaskStatus.FAILURE
        self.error = str(error)

    def mark_blocked(self, reason: Any) -> None:
        self.status = TaskStatus.BLOCKED
        self.error = str(reason)

    def mark_skipped(self, reason: Any = None) -> None:
        self.status = TaskStatus.SKIPPED
        if reason is not None:
            self.error = str(reason)

    def mark_cancelled(self, reason: Any = None) -> None:
        self.status = TaskStatus.CANCELLED
        if reason is not None:
            self.error = str(reason)

    def add_dependency(self, task_id: str) -> None:
        """Add a dependency without creating duplicates."""
        if task_id == self.task_id:
            raise ValueError("A task cannot depend on itself.")

        if task_id not in self.dependencies:
            self.dependencies.append(task_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "tool": self.tool,
            "arguments": dict(self.arguments),
            "dependencies": list(self.dependencies),
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "requires_confirmation": self.requires_confirmation,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        status_value = data.get("status", TaskStatus.PENDING)

        try:
            status = TaskStatus(status_value)
        except ValueError:
            status = TaskStatus.PENDING

        return cls(
            task_id=data.get("task_id", create_task_id()),
            name=data.get("name", "unnamed_task"),
            description=data.get("description", ""),
            tool=data.get("tool"),
            arguments=dict(data.get("arguments", {})),
            dependencies=list(data.get("dependencies", [])),
            status=status,
            result=data.get("result"),
            error=data.get("error"),
            requires_confirmation=bool(
                data.get("requires_confirmation", False)
            ),
            metadata=dict(data.get("metadata", {})),
        )


@dataclass
class Plan:
    """
    A collection of Tasks representing one ARES objective.
    """

    goal: str
    tasks: List[Task] = field(default_factory=list)

    plan_id: str = field(default_factory=lambda: f"plan_{uuid4().hex[:12]}")

    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_task(self, task: Task) -> Task:
        if any(existing.task_id == task.task_id for existing in self.tasks):
            raise ValueError(f"Duplicate task ID: {task.task_id}")

        self.tasks.append(task)
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        for task in self.tasks:
            if task.task_id == task_id:
                return task

        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "goal": self.goal,
            "tasks": [task.to_dict() for task in self.tasks],
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Plan":
        plan = cls(
            plan_id=data.get("plan_id", f"plan_{uuid4().hex[:12]}"),
            goal=data.get("goal", ""),
            metadata=dict(data.get("metadata", {})),
        )

        for task_data in data.get("tasks", []):
            plan.add_task(Task.from_dict(task_data))

        return plan
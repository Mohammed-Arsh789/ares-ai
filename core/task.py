"""
ARES Task Model
Step 170
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):

    PENDING = "pending"

    PLANNING = "planning"

    READY = "ready"

    RUNNING = "running"

    WAITING = "waiting"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


@dataclass
class Task:

    id: str

    description: str

    intent: str

    status: TaskStatus = TaskStatus.PENDING

    steps: list[dict[str, Any]] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    result: Any = None

    error: str | None = None

    def to_dict(self):

        return {
            "id": self.id,
            "description": self.description,
            "intent": self.intent,
            "status": self.status.value,
            "steps": self.steps,
            "metadata": self.metadata,
            "result": self.result,
            "error": self.error,
        }
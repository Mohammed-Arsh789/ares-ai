from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AgentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentTask:
    task_id: str
    agent_name: str
    input_data: Any
    status: AgentStatus = AgentStatus.PENDING
    output_data: Any = None
    error: str | None = None


@dataclass
class WorkflowResult:
    success: bool
    outputs: list[Any] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
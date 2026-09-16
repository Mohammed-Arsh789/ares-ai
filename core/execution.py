"""
ARES execution request and execution context models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ExecutionContext:
    """
    Information available during execution.
    """

    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    session_id: Optional[str] = None
    variables: dict[str, Any] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)
    permissions: set[str] = field(default_factory=set)
    dry_run: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.variables.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.variables[key] = value

    def update(self, values: dict[str, Any]) -> None:
        self.variables.update(values)


@dataclass
class ExecutionRequest:
    """
    A normalized request sent to a tool or agent.
    """

    name: str
    source: str
    arguments: dict[str, Any] = field(default_factory=dict)
    task_id: Optional[str] = None
    requires_confirmation: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def argument(self, key: str, default: Any = None) -> Any:
        return self.arguments.get(key, default)
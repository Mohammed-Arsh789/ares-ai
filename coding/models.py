from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CodingTaskType(str, Enum):
    CREATE = "create"
    MODIFY = "modify"
    DEBUG = "debug"
    REVIEW = "review"
    EXPLAIN = "explain"
    REFACTOR = "refactor"
    TEST = "test"


class ChangeType(str, Enum):
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"
    NONE = "none"


@dataclass
class CodingRequest:
    """
    Represents a structured coding request.
    """

    instruction: str
    project_path: str | None = None
    task_type: CodingTaskType = CodingTaskType.MODIFY
    target_files: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.instruction, str):
            raise TypeError("instruction must be a string")

        self.instruction = self.instruction.strip()

        if not self.instruction:
            raise ValueError("instruction cannot be empty")


@dataclass
class FileContext:
    """
    Context extracted from one project file.
    """

    path: str
    content: str
    language: str
    size_bytes: int


@dataclass
class ChangeProposal:
    """
    Represents a proposed file change.

    This does not automatically modify files.
    """

    path: str
    change_type: ChangeType
    original_content: str | None = None
    proposed_content: str | None = None
    reason: str = ""

    @property
    def is_destructive(self) -> bool:
        return self.change_type == ChangeType.DELETE


@dataclass
class CodingResult:
    """
    Standard result returned by the coding agent.
    """

    success: bool
    message: str
    task_type: CodingTaskType | None = None
    files_inspected: list[str] = field(default_factory=list)
    proposals: list[ChangeProposal] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
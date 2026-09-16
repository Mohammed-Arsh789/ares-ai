from dataclasses import dataclass, field
from enum import Enum


class CriticSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class CriticIssue:
    category: str
    message: str
    severity: CriticSeverity
    suggestion: str = ""


@dataclass
class CriticReport:
    score: float
    approved: bool
    issues: list[CriticIssue] = field(
        default_factory=list
    )
    strengths: list[str] = field(
        default_factory=list
    )

    def __post_init__(self):
        self.score = max(0.0, min(100.0, self.score))
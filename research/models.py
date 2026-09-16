from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ResearchDepth(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"


class EvidenceQuality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


@dataclass
class ResearchRequest:
    question: str
    depth: ResearchDepth = ResearchDepth.STANDARD
    max_sources: int = 10

    def __post_init__(self):
        self.question = self.question.strip()

        if not self.question:
            raise ValueError("Research question cannot be empty")

        if self.max_sources < 1:
            raise ValueError("max_sources must be at least 1")


@dataclass
class ResearchSubtask:
    title: str
    query: str
    priority: int = 1
    completed: bool = False


@dataclass
class ResearchSource:
    title: str
    url: str
    snippet: str = ""
    source_type: str = "web"
    quality: EvidenceQuality = EvidenceQuality.UNKNOWN


@dataclass
class EvidenceItem:
    claim: str
    source_url: str
    supporting_text: str = ""
    confidence: float = 0.5

    def __post_init__(self):
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")


@dataclass
class ResearchReport:
    question: str
    summary: str
    sources: list[ResearchSource] = field(default_factory=list)
    evidence: list[EvidenceItem] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
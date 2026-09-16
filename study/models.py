from dataclasses import dataclass, field
from enum import Enum


class Difficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class StudyRequest:
    topic: str
    difficulty: Difficulty = Difficulty.INTERMEDIATE
    session_minutes: int = 30

    def __post_init__(self):
        self.topic = self.topic.strip()

        if not self.topic:
            raise ValueError("topic cannot be empty")

        if self.session_minutes <= 0:
            raise ValueError("session_minutes must be positive")


@dataclass
class Flashcard:
    question: str
    answer: str
    topic: str
    difficulty: Difficulty = Difficulty.INTERMEDIATE


@dataclass
class QuizQuestion:
    question: str
    correct_answer: str
    explanation: str = ""


@dataclass
class QuizResult:
    total: int
    correct: int
    incorrect_questions: list[str] = field(
        default_factory=list
    )

    @property
    def percentage(self) -> float:
        if self.total == 0:
            return 0.0

        return (self.correct / self.total) * 100
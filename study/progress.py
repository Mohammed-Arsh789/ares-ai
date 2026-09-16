from dataclasses import dataclass, field


@dataclass
class TopicProgress:
    topic: str
    attempts: int = 0
    correct_answers: int = 0
    total_answers: int = 0
    weak_areas: list[str] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        if self.total_answers == 0:
            return 0.0

        return self.correct_answers / self.total_answers


class ProgressTracker:
    def __init__(self):
        self.topics: dict[str, TopicProgress] = {}

    def get_or_create(self, topic: str) -> TopicProgress:
        if topic not in self.topics:
            self.topics[topic] = TopicProgress(topic=topic)

        return self.topics[topic]

    def record_quiz(
        self,
        topic: str,
        correct: int,
        total: int,
        weak_areas: list[str] | None = None,
    ):
        progress = self.get_or_create(topic)

        progress.attempts += 1
        progress.correct_answers += correct
        progress.total_answers += total

        if weak_areas:
            progress.weak_areas.extend(weak_areas)
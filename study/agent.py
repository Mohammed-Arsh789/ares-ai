from .cards import FlashcardGenerator
from .models import Difficulty, StudyRequest
from .planner import StudyPlanner
from .progress import ProgressTracker
from .quiz import QuizEngine


class StudyAgent:
    def __init__(self):
        self.planner = StudyPlanner()
        self.cards = FlashcardGenerator()
        self.quiz = QuizEngine()
        self.progress = ProgressTracker()

    def create_study_plan(
        self,
        topic: str,
        difficulty: str = "intermediate",
        session_minutes: int = 30,
    ) -> list[dict]:
        request = self.planner.create_request(
            topic,
            difficulty,
            session_minutes,
        )

        return self.planner.create_plan(request)

    def create_flashcards(
        self,
        topic: str,
        concepts: list[str],
        difficulty: str = "intermediate",
    ):
        try:
            level = Difficulty(difficulty.lower())
        except ValueError:
            level = Difficulty.INTERMEDIATE

        return self.cards.generate(
            topic=topic,
            concepts=concepts,
            difficulty=level,
        )
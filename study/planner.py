from .models import Difficulty, StudyRequest


class StudyPlanner:
    def create_request(
        self,
        topic: str,
        difficulty: str = "intermediate",
        session_minutes: int = 30,
    ) -> StudyRequest:
        try:
            level = Difficulty(difficulty.lower())
        except ValueError:
            level = Difficulty.INTERMEDIATE

        return StudyRequest(
            topic=topic,
            difficulty=level,
            session_minutes=session_minutes,
        )

    def create_plan(
        self,
        request: StudyRequest,
    ) -> list[dict]:
        total = request.session_minutes

        explanation_time = max(5, int(total * 0.35))
        practice_time = max(5, int(total * 0.35))
        review_time = max(5, total - explanation_time - practice_time)

        return [
            {
                "stage": "Concept explanation",
                "minutes": explanation_time,
            },
            {
                "stage": "Active practice",
                "minutes": practice_time,
            },
            {
                "stage": "Review and recall",
                "minutes": review_time,
            },
        ]
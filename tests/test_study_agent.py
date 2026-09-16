from study import (
    FlashcardGenerator,
    ProgressTracker,
    StudyAgent,
    StudyPlanner,
)


def test_study_plan():
    planner = StudyPlanner()

    request = planner.create_request(
        "Physics",
        session_minutes=40,
    )

    plan = planner.create_plan(request)

    assert len(plan) == 3
    assert sum(item["minutes"] for item in plan) <= 40


def test_flashcards():
    generator = FlashcardGenerator()

    cards = generator.generate(
        "Python",
        ["variables", "loops"],
    )

    assert len(cards) == 2


def test_progress():
    tracker = ProgressTracker()

    tracker.record_quiz(
        topic="Math",
        correct=8,
        total=10,
    )

    progress = tracker.get_or_create("Math")

    assert progress.accuracy == 0.8


def test_study_agent_import():
    agent = StudyAgent()

    plan = agent.create_study_plan(
        "Biology",
        session_minutes=30,
    )

    assert plan
    assert len(plan) == 3
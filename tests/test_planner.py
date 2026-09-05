from core.intent_detector import IntentDetector
from core.planner import Planner


def main():

    detector = IntentDetector()

    planner = Planner()

    intent = detector.detect(
        "What is the weather today?"
    )

    task = planner.create_plan(
        "What is the weather today?",
        intent,
    )

    print(task.to_dict())

    assert task.intent == "weather"

    assert len(task.steps) >= 3

    print()
    print("PLANNER TEST PASSED")


if __name__ == "__main__":
    main()
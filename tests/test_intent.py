from core.intent_detector import IntentDetector
from core.intent import IntentType


def main():

    detector = IntentDetector()

    tests = [
        (
            "What is the weather today?",
            IntentType.WEATHER,
        ),
        (
            "Search the web for Python news",
            IntentType.SEARCH,
        ),
        (
            "Debug this Python code",
            IntentType.CODING,
        ),
        (
            "Open Chrome",
            IntentType.APPLICATION,
        ),
        (
            "Remind me every day",
            IntentType.AUTOMATION,
        ),
        (
            "What is quantum computing?",
            IntentType.QUESTION,
        ),
    ]

    for text, expected in tests:

        result = detector.detect(text)

        print(
            f"{text!r} -> "
            f"{result.type.value} "
            f"({result.confidence:.2f})"
        )

        assert result.type == expected

    print()
    print("INTENT TESTS PASSED")


if __name__ == "__main__":
    main()
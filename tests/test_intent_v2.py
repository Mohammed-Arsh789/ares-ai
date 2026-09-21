from core.intent import IntentName
from core.intent_detector import IntentDetector


def test_calculator_intent():
    intent = IntentDetector().detect("calculate 25 * 8")

    assert intent.name == IntentName.CALCULATOR
    assert intent.requires_tool is True
    assert intent.entities["expression"] == "25 * 8"


def test_memory_store_intent():
    intent = IntentDetector().detect("remember that I love watching F1")

    assert intent.name == IntentName.MEMORY_STORE
    assert intent.entities["content"] == "I love watching F1"


def test_weather_intent():
    intent = IntentDetector().detect("what is the weather in Bengaluru")

    assert intent.name == IntentName.WEATHER
    assert intent.requires_tool is True


def test_web_search_intent():
    intent = IntentDetector().detect("search the web for Python 3.13")

    assert intent.name == IntentName.WEB_SEARCH
    assert "Python 3.13" in intent.entities["query"]


def test_open_app_intent():
    intent = IntentDetector().detect("open notepad")

    assert intent.name == IntentName.OPEN_APP
    assert intent.entities["application"] == "notepad"


def test_coding_intent():
    intent = IntentDetector().detect("explain this Python code")

    assert intent.name == IntentName.CODING


def test_study_intent():
    intent = IntentDetector().detect("help me study biology")

    assert intent.name == IntentName.STUDY


def test_review_intent():
    intent = IntentDetector().detect("review this answer")

    assert intent.name == IntentName.REVIEW


def test_conversation_fallback():
    intent = IntentDetector().detect("tell me an interesting fact")

    assert intent.name == IntentName.CONVERSATION


def test_intent_serialization():
    intent = IntentDetector().detect("open calculator")
    data = intent.to_dict()

    assert data["name"] == "open_app"
    assert "confidence" in data
    assert "entities" in data
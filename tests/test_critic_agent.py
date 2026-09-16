from critic import CriticAgent


def test_good_response():
    agent = CriticAgent()

    report = agent.review(
        "Python is a programming language used to build software."
    )

    assert report.score >= 70
    assert report.approved is True


def test_empty_response():
    agent = CriticAgent()

    report = agent.review("")

    assert report.approved is False
    assert len(report.issues) > 0
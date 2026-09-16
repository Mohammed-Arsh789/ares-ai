from research import (
    EvidenceQuality,
    ResearchAgent,
    ResearchPlanner,
    SourceManager,
)


def fake_search(query, max_results=5):
    return [
        {
            "title": "Example Source",
            "url": "https://example.com/article",
            "snippet": f"Evidence related to {query}",
        },
        {
            "title": "Duplicate Source",
            "url": "https://example.com/article",
            "snippet": "Duplicate",
        },
    ][:max_results]


def test_research_request_planning():
    planner = ResearchPlanner()

    request = planner.create_request(
        "artificial intelligence",
        depth="deep",
    )

    subtasks = planner.decompose(request)

    assert request.question == "artificial intelligence"
    assert len(subtasks) >= 3


def test_source_quality():
    manager = SourceManager()

    source = manager.create_source(
        "Government source",
        "https://example.gov/report",
    )

    assert source.quality == EvidenceQuality.HIGH


def test_source_deduplication():
    manager = SourceManager()

    first = manager.create_source(
        "A",
        "https://example.com",
    )

    second = manager.create_source(
        "B",
        "https://example.com",
    )

    result = manager.deduplicate([first, second])

    assert len(result) == 1


def test_research_agent():
    agent = ResearchAgent(search_function=fake_search)

    report = agent.research(
        "Python programming",
        max_sources=5,
    )

    assert report.question == "Python programming"
    assert len(report.sources) > 0
    assert len(report.evidence) > 0
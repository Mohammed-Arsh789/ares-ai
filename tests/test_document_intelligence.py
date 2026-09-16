from pathlib import Path

from tools.document import (
    DocumentIntelligence,
)


def test_text_document(tmp_path: Path):

    file_path = (
        tmp_path / "test.txt"
    )

    file_path.write_text(
        "ARES is an AI assistant.\n"
        "ARES can analyze documents.\n"
        "Python is useful.",
        encoding="utf-8",
    )

    intelligence = (
        DocumentIntelligence()
    )

    document = intelligence.load(
        str(file_path)
    )

    assert document.name == "test.txt"

    assert document.extension == ".txt"

    assert "ARES" in document.content

    assert document.word_count > 0


def test_document_analysis(tmp_path: Path):

    file_path = (
        tmp_path / "analysis.txt"
    )

    file_path.write_text(
        "Hello ARES.\n"
        "This is a test.",
        encoding="utf-8",
    )

    intelligence = (
        DocumentIntelligence()
    )

    document = intelligence.load(
        str(file_path)
    )

    result = intelligence.analyze(
        document
    )

    assert result["words"] > 0

    assert result["lines"] == 2


def test_document_search(tmp_path: Path):

    file_path = (
        tmp_path / "search.txt"
    )

    file_path.write_text(
        "ARES is intelligent.\n"
        "Python powers many systems.\n"
        "ARES can use Python.",
        encoding="utf-8",
    )

    intelligence = (
        DocumentIntelligence()
    )

    document = intelligence.load(
        str(file_path)
    )

    matches = intelligence.search(
        document,
        "ARES",
    )

    assert len(matches) == 2

    assert matches[0].score >= 1
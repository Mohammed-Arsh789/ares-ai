from pathlib import Path

from coding.agent import CodingAgent
from coding.context import CodeContextBuilder
from coding.models import CodingTaskType
from coding.planner import CodingTaskPlanner
from coding.project import ProjectInspector
from coding.validator import CodeValidator


def test_project_inspector(tmp_path: Path):

    source_file = tmp_path / "example.py"

    source_file.write_text(
        "print('hello')",
        encoding="utf-8",
    )

    inspector = ProjectInspector()

    files = inspector.list_files(tmp_path)

    assert source_file in files


def test_language_detection():

    builder = CodeContextBuilder()

    assert (
        builder.detect_language("main.py")
        == "python"
    )

    assert (
        builder.detect_language("app.js")
        == "javascript"
    )


def test_planner_classifies_debug():

    planner = CodingTaskPlanner()

    task_type = planner.classify(
        "Fix the traceback in this Python file"
    )

    assert task_type == CodingTaskType.DEBUG


def test_python_validator():

    validator = CodeValidator()

    valid = validator.validate_python_syntax(
        "x = 10\nprint(x)"
    )

    invalid = validator.validate_python_syntax(
        "def broken(:"
    )

    assert valid["valid"] is True
    assert invalid["valid"] is False


def test_coding_agent_analysis(tmp_path: Path):

    source_file = tmp_path / "main.py"

    source_file.write_text(
        "print('ARES')",
        encoding="utf-8",
    )

    agent = CodingAgent()

    result = agent.analyze_request(
        "Inspect and explain this Python project",
        project_path=str(tmp_path),
    )

    assert result.success is True

    assert (
        result.task_type
        == CodingTaskType.EXPLAIN
    )

    assert (
        str(source_file.resolve())
        in result.files_inspected
    )
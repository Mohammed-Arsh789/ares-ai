from core.results import (
    ToolResult,
    AgentResult,
    ExecutionResult,
    ResultStatus,
)

from core.result_normalizer import (
    normalize_tool_result,
    normalize_agent_result,
)


def test_tool_result_success():
    result = ToolResult.ok("calculator", 25)

    assert result.success is True
    assert result.status == ResultStatus.SUCCESS
    assert result.data == 25
    assert result.tool == "calculator"


def test_tool_result_failure():
    result = ToolResult.fail("calculator", "Invalid expression")

    assert result.success is False
    assert result.error == "Invalid expression"


def test_agent_result_success():
    result = AgentResult.ok("research", "Research complete")

    assert result.success is True
    assert result.agent == "research"
    assert result.output == "Research complete"


def test_execution_result_success():
    result = ExecutionResult.ok(
        source="tool",
        name="weather",
        output={"temperature": 28},
    )

    assert result.success is True
    assert result.source == "tool"
    assert result.name == "weather"


def test_tool_normalization():
    result = normalize_tool_result(
        "calculator",
        ToolResult.ok("calculator", 100),
    )

    assert result.success is True
    assert result.output == 100
    assert result.source == "tool"


def test_agent_normalization():
    result = normalize_agent_result(
        "research",
        AgentResult.ok("research", "finished"),
    )

    assert result.success is True
    assert result.output == "finished"
    assert result.source == "agent"


def test_plain_value_normalization():
    result = normalize_tool_result("calculator", 55)

    assert result.success is True
    assert result.output == 55
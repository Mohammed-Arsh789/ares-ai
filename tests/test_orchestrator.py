from core.orchestrator import Orchestrator
from core.router import Router
from tools.registry import ToolRegistry
from tools.test_tool import EchoTool


def main():

    registry = ToolRegistry()

    registry.register(
        EchoTool()
    )

    router = Router(
        registry
    )

    orchestrator = Orchestrator(
        router
    )

    result = orchestrator.analyze(
        "What is the weather today?"
    )

    print(
        "INPUT:"
    )

    print(
        result["input"]
    )

    print()

    print(
        "INTENT:"
    )

    print(
        result["intent"]
    )

    print()

    print(
        "AMBIGUITY:"
    )

    print(
        result["ambiguity"]
    )

    print()

    print(
        "TASK:"
    )

    print(
        result["task"]
    )

    assert (
        result["intent"]["type"]
        == "weather"
    )

    assert result["task"] is not None

    print()
    print(
        "ORCHESTRATOR PASSED"
    )


if __name__ == "__main__":
    main()
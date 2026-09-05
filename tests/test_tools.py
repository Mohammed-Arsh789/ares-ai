from tools.registry import ToolRegistry
from tools.test_tool import EchoTool


def main():

    registry = ToolRegistry()

    echo = EchoTool()

    registry.register(echo)

    print(
        "Tools:"
    )

    print(
        registry.list_tools()
    )

    result = registry.get(
        "echo"
    ).execute(
        text="ARES tool test"
    )

    print()
    print("Result:")
    print(result)

    assert registry.has("echo")

    assert result["success"] is True

    print()
    print("TOOL REGISTRY PASSED")


if __name__ == "__main__":
    main()
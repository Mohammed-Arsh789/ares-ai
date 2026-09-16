from agents import MultiAgentCoordinator


class EchoAgent:
    def run(self, data):
        return f"processed: {data}"


def test_agent_pipeline():
    coordinator = MultiAgentCoordinator()
    coordinator.register("echo", EchoAgent())

    result = coordinator.run_pipeline(
        [
            ("echo", "hello"),
            ("echo", "world"),
        ]
    )

    assert result.success is True
    assert len(result.outputs) == 2
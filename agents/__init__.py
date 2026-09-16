from .models import AgentTask
from .registry import AgentRegistry
from .workflow import WorkflowExecutor


class MultiAgentCoordinator:
    def __init__(
        self,
        registry: AgentRegistry | None = None,
    ):
        self.registry = registry or AgentRegistry()
        self.executor = WorkflowExecutor(self.registry)

    def register(self, name: str, agent):
        self.registry.register(name, agent)

    def run_pipeline(
        self,
        pipeline: list[tuple[str, object]],
    ):
        tasks = [
            AgentTask(
                task_id=f"task-{index}",
                agent_name=agent_name,
                input_data=input_data,
            )
            for index, (agent_name, input_data)
            in enumerate(pipeline, start=1)
        ]

        return self.executor.execute(tasks)
from .models import AgentStatus, AgentTask, WorkflowResult


class WorkflowExecutor:
    """
    Executes agent tasks sequentially.
    """

    def __init__(self, registry):
        self.registry = registry

    def execute(
        self,
        tasks: list[AgentTask],
    ) -> WorkflowResult:
        outputs = []
        errors = []

        for task in tasks:
            agent = self.registry.get(task.agent_name)

            if agent is None:
                task.status = AgentStatus.FAILED
                task.error = (
                    f"Unknown agent: {task.agent_name}"
                )
                errors.append(task.error)
                continue

            task.status = AgentStatus.RUNNING

            try:
                if hasattr(agent, "run"):
                    result = agent.run(task.input_data)
                elif hasattr(agent, "review"):
                    result = agent.review(task.input_data)
                else:
                    raise AttributeError(
                        "Agent has no supported execution method."
                    )

                task.output_data = result
                task.status = AgentStatus.COMPLETED
                outputs.append(result)

            except Exception as error:
                task.status = AgentStatus.FAILED
                task.error = str(error)
                errors.append(str(error))

        return WorkflowResult(
            success=len(errors) == 0,
            outputs=outputs,
            errors=errors,
        )
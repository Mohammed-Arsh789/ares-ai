from .models import AutomationTask


class AutomationEngine:
    def __init__(self, action_registry):
        self.action_registry = action_registry

    def execute_task(
        self,
        task: AutomationTask,
    ):
        if not task.enabled:
            return {
                "success": False,
                "reason": "Task is disabled.",
            }

        if not self.action_registry.has(task.action_name):
            return {
                "success": False,
                "reason": "Action is not registered.",
            }

        result = self.action_registry.execute(
            task.action_name,
            **task.metadata,
        )

        task.mark_run()

        return {
            "success": True,
            "result": result,
            "task_id": task.task_id,
            "run_count": task.run_count,
        }
"""
ARES Automation Manager

Stores and manages automation tasks.
"""

from __future__ import annotations

from .models import AutomationTask


class AutomationManager:
    def __init__(self):
        self._tasks: dict[str, AutomationTask] = {}

    def add_task(self, task: AutomationTask) -> None:
        """
        Add a new automation task.
        """
        if not isinstance(task, AutomationTask):
            raise TypeError(
                "task must be an AutomationTask instance."
            )

        if not task.task_id.strip():
            raise ValueError(
                "Automation task ID cannot be empty."
            )

        if task.task_id in self._tasks:
            raise ValueError(
                f"Task already exists: {task.task_id}"
            )

        self._tasks[task.task_id] = task

    def get_task(self, task_id: str) -> AutomationTask | None:
        """
        Retrieve a task by ID.
        """
        return self._tasks.get(task_id)

    def remove_task(self, task_id: str) -> None:
        """
        Remove a task by ID.
        """
        self._tasks.pop(task_id, None)

    def list_tasks(self) -> list[AutomationTask]:
        """
        Return all automation tasks.
        """
        return list(self._tasks.values())

    def enable_task(self, task_id: str) -> bool:
        """
        Enable an existing task.
        """
        task = self.get_task(task_id)

        if task is None:
            return False

        task.enabled = True
        return True

    def disable_task(self, task_id: str) -> bool:
        """
        Disable an existing task.
        """
        task = self.get_task(task_id)

        if task is None:
            return False

        task.enabled = False
        return True

    def count(self) -> int:
        """
        Return the number of stored tasks.
        """
        return len(self._tasks)
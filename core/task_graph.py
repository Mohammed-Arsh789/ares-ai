from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Set

from .task import Plan, Task, TaskStatus


class TaskGraphError(Exception):
    """Base exception for task graph problems."""


class TaskNotFoundError(TaskGraphError):
    """Raised when a requested task does not exist."""


class DependencyCycleError(TaskGraphError):
    """Raised when task dependencies contain a cycle."""


class TaskGraph:
    """
    Dependency graph for ARES tasks.

    Example:

        A
        |
        v
        B
        |
        v
        C

    B cannot run until A succeeds.
    C cannot run until B succeeds.
    """

    def __init__(self, plan: Optional[Plan] = None):
        self.tasks: Dict[str, Task] = {}

        if plan is not None:
            self.load_plan(plan)

    def load_plan(self, plan: Plan) -> None:
        self.tasks.clear()

        for task in plan.tasks:
            self.add_task(task)

        self.validate()

    def add_task(self, task: Task) -> None:
        if task.task_id in self.tasks:
            raise ValueError(f"Duplicate task ID: {task.task_id}")

        self.tasks[task.task_id] = task

    def get(self, task_id: str) -> Task:
        try:
            return self.tasks[task_id]
        except KeyError:
            raise TaskNotFoundError(
                f"Task '{task_id}' does not exist."
            ) from None

    def has(self, task_id: str) -> bool:
        return task_id in self.tasks

    def all_tasks(self) -> List[Task]:
        return list(self.tasks.values())

    def dependencies_satisfied(self, task_id: str) -> bool:
        task = self.get(task_id)

        for dependency_id in task.dependencies:
            dependency = self.get(dependency_id)

            if dependency.status != TaskStatus.SUCCESS:
                return False

        return True

    def dependency_failed(self, task_id: str) -> bool:
        task = self.get(task_id)

        failure_states = {
            TaskStatus.FAILURE,
            TaskStatus.CANCELLED,
            TaskStatus.BLOCKED,
        }

        return any(
            self.get(dependency_id).status in failure_states
            for dependency_id in task.dependencies
        )

    def ready_tasks(self) -> List[Task]:
        """
        Return tasks whose dependencies have all succeeded.
        """
        ready: List[Task] = []

        for task in self.tasks.values():
            if task.status != TaskStatus.PENDING:
                continue

            if self.dependency_failed(task.task_id):
                task.mark_blocked(
                    "A dependency failed, was cancelled, or was blocked."
                )
                continue

            if self.dependencies_satisfied(task.task_id):
                task.mark_ready()
                ready.append(task)

        return ready

    def validate(self) -> None:
        """
        Validate references and detect dependency cycles.
        """
        for task in self.tasks.values():
            for dependency_id in task.dependencies:
                if dependency_id not in self.tasks:
                    raise TaskGraphError(
                        f"Task '{task.task_id}' depends on unknown "
                        f"task '{dependency_id}'."
                    )

                if dependency_id == task.task_id:
                    raise TaskGraphError(
                        f"Task '{task.task_id}' cannot depend on itself."
                    )

        self._detect_cycles()

    def _detect_cycles(self) -> None:
        visiting: Set[str] = set()
        visited: Set[str] = set()

        def visit(task_id: str) -> None:
            if task_id in visiting:
                raise DependencyCycleError(
                    f"Dependency cycle detected at task '{task_id}'."
                )

            if task_id in visited:
                return

            visiting.add(task_id)

            for dependency_id in self.tasks[task_id].dependencies:
                visit(dependency_id)

            visiting.remove(task_id)
            visited.add(task_id)

        for task_id in self.tasks:
            visit(task_id)

    def execution_order(self) -> List[Task]:
        """
        Return a deterministic topological execution order.
        """
        self.validate()

        remaining = set(self.tasks.keys())
        ordered: List[Task] = []

        while remaining:
            progress = False

            for task_id in list(remaining):
                task = self.tasks[task_id]

                if all(
                    dependency_id not in remaining
                    for dependency_id in task.dependencies
                ):
                    ordered.append(task)
                    remaining.remove(task_id)
                    progress = True

            if not progress:
                raise DependencyCycleError(
                    "Unable to calculate execution order."
                )

        return ordered

    def is_complete(self) -> bool:
        return all(task.is_complete() for task in self.tasks.values())

    def has_failures(self) -> bool:
        return any(
            task.status in {
                TaskStatus.FAILURE,
                TaskStatus.BLOCKED,
                TaskStatus.CANCELLED,
            }
            for task in self.tasks.values()
        )

    def summary(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}

        for task in self.tasks.values():
            key = task.status.value
            counts[key] = counts.get(key, 0) + 1

        return counts
from __future__ import annotations

import time
from typing import Any, Optional

from core.execution import ExecutionContext
from core.planner import Planner
from core.result_normalizer import (
    normalize_failure,
    normalize_tool_result,
)
from core.results import ExecutionResult, ResultStatus
from core.task import Plan, Task, TaskStatus
from core.task_graph import TaskGraph


class Orchestrator:
    """
    Executes plans produced by the ARES planner.

    Responsibilities:
    - Validate task dependencies.
    - Execute ready tasks.
    - Respect confirmation requirements.
    - Support dry-run execution.
    - Normalize tool results.
    - Convert failures into structured ExecutionResult objects.
    - Produce execution summaries.
    """

    def __init__(
        self,
        registry: Any = None,
        planner: Optional[Planner] = None,
    ) -> None:
        self.registry = registry
        self.planner = planner or Planner()

    # ------------------------------------------------------------------
    # PLAN EXECUTION
    # ------------------------------------------------------------------

    def execute_plan(
        self,
        plan: Plan,
        context: Optional[ExecutionContext] = None,
        dry_run: bool = False,
    ) -> ExecutionResult:
        """
        Execute every task in a plan while respecting dependencies.
        """

        context = context or ExecutionContext()
        graph = TaskGraph(plan)

        try:
            graph.validate()
        except Exception as exc:
            return normalize_failure(
                "orchestrator",
                "plan_validation",
                str(exc),
            )

        results: list[ExecutionResult] = []
        started = time.perf_counter()

        while not graph.is_complete():

            ready_tasks = graph.ready_tasks()

            if not ready_tasks:
                remaining = [
                    task.name
                    for task in graph.all_tasks()
                    if task.status
                    in {
                        TaskStatus.PENDING,
                        TaskStatus.READY,
                        TaskStatus.BLOCKED,
                    }
                ]

                return ExecutionResult.fail(
                    name="plan",
                    error=(
                        "Execution stopped because no executable "
                        f"tasks remain. Pending tasks: {remaining}"
                    ),
                    source="orchestrator",
                    metadata={
                        "completed_results": [
                            result.to_dict()
                            for result in results
                        ],
                        "summary": self._build_summary(results),
                    },
                    duration_ms=round(
                        (time.perf_counter() - started) * 1000,
                        2,
                    ),
                )

            for task in ready_tasks:
                result = self.execute_task(
                    task=task,
                    context=context,
                    dry_run=dry_run,
                )

                results.append(result)

        # --------------------------------------------------------------
        # SUMMARY
        # --------------------------------------------------------------

        summary = self._build_summary(results)

        success = summary["failure"] == 0

        output = {
            "plan_id": plan.plan_id,
            "goal": plan.goal,
            "results": [
                result.to_dict()
                for result in results
            ],
            "summary": summary,
        }

        # --------------------------------------------------------------
        # SUCCESSFUL PLAN
        # --------------------------------------------------------------

        if success:
            return ExecutionResult(
                success=True,
                status=ResultStatus.SUCCESS,
                output=output,
                error=None,
                metadata={
                    "task_count": summary["total"],
                    "successful_tasks": summary["success"],
                    "failed_tasks": summary["failure"],
                    "dry_run": dry_run,
                },
                source="orchestrator",
                name="plan",
                task_id=plan.plan_id,
                attempts=1,
                duration_ms=round(
                    (time.perf_counter() - started) * 1000,
                    2,
                ),
            )

        # --------------------------------------------------------------
        # PARTIAL / FAILED PLAN
        # --------------------------------------------------------------

        return ExecutionResult(
            success=False,
            status=ResultStatus.PARTIAL,
            output=output,
            error="One or more tasks failed.",
            metadata={
                "task_count": summary["total"],
                "successful_tasks": summary["success"],
                "failed_tasks": summary["failure"],
                "dry_run": dry_run,
            },
            source="orchestrator",
            name="plan",
            task_id=plan.plan_id,
            attempts=1,
            duration_ms=round(
                (time.perf_counter() - started) * 1000,
                2,
            ),
        )

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------

    @staticmethod
    def _build_summary(
        results: list[ExecutionResult],
    ) -> dict[str, int]:
        """
        Build a compact execution summary.

        Example:

        {
            "total": 3,
            "success": 2,
            "failure": 1
        }
        """

        success_count = sum(
            1
            for result in results
            if result.success
        )

        failure_count = len(results) - success_count

        return {
            "total": len(results),
            "success": success_count,
            "failure": failure_count,
        }

    # ------------------------------------------------------------------
    # SINGLE TASK EXECUTION
    # ------------------------------------------------------------------

    def execute_task(
        self,
        task: Task,
        context: ExecutionContext,
        dry_run: bool = False,
    ) -> ExecutionResult:

        start = time.perf_counter()

        if task.status not in {
            TaskStatus.READY,
            TaskStatus.PENDING,
        }:
            return ExecutionResult.fail(
                name=task.name,
                error=(
                    f"Task cannot execute from status "
                    f"'{task.status.value}'."
                ),
                source="orchestrator",
                task_id=task.task_id,
            )

        # --------------------------------------------------------------
        # CONFIRMATION
        # --------------------------------------------------------------

        if task.requires_confirmation and not self._confirmed(context):
            task.mark_blocked(
                "Task requires confirmation."
            )

            return ExecutionResult(
                success=False,
                status=ResultStatus.DENIED,
                output=None,
                error="Task requires confirmation.",
                metadata={
                    "confirmation_required": True
                },
                source="orchestrator",
                name=task.name,
                task_id=task.task_id,
                attempts=0,
                duration_ms=round(
                    (time.perf_counter() - start) * 1000,
                    2,
                ),
            )

        task.mark_running()

        # --------------------------------------------------------------
        # DRY RUN
        # --------------------------------------------------------------

        if dry_run:
            preview = {
                "task_id": task.task_id,
                "name": task.name,
                "tool": task.tool,
                "arguments": dict(task.arguments),
                "dry_run": True,
            }

            task.mark_success(preview)

            return ExecutionResult(
                success=True,
                status=ResultStatus.SUCCESS,
                output=preview,
                error=None,
                metadata={
                    "dry_run": True
                },
                source="orchestrator",
                name=task.name,
                task_id=task.task_id,
                attempts=1,
                duration_ms=round(
                    (time.perf_counter() - start) * 1000,
                    2,
                ),
            )

        # --------------------------------------------------------------
        # REAL EXECUTION
        # --------------------------------------------------------------

        try:
            result = self._dispatch(
                task,
                context,
            )

            normalized = normalize_tool_result(
                task.tool or task.name,
                result,
            )

            if normalized.success:
                task.mark_success(
                    normalized.output
                )
            else:
                task.mark_failure(
                    normalized.error
                    or "Tool execution failed."
                )

            return ExecutionResult(
                success=normalized.success,
                status=normalized.status,
                output=normalized.output,
                error=normalized.error,
                metadata=dict(normalized.metadata),
                source="orchestrator",
                name=task.name,
                task_id=task.task_id,
                attempts=1,
                duration_ms=round(
                    (time.perf_counter() - start) * 1000,
                    2,
                ),
            )

        except Exception as exc:

            task.mark_failure(str(exc))

            failure = normalize_failure(
                "orchestrator",
                task.name,
                str(exc),
            )

            return ExecutionResult(
                success=failure.success,
                status=failure.status,
                output=failure.output,
                error=failure.error,
                metadata=dict(failure.metadata),
                source="orchestrator",
                name=task.name,
                task_id=task.task_id,
                attempts=1,
                duration_ms=round(
                    (time.perf_counter() - start) * 1000,
                    2,
                ),
            )

    # ------------------------------------------------------------------
    # DISPATCH
    # ------------------------------------------------------------------

    def _dispatch(
        self,
        task: Task,
        context: ExecutionContext,
    ) -> Any:

        if not task.tool:
            raise ValueError(
                f"Task '{task.name}' has no tool."
            )

        # Agent tasks will be connected during the
        # agent-orchestration stage.
        if task.tool.startswith("agent:"):
            raise NotImplementedError(
                f"Agent execution is not connected yet: "
                f"{task.tool}"
            )

        if task.tool == "conversation":
            raise NotImplementedError(
                "Conversation execution is not connected "
                "to the orchestrator yet."
            )

        if task.tool == "help":
            raise NotImplementedError(
                "Help execution is not connected "
                "to the orchestrator yet."
            )

        if self.registry is None:
            raise RuntimeError(
                "No tool registry is configured."
            )

        # Preferred structured registry API.
        if hasattr(self.registry, "execute_result"):
            return self.registry.execute_result(
                task.tool,
                **dict(task.arguments),
            )

        # Compatibility with older registries.
        if hasattr(self.registry, "execute"):
            return self.registry.execute(
                task.tool,
                **dict(task.arguments),
            )

        raise RuntimeError(
            "Configured registry does not provide "
            "'execute_result' or 'execute'."
        )

    # ------------------------------------------------------------------
    # CONFIRMATION
    # ------------------------------------------------------------------

    @staticmethod
    def _confirmed(
        context: ExecutionContext,
    ) -> bool:

        permissions = context.permissions

        if isinstance(permissions, dict):
            return bool(
                permissions.get("confirmed")
                or permissions.get("allow_sensitive")
            )

        if isinstance(permissions, set):
            return (
                "confirmed" in permissions
                or "allow_sensitive" in permissions
            )

        if isinstance(permissions, (list, tuple)):
            return (
                "confirmed" in permissions
                or "allow_sensitive" in permissions
            )

        return False


# Compatibility alias.
OrchestratorV2 = Orchestrator
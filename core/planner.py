"""
ARES Planner
Step 171

Creates an executable task plan.

Important:
The planner DOES NOT execute tools.
It only creates a plan.

Execution will be handled by the router later.
"""

from __future__ import annotations

import uuid

from .intent import Intent
from .task import Task, TaskStatus


class Planner:

    def create_plan(
        self,
        user_input: str,
        intent: Intent,
    ) -> Task:

        task = Task(
            id=str(uuid.uuid4()),
            description=user_input,
            intent=intent.type.value,
            status=TaskStatus.READY,
        )

        if intent.requires_tool:

            task.steps.append(
                {
                    "action": "select_tool",
                    "status": "pending",
                }
            )

            task.steps.append(
                {
                    "action": "validate_permissions",
                    "status": "pending",
                }
            )

            task.steps.append(
                {
                    "action": "execute_tool",
                    "status": "pending",
                }
            )

            task.steps.append(
                {
                    "action": "validate_result",
                    "status": "pending",
                }
            )

        else:

            task.steps.append(
                {
                    "action": "generate_response",
                    "status": "pending",
                }
            )

        return task
from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from typing import Any


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class CognitiveState:
    """
    Represents ARES's current task and reasoning state.

    CognitiveState is short-lived operational state.

    It describes what ARES is currently doing, what it currently
    knows about the task, what it has attempted, and what happened.

    It is intentionally separate from long-term memory.
    """

    task_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    session_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    current_goal: str = ""

    current_step: int = 0

    active_plan: Any = None

    pending_actions: list[Any] = field(
        default_factory=list
    )

    observations: list[Any] = field(
        default_factory=list
    )

    constraints: list[Any] = field(
        default_factory=list
    )

    facts: list[Any] = field(
        default_factory=list
    )

    last_decision: Any = None

    last_tool_result: Any = None

    failure_count: int = 0

    recovery_count: int = 0

    status: str = "idle"

    def set_goal(
        self,
        goal: str,
    ) -> None:
        """
        Set the current task goal.
        """

        if not isinstance(goal, str):
            raise TypeError(
                "goal must be a string."
            )

        self.current_goal = goal.strip()

        logger.debug(
            "Cognitive goal updated: %s",
            self.current_goal,
        )

    def set_step(
        self,
        step: int,
    ) -> None:
        """
        Set the current reasoning/task step.
        """

        if not isinstance(step, int):
            raise TypeError(
                "step must be an integer."
            )

        if step < 0:
            raise ValueError(
                "step cannot be negative."
            )

        self.current_step = step

    def advance_step(self) -> int:
        """
        Advance to the next task step.

        Returns the new step number.
        """

        self.current_step += 1

        return self.current_step

    def set_plan(
        self,
        plan: Any,
    ) -> None:
        """
        Set the currently active plan.
        """

        self.active_plan = plan

    def add_pending_action(
        self,
        action: Any,
    ) -> None:
        """
        Add an action that still needs to be executed.
        """

        self.pending_actions.append(action)

    def remove_pending_action(
        self,
        action: Any,
    ) -> bool:
        """
        Remove a pending action.

        Returns True if the action was present.
        """

        try:
            self.pending_actions.remove(action)
            return True
        except ValueError:
            return False

    def clear_pending_actions(self) -> None:
        """
        Remove all pending actions.
        """

        self.pending_actions.clear()

    def add_observation(
        self,
        observation: Any,
    ) -> None:
        """
        Record a new observation from the environment,
        tool system, or verification layer.
        """

        self.observations.append(observation)

    def add_constraint(
        self,
        constraint: Any,
    ) -> None:
        """
        Record a constraint relevant to the current task.
        """

        self.constraints.append(constraint)

    def add_fact(
        self,
        fact: Any,
    ) -> None:
        """
        Record a fact relevant to the current task.
        """

        self.facts.append(fact)

    def set_decision(
        self,
        decision: Any,
    ) -> None:
        """
        Store the most recent cognitive decision.
        """

        self.last_decision = decision

    def set_tool_result(
        self,
        result: Any,
    ) -> None:
        """
        Store the most recent tool execution result.
        """

        self.last_tool_result = result

    def record_failure(self) -> int:
        """
        Record a failed operation.

        Returns the updated failure count.
        """

        self.failure_count += 1

        return self.failure_count

    def record_recovery(self) -> int:
        """
        Record a recovery attempt.

        Returns the updated recovery count.
        """

        self.recovery_count += 1

        return self.recovery_count

    def set_status(
        self,
        status: str,
    ) -> None:
        """
        Update the current cognitive state status.
        """

        if not isinstance(status, str):
            raise TypeError(
                "status must be a string."
            )

        normalized = status.strip().lower()

        if not normalized:
            raise ValueError(
                "status cannot be empty."
            )

        self.status = normalized

    def reset_task(
        self,
        *,
        keep_session: bool = True,
    ) -> None:
        """
        Reset task-specific state.

        By default the current session is preserved while a new
        task identifier is generated.
        """

        self.task_id = str(uuid.uuid4())

        if not keep_session:
            self.session_id = str(uuid.uuid4())

        self.current_goal = ""
        self.current_step = 0
        self.active_plan = None

        self.pending_actions.clear()
        self.observations.clear()
        self.constraints.clear()
        self.facts.clear()

        self.last_decision = None
        self.last_tool_result = None

        self.failure_count = 0
        self.recovery_count = 0

        self.status = "idle"

    def snapshot(self) -> dict[str, Any]:
        """
        Return a serializable snapshot of the current state.

        The snapshot is intended for logging, debugging,
        context construction, and future persistence.
        """

        return {
            "task_id": self.task_id,
            "session_id": self.session_id,
            "current_goal": self.current_goal,
            "current_step": self.current_step,
            "active_plan": self.active_plan,
            "pending_actions": list(
                self.pending_actions
            ),
            "observations": list(
                self.observations
            ),
            "constraints": list(
                self.constraints
            ),
            "facts": list(
                self.facts
            ),
            "last_decision": self.last_decision,
            "last_tool_result": self.last_tool_result,
            "failure_count": self.failure_count,
            "recovery_count": self.recovery_count,
            "status": self.status,
        }

    def clear(self) -> None:
        """
        Clear all task and session state.

        This creates a fresh state while preserving the
        object itself.
        """

        self.reset_task(
            keep_session=False
        )
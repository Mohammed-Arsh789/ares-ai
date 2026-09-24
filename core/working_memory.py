from __future__ import annotations

import logging
from collections import deque
from typing import Any


logger = logging.getLogger(__name__)


class WorkingMemory:
    """
    Short-lived memory used by ARES while handling the
    current task or reasoning cycle.

    Working memory is intentionally separate from long-term
    memory.

    It stores temporary information such as:

    - recent facts
    - recent observations
    - pending actions
    - temporary context

    The memory is bounded so it cannot grow indefinitely.
    """

    def __init__(
        self,
        *,
        max_facts: int = 20,
        max_observations: int = 20,
        max_pending_actions: int = 10,
    ) -> None:
        if max_facts <= 0:
            raise ValueError(
                "max_facts must be greater than zero."
            )

        if max_observations <= 0:
            raise ValueError(
                "max_observations must be greater than zero."
            )

        if max_pending_actions <= 0:
            raise ValueError(
                "max_pending_actions must be greater than zero."
            )

        self.max_facts = max_facts
        self.max_observations = max_observations
        self.max_pending_actions = max_pending_actions

        self._facts: deque[Any] = deque(
            maxlen=max_facts
        )

        self._observations: deque[Any] = deque(
            maxlen=max_observations
        )

        self._pending_actions: deque[Any] = deque(
            maxlen=max_pending_actions
        )

    # ------------------------------------------------------------------
    # Facts
    # ------------------------------------------------------------------

    def add_fact(
        self,
        fact: Any,
    ) -> None:
        """
        Add a temporary fact to working memory.

        If the memory is full, the oldest fact is automatically
        discarded.
        """

        self._facts.append(fact)

        logger.debug(
            "Working memory fact added."
        )

    def get_facts(
        self,
        limit: int | None = None,
    ) -> list[Any]:
        """
        Return recent facts.

        Results are returned oldest-to-newest.
        """

        facts = list(self._facts)

        if limit is None:
            return facts

        if limit <= 0:
            return []

        return facts[-limit:]

    # ------------------------------------------------------------------
    # Observations
    # ------------------------------------------------------------------

    def add_observation(
        self,
        observation: Any,
    ) -> None:
        """
        Add a temporary observation.
        """

        self._observations.append(
            observation
        )

        logger.debug(
            "Working memory observation added."
        )

    def get_observations(
        self,
        limit: int | None = None,
    ) -> list[Any]:
        """
        Return recent observations.

        Results are returned oldest-to-newest.
        """

        observations = list(
            self._observations
        )

        if limit is None:
            return observations

        if limit <= 0:
            return []

        return observations[-limit:]

    # ------------------------------------------------------------------
    # Pending actions
    # ------------------------------------------------------------------

    def add_pending_action(
        self,
        action: Any,
    ) -> None:
        """
        Add an action that remains to be executed.
        """

        self._pending_actions.append(
            action
        )

        logger.debug(
            "Working memory pending action added."
        )

    def get_pending_actions(
        self,
        limit: int | None = None,
    ) -> list[Any]:
        """
        Return pending actions.
        """

        actions = list(
            self._pending_actions
        )

        if limit is None:
            return actions

        if limit <= 0:
            return []

        return actions[-limit:]

    def remove_pending_action(
        self,
        action: Any,
    ) -> bool:
        """
        Remove a pending action.

        Returns True when the action existed.
        """

        try:
            self._pending_actions.remove(
                action
            )
            return True
        except ValueError:
            return False

    # ------------------------------------------------------------------
    # Temporary context
    # ------------------------------------------------------------------

    def add(
        self,
        *,
        fact: Any = None,
        observation: Any = None,
        pending_action: Any = None,
    ) -> None:
        """
        Convenience method for adding one or more
        working-memory items.
        """

        if fact is not None:
            self.add_fact(fact)

        if observation is not None:
            self.add_observation(
                observation
            )

        if pending_action is not None:
            self.add_pending_action(
                pending_action
            )

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def snapshot(self) -> dict[str, list[Any]]:
        """
        Return the current working-memory contents.
        """

        return {
            "facts": self.get_facts(),
            "observations": self.get_observations(),
            "pending_actions": self.get_pending_actions(),
        }

    def is_empty(self) -> bool:
        """
        Return True when working memory contains nothing.
        """

        return not (
            self._facts
            or self._observations
            or self._pending_actions
        )

    # ------------------------------------------------------------------
    # Clearing
    # ------------------------------------------------------------------

    def clear_facts(self) -> None:
        """
        Clear temporary facts.
        """

        self._facts.clear()

    def clear_observations(self) -> None:
        """
        Clear temporary observations.
        """

        self._observations.clear()

    def clear_pending_actions(self) -> None:
        """
        Clear all pending actions.
        """

        self._pending_actions.clear()

    def clear(self) -> None:
        """
        Completely clear working memory.
        """

        self.clear_facts()
        self.clear_observations()
        self.clear_pending_actions()

        logger.debug(
            "Working memory cleared."
        )

    # ------------------------------------------------------------------
    # Length helpers
    # ------------------------------------------------------------------

    @property
    def fact_count(self) -> int:
        return len(self._facts)

    @property
    def observation_count(self) -> int:
        return len(self._observations)

    @property
    def pending_action_count(self) -> int:
        return len(self._pending_actions)

    def __len__(self) -> int:
        """
        Return the total number of items currently
        held in working memory.
        """

        return (
            self.fact_count
            + self.observation_count
            + self.pending_action_count
        )
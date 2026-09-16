"""
ARES Agent Registry

Stores and retrieves named agent instances for the multi-agent system.
"""

from __future__ import annotations

from typing import Any


class AgentRegistry:
    def __init__(self):
        self._agents: dict[str, Any] = {}

    def register(self, name: str, agent: Any) -> None:
        """
        Register an agent under a unique name.
        """
        if not isinstance(name, str):
            raise TypeError("Agent name must be a string.")

        name = name.strip()

        if not name:
            raise ValueError("Agent name cannot be empty.")

        if agent is None:
            raise ValueError("Agent cannot be None.")

        if name in self._agents:
            raise ValueError(
                f"Agent already registered: {name}"
            )

        self._agents[name] = agent

    def get(self, name: str) -> Any | None:
        """
        Retrieve an agent by name.
        """
        return self._agents.get(name)

    def has(self, name: str) -> bool:
        """
        Check whether an agent exists.
        """
        return name in self._agents

    def unregister(self, name: str) -> None:
        """
        Remove an agent if it exists.
        """
        self._agents.pop(name, None)

    def names(self) -> list[str]:
        """
        Return all registered agent names.
        """
        return list(self._agents.keys())

    def count(self) -> int:
        """
        Return the number of registered agents.
        """
        return len(self._agents)
from __future__ import annotations

import logging
from typing import Any


logger = logging.getLogger(__name__)


class MemoryBridge:
    """
    Adapter between the Brain and the existing ARES memory system.

    The bridge intentionally supports multiple memory APIs so the
    underlying memory implementation can evolve independently.
    """

    def __init__(
        self,
        memory: Any | None = None,
    ) -> None:
        self.memory = memory

    def remember(
        self,
        *,
        user_input: str,
        response: str,
        decision: Any = None,
        result: Any = None,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """
        Store a completed interaction.

        Returns True when the memory system accepted the entry.
        """

        if self.memory is None:
            return False

        entry = {
            "type": "interaction",
            "user_input": user_input,
            "response": response,
            "decision": self._serialize(
                decision
            ),
            "result": self._serialize(
                result
            ),
            "context": context or {},
        }

        try:
            if hasattr(
                self.memory,
                "store",
            ):
                self.memory.store(entry)
                return True

            if hasattr(
                self.memory,
                "remember",
            ):
                self.memory.remember(entry)
                return True

            if hasattr(
                self.memory,
                "add",
            ):
                self.memory.add(entry)
                return True

            if hasattr(
                self.memory,
                "save",
            ):
                self.memory.save(entry)
                return True

        except Exception:
            logger.exception(
                "Failed to store interaction memory."
            )
            return False

        logger.warning(
            "Memory system has no supported write interface."
        )

        return False

    @staticmethod
    def _serialize(
        value: Any,
    ) -> Any:
        if value is None:
            return None

        if isinstance(
            value,
            (
                str,
                int,
                float,
                bool,
            ),
        ):
            return value

        if isinstance(
            value,
            dict,
        ):
            return value

        if hasattr(
            value,
            "__dict__",
        ):
            try:
                return vars(value)
            except TypeError:
                pass

        return str(value)
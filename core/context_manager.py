from __future__ import annotations

import logging
from typing import Any

from .cognitive_context import CognitiveContext


logger = logging.getLogger(__name__)


class ContextManager:
    """
    Builds the cognitive context supplied to ARES.

    The ContextManager gathers information from multiple sources:

        User Input
            +
        Recent Conversation
            +
        Relevant Memories
            +
        Session Context
            +
        Current Intent
            +
        Available Tools
            ↓
        CognitiveContext

    This layer does NOT make decisions.

    Its job is to collect, normalize, limit, and safely package
    information before the Cognitive Core reasons about it.
    """

    def __init__(
        self,
        memory: Any = None,
        conversation: Any = None,
        tool_registry: Any = None,
        max_messages: int = 10,
        max_memories: int = 8,
    ) -> None:
        """
        Initialize the ContextManager.

        Args:
            memory:
                Memory system used for retrieving relevant memories.

            conversation:
                Conversation/history provider.

            tool_registry:
                Registry containing currently available ARES tools.

            max_messages:
                Maximum number of recent conversation messages.

            max_memories:
                Maximum number of memories supplied to cognition.
        """

        self.memory = memory
        self.conversation = conversation
        self.tool_registry = tool_registry

        self.max_messages = max(
            0,
            int(max_messages),
        )

        self.max_memories = max(
            0,
            int(max_memories),
        )

    # ==================================================================
    # BUILD COGNITIVE CONTEXT
    # ==================================================================

    def build(
        self,
        user_input: str,
        *,
        session_context: dict[str, Any] | None = None,
        intent: Any = None,
    ) -> CognitiveContext:
        """
        Build a CognitiveContext for the current request.

        This is the primary entry point used by the ARES Brain.
        """

        recent_messages = self._get_recent_messages()

        memories = self._retrieve_memories(
            user_input
        )

        available_tools = self._get_available_tools()

        context = CognitiveContext(
            user_input=user_input,
            recent_messages=recent_messages,
            memories=memories,
            session_context=dict(
                session_context or {}
            ),
            intent=self._serialize(intent),
            available_tools=available_tools,
            metadata={
                "message_count": len(
                    recent_messages
                ),
                "memory_count": len(
                    memories
                ),
                "tool_count": len(
                    available_tools
                ),
            },
        )

        return context

    # ==================================================================
    # RECENT CONVERSATION
    # ==================================================================

    def _get_recent_messages(self) -> list[Any]:
        """
        Retrieve recent conversation history.

        Supports multiple conversation interfaces:

            recent(limit)
            get_recent(limit)
            history(limit)

        If the conversation provider fails, the Brain continues with
        an empty conversation context.
        """

        if self.conversation is None:
            return []

        try:

            result = None

            if hasattr(
                self.conversation,
                "recent",
            ):
                result = self.conversation.recent(
                    self.max_messages
                )

            elif hasattr(
                self.conversation,
                "get_recent",
            ):
                result = self.conversation.get_recent(
                    self.max_messages
                )

            elif hasattr(
                self.conversation,
                "history",
            ):
                result = self.conversation.history(
                    self.max_messages
                )

            else:
                logger.debug(
                    "Conversation provider has no supported "
                    "history method."
                )

                return []

            messages = self._normalize_list(
                result
            )

            # ----------------------------------------------------------
            # Hard boundary.
            #
            # A provider might ignore the requested limit, so enforce
            # max_messages here too.
            # ----------------------------------------------------------

            return messages[
                :self.max_messages
            ]

        except Exception:

            logger.exception(
                "Failed to retrieve recent conversation."
            )

            return []

    # ==================================================================
    # MEMORY RETRIEVAL
    # ==================================================================

    def _retrieve_memories(
        self,
        query: str,
    ) -> list[Any]:
        """
        Retrieve memories relevant to the current request.

        Supported memory interfaces:

            search(query, limit=...)
            retrieve(query, limit=...)
            recall(query, limit=...)

        The result is always capped by max_memories.
        """

        if self.memory is None:
            return []

        if self.max_memories <= 0:
            return []

        try:

            result = None

            # ----------------------------------------------------------
            # Preferred interface
            # ----------------------------------------------------------

            if hasattr(
                self.memory,
                "search",
            ):
                try:
                    result = self.memory.search(
                        query,
                        limit=self.max_memories,
                    )
                except TypeError:
                    # Compatibility with implementations that only
                    # accept the query argument.
                    result = self.memory.search(
                        query
                    )

            # ----------------------------------------------------------
            # Alternative interface
            # ----------------------------------------------------------

            elif hasattr(
                self.memory,
                "retrieve",
            ):
                try:
                    result = self.memory.retrieve(
                        query,
                        limit=self.max_memories,
                    )
                except TypeError:
                    result = self.memory.retrieve(
                        query
                    )

            # ----------------------------------------------------------
            # Alternative interface
            # ----------------------------------------------------------

            elif hasattr(
                self.memory,
                "recall",
            ):
                try:
                    result = self.memory.recall(
                        query,
                        limit=self.max_memories,
                    )
                except TypeError:
                    result = self.memory.recall(
                        query
                    )

            else:
                logger.debug(
                    "Memory provider has no supported "
                    "retrieval method."
                )

                return []

            memories = self._normalize_list(
                result
            )

            # ----------------------------------------------------------
            # HARD MEMORY LIMIT
            #
            # Never allow a memory backend to flood the cognitive
            # context even if it ignores the requested limit.
            # ----------------------------------------------------------

            memories = memories[
                :self.max_memories
            ]

            return memories

        except Exception:

            logger.exception(
                "Failed to retrieve memories."
            )

            return []

    # ==================================================================
    # AVAILABLE TOOLS
    # ==================================================================

    def _get_available_tools(self) -> list[str]:
        """
        Retrieve names of tools currently available to ARES.

        Supported registry interfaces:

            names()
            list_tools()
            tools

        Tool objects may expose:

            name
            tool_name
            id
        """

        if self.tool_registry is None:
            return []

        try:

            # ----------------------------------------------------------
            # Registry.names()
            # ----------------------------------------------------------

            if hasattr(
                self.tool_registry,
                "names",
            ):
                names = self.tool_registry.names()

                return [
                    str(name)
                    for name in names
                ]

            # ----------------------------------------------------------
            # Registry.list_tools()
            # ----------------------------------------------------------

            if hasattr(
                self.tool_registry,
                "list_tools",
            ):
                tools = (
                    self.tool_registry.list_tools()
                )

                return [
                    self._tool_name(tool)
                    for tool in tools
                ]

            # ----------------------------------------------------------
            # Registry.tools
            # ----------------------------------------------------------

            if hasattr(
                self.tool_registry,
                "tools",
            ):
                tools = self.tool_registry.tools

                if isinstance(
                    tools,
                    dict,
                ):
                    return [
                        str(name)
                        for name in tools.keys()
                    ]

                return [
                    self._tool_name(tool)
                    for tool in tools
                ]

            logger.debug(
                "Tool registry has no supported "
                "tool discovery interface."
            )

            return []

        except Exception:

            logger.exception(
                "Failed to retrieve available tools."
            )

            return []

    # ==================================================================
    # NORMALIZE LIST
    # ==================================================================

    def _normalize_list(
        self,
        value: Any,
    ) -> list[Any]:
        """
        Normalize an arbitrary value into a list.

        Examples:

            None          → []
            "hello"       → ["hello"]
            tuple         → [...]
            set           → [...]
            list          → [...]
            object        → [object]
        """

        if value is None:
            return []

        if isinstance(
            value,
            list,
        ):
            items = value

        elif isinstance(
            value,
            tuple,
        ):
            items = list(value)

        elif isinstance(
            value,
            set,
        ):
            items = list(value)

        else:
            items = [value]

        return [
            self._serialize(item)
            for item in items
        ]

    # ==================================================================
    # SERIALIZATION
    # ==================================================================

    def _serialize(
        self,
        value: Any,
    ) -> Any:
        """
        Convert common Python/ARES objects into data that can safely
        be placed into a model context.

        Supported:

            primitives
            dictionaries
            lists
            tuples
            sets
            objects with to_dict()
            regular Python objects
        """

        if value is None:
            return None

        # --------------------------------------------------------------
        # Primitive values
        # --------------------------------------------------------------

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

        # --------------------------------------------------------------
        # Dictionaries
        # --------------------------------------------------------------

        if isinstance(
            value,
            dict,
        ):
            return {
                str(key): self._serialize(item)
                for key, item in value.items()
            }

        # --------------------------------------------------------------
        # Collections
        # --------------------------------------------------------------

        if isinstance(
            value,
            (
                list,
                tuple,
                set,
            ),
        ):
            return [
                self._serialize(item)
                for item in value
            ]

        # --------------------------------------------------------------
        # ARES objects exposing to_dict()
        # --------------------------------------------------------------

        if hasattr(
            value,
            "to_dict",
        ):
            try:

                serialized = value.to_dict()

                return self._serialize(
                    serialized
                )

            except Exception:

                logger.debug(
                    "Object.to_dict() failed during "
                    "context serialization.",
                    exc_info=True,
                )

        # --------------------------------------------------------------
        # Generic Python objects
        # --------------------------------------------------------------

        if hasattr(
            value,
            "__dict__",
        ):
            try:

                return {
                    str(key): self._serialize(item)
                    for key, item in vars(
                        value
                    ).items()
                    if not key.startswith("_")
                }

            except Exception:

                logger.debug(
                    "Object __dict__ serialization failed.",
                    exc_info=True,
                )

        # --------------------------------------------------------------
        # Final safe representation
        # --------------------------------------------------------------

        return str(value)

    # ==================================================================
    # TOOL NAME EXTRACTION
    # ==================================================================

    def _tool_name(
        self,
        tool: Any,
    ) -> str:
        """
        Extract a stable name from a tool definition.
        """

        # --------------------------------------------------------------
        # String tool
        # --------------------------------------------------------------

        if isinstance(
            tool,
            str,
        ):
            return tool

        # --------------------------------------------------------------
        # Dictionary tool
        # --------------------------------------------------------------

        if isinstance(
            tool,
            dict,
        ):
            return str(
                tool.get("name")
                or tool.get("tool_name")
                or tool.get("id")
                or tool
            )

        # --------------------------------------------------------------
        # Object tool
        # --------------------------------------------------------------

        name = getattr(
            tool,
            "name",
            None,
        )

        if name is not None:
            return str(name)

        tool_name = getattr(
            tool,
            "tool_name",
            None,
        )

        if tool_name is not None:
            return str(tool_name)

        tool_id = getattr(
            tool,
            "id",
            None,
        )

        if tool_id is not None:
            return str(tool_id)

        return str(tool)
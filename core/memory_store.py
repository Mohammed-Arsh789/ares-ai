"""
ARES Memory Store
Step 151

Provides the low-level persistent memory foundation for ARES.

Design goals:
- Standard library only
- Human-readable JSON
- Safe loading
- Atomic writes
- Structured memories
- Stable memory IDs
- Future-compatible schema
"""

from __future__ import annotations

import json
import os
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class MemoryStore:
    """
    Persistent JSON-backed memory store.

    The store is deliberately simple at this stage.
    Later steps can add semantic retrieval, embeddings,
    relationships, importance scoring, and SQLite/vector storage.
    """

    SCHEMA_VERSION = 1

    def __init__(self, file_path: str | Path = "memory.json"):
        self.file_path = Path(file_path)
        self._data: dict[str, Any] = {
            "schema_version": self.SCHEMA_VERSION,
            "memories": [],
        }

        self.load()

    # ---------------------------------------------------------
    # Loading
    # ---------------------------------------------------------

    def load(self) -> None:
        """Load the memory database from disk."""

        if not self.file_path.exists():
            self._write_default()
            return

        try:
            raw = self.file_path.read_text(
                encoding="utf-8"
            )

            if not raw.strip():
                self._write_default()
                return

            parsed = json.loads(raw)

            self._data = self._normalize(parsed)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Memory file contains invalid JSON: {exc}"
            ) from exc

        except OSError as exc:
            raise RuntimeError(
                f"Unable to read memory file: {exc}"
            ) from exc

    # ---------------------------------------------------------
    # Normalization
    # ---------------------------------------------------------

    def _normalize(self, data: Any) -> dict[str, Any]:
        """
        Convert older memory formats into the current structure.
        """

        # Old ARES format:
        #
        # [
        #     "ARES memory test"
        # ]
        #
        # Convert each string into a proper memory record.

        if isinstance(data, list):

            memories = []

            for item in data:

                if isinstance(item, str):

                    memories.append(
                        self._create_record(
                            content=item,
                            memory_type="legacy",
                            importance=0.5,
                            source="legacy_memory.json",
                        )
                    )

                elif isinstance(item, dict):

                    memories.append(item)

            return {
                "schema_version": self.SCHEMA_VERSION,
                "memories": memories,
            }

        # Current dictionary format.

        if isinstance(data, dict):

            memories = data.get("memories", [])

            if not isinstance(memories, list):
                memories = []

            return {
                "schema_version": self.SCHEMA_VERSION,
                "memories": memories,
            }

        raise RuntimeError(
            "Unsupported memory database format."
        )

    # ---------------------------------------------------------
    # Default database
    # ---------------------------------------------------------

    def _write_default(self) -> None:

        self._data = {
            "schema_version": self.SCHEMA_VERSION,
            "memories": [],
        }

        self._atomic_write()

    # ---------------------------------------------------------
    # Record creation
    # ---------------------------------------------------------

    def _create_record(
        self,
        content: str,
        memory_type: str = "general",
        importance: float = 0.5,
        source: str = "user",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        now = datetime.now(timezone.utc).isoformat()

        return {
            "id": str(uuid.uuid4()),
            "content": content,
            "type": memory_type,
            "importance": max(0.0, min(1.0, importance)),
            "source": source,
            "created_at": now,
            "updated_at": now,
            "access_count": 0,
            "last_accessed": None,
            "metadata": metadata or {},
        }

    # ---------------------------------------------------------
    # Add memory
    # ---------------------------------------------------------

    def add(
        self,
        content: str,
        memory_type: str = "general",
        importance: float = 0.5,
        source: str = "user",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        content = content.strip()

        if not content:
            raise ValueError(
                "Memory content cannot be empty."
            )

        memory = self._create_record(
            content=content,
            memory_type=memory_type,
            importance=importance,
            source=source,
            metadata=metadata,
        )

        self._data["memories"].append(memory)

        self._atomic_write()

        return memory

    # ---------------------------------------------------------
    # Get all memories
    # ---------------------------------------------------------

    def all(self) -> list[dict[str, Any]]:

        return list(self._data["memories"])

    # ---------------------------------------------------------
    # Find memory by ID
    # ---------------------------------------------------------

    def get(self, memory_id: str) -> dict[str, Any] | None:

        for memory in self._data["memories"]:

            if memory.get("id") == memory_id:
                return memory

        return None

    # ---------------------------------------------------------
    # Delete memory
    # ---------------------------------------------------------

    def delete(self, memory_id: str) -> bool:

        memories = self._data["memories"]

        original_length = len(memories)

        self._data["memories"] = [
            memory
            for memory in memories
            if memory.get("id") != memory_id
        ]

        deleted = len(self._data["memories"]) < original_length

        if deleted:
            self._atomic_write()

        return deleted

    # ---------------------------------------------------------
    # Update memory
    # ---------------------------------------------------------

    def update(
        self,
        memory_id: str,
        **changes: Any,
    ) -> dict[str, Any] | None:

        memory = self.get(memory_id)

        if memory is None:
            return None

        allowed_fields = {
            "content",
            "type",
            "importance",
            "source",
            "metadata",
        }

        for key, value in changes.items():

            if key not in allowed_fields:
                continue

            if key == "content":

                if not isinstance(value, str):
                    raise ValueError(
                        "Memory content must be text."
                    )

                value = value.strip()

                if not value:
                    raise ValueError(
                        "Memory content cannot be empty."
                    )

            if key == "importance":

                value = max(
                    0.0,
                    min(1.0, float(value)),
                )

            memory[key] = value

        memory["updated_at"] = datetime.now(
            timezone.utc
        ).isoformat()

        self._atomic_write()

        return memory

    # ---------------------------------------------------------
    # Record memory access
    # ---------------------------------------------------------

    def touch(self, memory_id: str) -> None:

        memory = self.get(memory_id)

        if memory is None:
            return

        memory["access_count"] = (
            int(memory.get("access_count", 0)) + 1
        )

        memory["last_accessed"] = (
            datetime.now(timezone.utc).isoformat()
        )

        self._atomic_write()

    # ---------------------------------------------------------
    # Atomic write
    # ---------------------------------------------------------

    def _atomic_write(self) -> None:
        """
        Write the memory file safely.

        We write to a temporary file first and replace the
        original only after the temporary file is complete.
        """

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        fd, temp_name = tempfile.mkstemp(
            prefix=".ares_memory_",
            suffix=".tmp",
            dir=str(self.file_path.parent),
        )

        try:

            with os.fdopen(
                fd,
                "w",
                encoding="utf-8",
            ) as temp_file:

                json.dump(
                    self._data,
                    temp_file,
                    indent=2,
                    ensure_ascii=False,
                )

                temp_file.write("\n")

                temp_file.flush()

                os.fsync(temp_file.fileno())

            os.replace(
                temp_name,
                self.file_path,
            )

        except Exception:

            try:
                os.remove(temp_name)
            except OSError:
                pass

            raise

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def stats(self) -> dict[str, int]:

        memories = self._data["memories"]

        types: dict[str, int] = {}

        for memory in memories:

            memory_type = memory.get(
                "type",
                "general",
            )

            types[memory_type] = (
                types.get(memory_type, 0) + 1
            )

        return {
            "total": len(memories),
            "types": types,
        }
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import uuid


@dataclass
class Workspace:

    name: str

    description: str = ""

    workspace_id: str = field(
        default_factory=lambda: str(
            uuid.uuid4()
        )
    )

    created_at: str = field(
        default_factory=lambda:
            datetime.now(
                timezone.utc
            ).isoformat()
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self):

        return {
            "workspace_id":
                self.workspace_id,

            "name":
                self.name,

            "description":
                self.description,

            "created_at":
                self.created_at,

            "metadata":
                self.metadata,
        }
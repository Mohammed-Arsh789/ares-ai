from __future__ import annotations

import json
from pathlib import Path

from .models import Workspace


class WorkspaceStorage:

    def __init__(
        self,
        root: str = "data/workspaces",
    ):

        self.root = Path(root)

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _path(
        self,
        workspace_id: str,
    ) -> Path:

        return (
            self.root
            / f"{workspace_id}.json"
        )

    def save(
        self,
        workspace: Workspace,
    ):

        path = self._path(
            workspace.workspace_id
        )

        path.write_text(
            json.dumps(
                workspace.to_dict(),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def load(
        self,
        workspace_id: str,
    ) -> Workspace:

        path = self._path(
            workspace_id
        )

        if not path.exists():

            raise FileNotFoundError(
                "Workspace not found."
            )

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        return Workspace(
            name=data["name"],
            description=data[
                "description"
            ],
            workspace_id=data[
                "workspace_id"
            ],
            created_at=data[
                "created_at"
            ],
            metadata=data.get(
                "metadata",
                {},
            ),
        )
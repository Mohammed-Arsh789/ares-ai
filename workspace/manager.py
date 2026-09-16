from __future__ import annotations

from .models import Workspace
from .storage import WorkspaceStorage


class WorkspaceManager:

    def __init__(
        self,
        storage=None,
    ):

        self.storage = (
            storage
            or WorkspaceStorage()
        )

        self.active_id: str | None = None

    def create(
        self,
        name: str,
        description: str = "",
    ) -> Workspace:

        if not name.strip():

            raise ValueError(
                "Workspace name cannot be empty."
            )

        workspace = Workspace(
            name=name.strip(),
            description=description.strip(),
        )

        self.storage.save(
            workspace
        )

        self.active_id = (
            workspace.workspace_id
        )

        return workspace

    def open(
        self,
        workspace_id: str,
    ) -> Workspace:

        workspace = (
            self.storage.load(
                workspace_id
            )
        )

        self.active_id = (
            workspace.workspace_id
        )

        return workspace

    def close(self):

        self.active_id = None
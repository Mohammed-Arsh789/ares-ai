"""
ARES Permission Store

Stores the permissions granted to ARES.
"""

from __future__ import annotations

from .permissions import (
    Permission,
    PermissionLevel,
)


class PermissionStore:

    def __init__(self):

        self._permissions: dict[
            str,
            Permission,
        ] = {}

    def grant(
        self,
        resource: str,
        level: PermissionLevel,
    ) -> None:

        self._permissions[resource] = (
            Permission(
                resource,
                level,
            )
        )

    def revoke(
        self,
        resource: str,
    ) -> None:

        self._permissions.pop(
            resource,
            None,
        )

    def get(
        self,
        resource: str,
    ) -> Permission | None:

        return self._permissions.get(
            resource
        )

    def allows(
        self,
        resource: str,
        level: PermissionLevel,
    ) -> bool:

        permission = self.get(
            resource
        )

        if permission is None:

            return False

        return permission.allows(
            level
        )

    def list_permissions(self):

        return [
            permission.to_dict()
            for permission
            in self._permissions.values()
        ]
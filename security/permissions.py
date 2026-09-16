"""
ARES Permission System

Defines the permission levels used by the
security gateway.

The model may REQUEST an action.

The security layer decides whether it is allowed.
"""

from __future__ import annotations

from enum import IntEnum


class PermissionLevel(IntEnum):

    NONE = 0

    READ = 10

    USE = 20

    WRITE = 30

    EXECUTE = 40

    ADMIN = 50


class Permission:

    def __init__(
        self,
        resource: str,
        level: PermissionLevel,
    ):

        self.resource = resource

        self.level = level

    def allows(
        self,
        requested: PermissionLevel,
    ) -> bool:

        return self.level >= requested

    def to_dict(self):

        return {
            "resource": self.resource,
            "level": self.level.name,
            "level_value": int(
                self.level
            ),
        }
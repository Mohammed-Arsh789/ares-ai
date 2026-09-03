from enum import Enum


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class PermissionManager:
    def __init__(self):
        self.tool_permissions = {
            "calculator": Permission.READ,
            "weather": Permission.READ,
        }

    def allowed(
        self,
        tool_name,
        permission,
    ):
        current = self.tool_permissions.get(
            tool_name
        )

        if current is None:
            return False

        return current == permission
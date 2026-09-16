"""
ARES unified exception hierarchy.
"""


class ARESException(Exception):
    """
    Base exception for ARES.
    """


class ConfigurationError(ARESException):
    pass


class ToolError(ARESException):
    pass


class ToolNotFoundError(ToolError):
    pass


class ToolExecutionError(ToolError):
    pass


class AgentError(ARESException):
    pass


class AgentNotFoundError(AgentError):
    pass


class AgentExecutionError(AgentError):
    pass


class PlanningError(ARESException):
    pass


class ExecutionError(ARESException):
    pass


class PermissionDeniedError(ExecutionError):
    pass


class ConfirmationRequiredError(ExecutionError):
    pass


class TaskCancelledError(ExecutionError):
    pass


class TaskTimeoutError(ExecutionError):
    pass


class InvalidRequestError(ARESException):
    pass
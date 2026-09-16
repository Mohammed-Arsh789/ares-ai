"""
Backward-compatible tool result exports.

The canonical result implementation lives in core.results.
"""

from core.results import (
    ToolResult,
    ResultStatus,
    create_trace_id,
    utc_timestamp,
)

__all__ = [
    "ToolResult",
    "ResultStatus",
    "create_trace_id",
    "utc_timestamp",
]
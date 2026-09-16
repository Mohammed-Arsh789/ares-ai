"""
Compatibility bridge for the canonical tools.registry.ToolRegistry.

New code should import ToolRegistry from tools.registry.
"""

from tools.registry import ToolRegistry

__all__ = ["ToolRegistry"]
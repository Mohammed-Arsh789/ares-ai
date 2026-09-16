from .base import Filter
from .builtin import (
    NoirFilter,
    SketchFilter,
    VintageFilter,
)
from .pipeline import FilterPipeline
from .registry import FilterRegistry


def create_default_registry():

    registry = FilterRegistry()

    registry.register(
        NoirFilter()
    )

    registry.register(
        VintageFilter()
    )

    registry.register(
        SketchFilter()
    )

    return registry


__all__ = [
    "Filter",
    "NoirFilter",
    "VintageFilter",
    "SketchFilter",
    "FilterPipeline",
    "FilterRegistry",
    "create_default_registry",
]
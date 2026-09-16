from __future__ import annotations

from .base import Filter


class FilterRegistry:

    def __init__(self):

        self._filters: dict[
            str,
            Filter,
        ] = {}

    def register(
        self,
        filter_instance: Filter,
    ):

        name = (
            filter_instance.name
            .strip()
            .lower()
        )

        if not name:
            raise ValueError(
                "Filter name cannot be empty."
            )

        self._filters[
            name
        ] = filter_instance

    def get(
        self,
        name: str,
    ) -> Filter:

        try:

            return self._filters[
                name.lower()
            ]

        except KeyError as exc:

            raise KeyError(
                f"Unknown filter: {name}"
            ) from exc

    def list(self):

        return sorted(
            self._filters.keys()
        )
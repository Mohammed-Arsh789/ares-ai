from __future__ import annotations


class FilterPipeline:

    def __init__(
        self,
        registry,
    ):

        self.registry = registry

    def apply(
        self,
        frame,
        filter_name: str,
    ):

        filter_instance = (
            self.registry.get(
                filter_name
            )
        )

        return filter_instance.apply(
            frame
        )
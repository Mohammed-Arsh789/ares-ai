from collections.abc import Callable


class ActionRegistry:
    def __init__(self):
        self.actions: dict[str, Callable] = {}

    def register(self, name: str, function: Callable):
        self.actions[name] = function

    def execute(self, name: str, **kwargs):
        if name not in self.actions:
            raise ValueError(f"Unknown automation action: {name}")

        return self.actions[name](**kwargs)

    def has(self, name: str) -> bool:
        return name in self.actions
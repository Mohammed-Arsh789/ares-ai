class PluginRegistry:
    def __init__(self):
        self.plugins = {}

    def register(self, plugin):
        name = plugin.metadata.name

        if name in self.plugins:
            raise ValueError(
                f"Plugin already registered: {name}"
            )

        self.plugins[name] = plugin

    def get(self, name: str):
        return self.plugins.get(name)

    def remove(self, name: str) -> bool:
        return self.plugins.pop(name, None) is not None

    def names(self) -> list[str]:
        return list(self.plugins.keys())
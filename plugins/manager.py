class PluginManager:
    def __init__(self, registry):
        self.registry = registry

    def load(self, name: str):
        plugin = self.registry.get(name)

        if plugin is None:
            raise KeyError(f"Unknown plugin: {name}")

        try:
            plugin.on_load()
            plugin.state.loaded = True
            plugin.state.error = None
            return True

        except Exception as error:
            plugin.state.loaded = False
            plugin.state.error = str(error)
            return False

    def unload(self, name: str):
        plugin = self.registry.get(name)

        if plugin is None:
            raise KeyError(f"Unknown plugin: {name}")

        plugin.on_unload()
        plugin.state.loaded = False
from plugins import (
    ARESPlugin,
    PluginManager,
    PluginMetadata,
    PluginRegistry,
)


class ExamplePlugin(ARESPlugin):
    metadata = PluginMetadata(
        name="example",
        version="1.0.0",
        description="Test plugin",
    )

    def on_load(self):
        self.enable()

    def on_unload(self):
        self.disable()


def test_plugin_lifecycle():
    registry = PluginRegistry()
    plugin = ExamplePlugin()

    registry.register(plugin)

    manager = PluginManager(registry)

    assert manager.load("example") is True
    assert plugin.state.loaded is True
    assert plugin.state.enabled is True

    manager.unload("example")

    assert plugin.state.loaded is False
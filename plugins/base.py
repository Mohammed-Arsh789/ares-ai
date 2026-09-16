from abc import ABC, abstractmethod

from .models import PluginMetadata, PluginState


class ARESPlugin(ABC):
    metadata: PluginMetadata

    def __init__(self):
        self.state = PluginState()

    @abstractmethod
    def on_load(self):
        raise NotImplementedError

    @abstractmethod
    def on_unload(self):
        raise NotImplementedError

    def enable(self):
        self.state.enabled = True

    def disable(self):
        self.state.enabled = False
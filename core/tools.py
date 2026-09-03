from tools.registry import ToolRegistry
from tools.calculator import CalculatorTool
from tools.weather import WeatherTool


class ToolManager:
    def __init__(self):
        self.registry = ToolRegistry()

        self.register_default_tools()

    def register_default_tools(self):
        self.registry.register(
            CalculatorTool()
        )

        self.registry.register(
            WeatherTool()
        )

    def get(self, name):
        return self.registry.get(name)

    def has(self, name):
        return self.registry.has(name)

    def available_tools(self):
        return self.registry.list_tools()

    def descriptions(self):
        return self.registry.descriptions()
class ToolRegistry:

    def __init__(self):

        self.tools = {}

    def register(self, name, description, function):

        self.tools[name] = {
            "description": description,
            "function": function
        }

    def list_tools(self):

        return {
            name: info["description"]
            for name, info in self.tools.items()
        }

    def exists(self, name):

        return name in self.tools

    def execute(self, name, **kwargs):

        if name not in self.tools:
            raise ValueError(f"Tool '{name}' is not allowed.")

        function = self.tools[name]["function"]

        return function(**kwargs)
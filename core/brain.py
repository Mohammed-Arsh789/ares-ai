from core.ai import AIClient
from core.memory import Memory
from core.router import Router
from core.tool_registry import ToolRegistry
from tools.calculator import calculate


class ARES:

    def __init__(self):

        self.ai = AIClient()
        self.memory = Memory()
        self.router = Router()
        self.tools = ToolRegistry()

        self.tools.register(
            "calculator",
            "Safely perform mathematical calculations.",
            calculate
        )

    def respond(self, message):

        route = self.router.route(message)

        if route == "calculator":

            expression = message

            expression = expression.replace(
                "calculate", ""
            ).replace(
                "calc", ""
            ).strip()

            try:

                result = self.tools.execute(
                    "calculator",
                    expression=expression
                )

                return f"The answer is {result}."

            except Exception as error:

                return f"I couldn't calculate that safely: {error}"

        if route == "memory":

            content = message[len("remember "):].strip()

            if not content:
                return "Tell me what you'd like me to remember."

            self.memory.remember(
                "user_memory",
                content
            )

            return "Got it. I've stored that in ARES memory."

        if route == "help":

            return self._help()

        return self.ai.ask(message)

    def _help(self):

        tools = self.tools.list_tools()

        return (
            "I can currently have conversations, maintain context, "
            "remember information, detect conversational tone, "
            "and safely perform calculations.\n\n"
            f"Available tools: {', '.join(tools.keys())}"
        )

    def close(self):

        self.memory.close()
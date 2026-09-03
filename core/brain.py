from core.ai import AIClient
from core.memory import Memory
from core.router import Router
from core.tools import ToolManager


class ARES:
    def __init__(self):
        self.name = "ARES"

        self.ai = AIClient()
        self.memory = Memory()
        self.router = Router()
        self.tools = ToolManager()

    def respond(self, message):
        message = message.strip()

        if not message:
            return "I'm listening."

        lower = message.lower()

        # Memory commands
        if lower.startswith("remember that "):
            content = message[len("remember that "):].strip()

            if self.memory.remember(
                content,
                category="user_preference",
                importance=2,
            ):
                return "Got it. I'll remember that."

            return "I already have that in memory."

        if lower.startswith("forget that "):
            content = message[len("forget that "):].strip()

            if self.memory.forget(content):
                return "Removed from memory."

            return "I couldn't find that exact memory."

        if lower in {
            "show my memories",
            "show memories",
            "what do you remember",
        }:
            memories = self.memory.all()

            if not memories:
                return "My long-term memory is currently empty."

            return "\n".join(
                f"- {memory['content']}"
                for memory in memories
            )

        intent = self.router.route(message)

        if intent == "exit":
            return None

        if intent == "calculator":
            return self._calculator(message)

        if intent == "weather":
            return self._weather(message)

        if intent == "web":
            return self.ai.ask(
                "The user wants current web information. "
                "Explain that web search integration is being built, "
                "and do not invent current facts.\n\n"
                f"User request: {message}"
            )

        context = self._memory_context(message)

        if context:
            prompt = (
                "Relevant long-term memories:\n"
                f"{context}\n\n"
                f"User message:\n{message}"
            )
        else:
            prompt = message

        return self.ai.ask(prompt)

    def _calculator(self, message):
        expression = message.lower()

        for prefix in [
            "calculate",
            "calculator",
            "compute",
            "solve",
        ]:
            if expression.startswith(prefix):
                expression = expression[len(prefix):].strip()
                break

        try:
            result = self.tools.get("calculator").run(
                expression=expression
            )

            return f"The result is {result}."

        except Exception as error:
            return f"I couldn't calculate that: {error}"

    def _weather(self, message):
        return self.ai.ask(
            "The user asked about weather.\n"
            "The weather tool requires a location.\n"
            "Do not invent weather data.\n"
            "Ask for a city if one is not provided.\n\n"
            f"User request: {message}"
        )

    def _memory_context(self, message):
        results = self.memory.search(
            message,
            limit=3,
        )

        if not results:
            return ""

        return "\n".join(
            f"- {memory['content']}"
            for memory in results
        )

    def run(self):
        print("=" * 50)
        print("                    ARES")
        print("             Local AI Assistant")
        print("=" * 50)
        print("Type 'exit' to shut down.\n")

        while True:
            try:
                user_input = input("You > ")

                response = self.respond(
                    user_input
                )

                if response is None:
                    print("ARES > Goodbye.")
                    break

                print(f"ARES > {response}")

            except KeyboardInterrupt:
                print("\nARES > Shutdown requested.")
                break

            except Exception as error:
                print(
                    f"ARES > An internal error occurred: {error}"
                )
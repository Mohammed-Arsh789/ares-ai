from core.ai import AIClient
from core.router import Router
from core.tools import ToolManager


class ARES:
    def __init__(self):
        self.name = "ARES"

        self.router = Router()
        self.ai = AIClient()
        self.tools = ToolManager()

    def respond(self, message):
        message = message.strip()

        if not message:
            return "I'm listening."

        intent = self.router.route(message)

        if intent == "exit":
            return None

        if intent == "calculator":
            return self.handle_calculator(message)

        if intent == "weather":
            return self.handle_weather(message)

        return self.ai.ask(message)

    def handle_calculator(self, message):
        expression = self.extract_expression(message)

        try:
            result = self.tools.get("calculator").run(
                expression=expression
            )

            return f"The result is {result}."

        except ValueError as error:
            return f"I couldn't calculate that: {error}"

    def handle_weather(self, message):
        return self.ai.ask(
            f"The user asked about weather: {message}. "
            "Explain that the weather tool is available, "
            "but location coordinates are required before retrieving "
            "weather data."
        )

    def extract_expression(self, message):
        prefixes = [
            "calculate",
            "calculator",
            "solve",
            "math",
        ]

        expression = message.lower().strip()

        for prefix in prefixes:
            if expression.startswith(prefix):
                expression = expression[len(prefix):].strip()

        return expression

    def run(self):
        print("=" * 40)
        print("              ARES")
        print("        Personal AI Assistant")
        print("=" * 40)
        print("Type 'exit' to shut down ARES.\n")

        while True:
            user_input = input("You > ")

            response = self.respond(user_input)

            if response is None:
                print("ARES > Goodbye.")
                break

            print(f"ARES > {response}")
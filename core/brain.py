from core.ai import AIClient
from core.router import Router


class ARES:
    def __init__(self):
        self.name = "ARES"
        self.router = Router()
        self.ai = AIClient()

    def respond(self, message):
        message = message.strip()

        if not message:
            return "I'm listening."

        intent = self.router.route(message)

        if intent == "exit":
            return None

        return self.ai.ask(message)

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
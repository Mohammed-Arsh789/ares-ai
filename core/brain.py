class ARES:
    def __init__(self):
        self.name = "ARES"

    def respond(self, message):
        message = message.lower().strip()

        if message in ["hello", "hi", "hey"]:
            return "Hello. I'm ARES. How can I help?"

        if "who are you" in message:
            return "I'm ARES, your personal AI assistant."

        if "how are you" in message:
            return "I'm online and ready."

        if message in ["bye", "exit", "quit"]:
            return None

        return "I understand the request, but my intelligence systems are still being developed."

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
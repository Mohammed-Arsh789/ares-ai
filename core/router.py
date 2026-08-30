class Router:
    def route(self, message):
        message = message.lower().strip()

        if not message:
            return "empty"

        if message in ["hello", "hi", "hey"]:
            return "conversation"

        if message in ["bye", "exit", "quit"]:
            return "exit"

        if "weather" in message:
            return "weather"

        return "conversation"
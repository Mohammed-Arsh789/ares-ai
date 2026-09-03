class Router:

    def route(self, text):

        lowered = text.lower().strip()

        if lowered.startswith("calculate "):
            return "calculator"

        if lowered.startswith("calc "):
            return "calculator"

        if "weather" in lowered:
            return "weather"

        if lowered.startswith("remember "):
            return "memory"

        if lowered in {
            "help",
            "what can you do",
            "what are your capabilities"
        }:
            return "help"

        return "chat"
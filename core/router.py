class Router:

    def route(self, text):

        lowered = text.lower().strip()

        if lowered.startswith(("calculate ", "calc ")):
            return "calculator"

        if any(word in lowered for word in [
            "weather",
            "temperature outside",
            "forecast",
            "is it raining"
        ]):
            return "weather"

        if lowered.startswith("remember "):
            return "memory"

        if lowered.startswith((
            "what do you remember",
            "what do you know about me",
            "show my memories"
        )):
            return "memory_search"

        if lowered.startswith("open notepad"):
            return "open_notepad"

        if lowered.startswith("open calculator"):
            return "open_calculator"

        if lowered in {
            "help",
            "what can you do",
            "what are your capabilities",
            "capabilities"
        }:
            return "help"

        return "chat"
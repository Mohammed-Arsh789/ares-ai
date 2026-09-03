class Router:

    def route(self, text):

        lowered = text.lower().strip()

        calculation_words = [
            "calculate",
            "calc"
        ]

        if any(
            lowered.startswith(word)
            for word in calculation_words
        ):
            return "calculator"

        weather_words = [
            "weather",
            "temperature outside",
            "forecast",
            "is it raining"
        ]

        if any(word in lowered for word in weather_words):
            return "weather"

        if lowered.startswith("remember "):
            return "memory"

        if lowered in {
            "help",
            "what can you do",
            "what are your capabilities",
            "capabilities"
        }:
            return "help"

        return "chat"
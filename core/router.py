class Router:
    def route(self, message):
        text = message.lower().strip()

        # Exit
        if text in ["exit", "quit", "bye"]:
            return "exit"

        # Calculator
        calculator_words = [
            "calculate",
            "calculator",
            "solve",
            "math",
            "what is",
        ]

        if any(word in text for word in calculator_words):
            # Only classify as calculator if it looks like a math request
            math_symbols = ["+", "-", "*", "/", "%"]

            if any(symbol in text for symbol in math_symbols):
                return "calculator"

            if "calculate" in text or "calculator" in text or "solve" in text:
                return "calculator"

        # Weather
        weather_words = [
            "weather",
            "temperature",
            "forecast",
            "rain",
            "raining",
        ]

        if any(word in text for word in weather_words):
            return "weather"

        # Web / current information
        web_words = [
            "search the web",
            "search online",
            "look up",
            "latest",
            "news",
            "today",
            "current",
            "who won",
        ]

        if any(word in text for word in web_words):
            return "web"

        # File operations
        file_words = [
            "open file",
            "read file",
            "create file",
            "delete file",
            "rename file",
            "file",
        ]

        if any(word in text for word in file_words):
            return "files"

        # System operations
        system_words = [
            "system information",
            "python version",
            "system status",
            "ares status",
        ]

        if any(word in text for word in system_words):
            return "system"

        # Normal conversation
        return "conversation"
class Router:
    def route(self, message):
        text = message.lower().strip()

        if not text:
            return "conversation"

        if text in {
            "exit",
            "quit",
            "shutdown",
            "goodbye",
        }:
            return "exit"

        if self._looks_like_calculation(text):
            return "calculator"

        if self._looks_like_weather(text):
            return "weather"

        if self._looks_like_web_search(text):
            return "web"

        if self._looks_like_file_operation(text):
            return "files"

        if self._looks_like_system_request(text):
            return "system"

        return "conversation"

    def _looks_like_calculation(self, text):
        keywords = [
            "calculate",
            "calculator",
            "solve",
            "compute",
        ]

        if any(word in text for word in keywords):
            return True

        math_symbols = ["+", "-", "*", "/", "%"]

        if any(symbol in text for symbol in math_symbols):
            return any(char.isdigit() for char in text)

        return False

    def _looks_like_weather(self, text):
        keywords = [
            "weather",
            "temperature outside",
            "forecast",
            "is it raining",
            "will it rain",
        ]

        return any(keyword in text for keyword in keywords)

    def _looks_like_web_search(self, text):
        keywords = [
            "search the web",
            "search online",
            "look this up",
            "look it up",
            "latest news",
            "current news",
            "what happened today",
        ]

        return any(keyword in text for keyword in keywords)

    def _looks_like_file_operation(self, text):
        keywords = [
            "open file",
            "read file",
            "create file",
            "delete file",
            "rename file",
            "list files",
        ]

        return any(keyword in text for keyword in keywords)

    def _looks_like_system_request(self, text):
        keywords = [
            "system information",
            "system status",
            "python version",
            "ares status",
        ]

        return any(keyword in text for keyword in keywords)
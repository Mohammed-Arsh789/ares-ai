from core.ai import AIClient
from core.memory import Memory
from core.router import Router
from core.tool_registry import ToolRegistry
from core.logger import get_logger

from tools.calculator import calculate
from tools.weather import get_weather
from tools.weather_codes import describe_weather
from tools.apps import launch_app


class ARES:

    def __init__(self):

        self.logger = get_logger()

        self.ai = AIClient()
        self.memory = Memory()
        self.router = Router()
        self.tools = ToolRegistry()

        self.tools.register(
            "calculator",
            "Safely perform mathematical calculations.",
            calculate
        )

        self.tools.register(
            "weather",
            "Retrieve current weather information.",
            get_weather
        )

        self.tools.register(
            "launch_app",
            "Launch an explicitly allowlisted application.",
            launch_app
        )

        self.logger.info("ARES initialized")

    def respond(self, message):

        self.logger.info(
            "User request: %s",
            message
        )

        route = self.router.route(message)

        self.logger.info(
            "Selected route: %s",
            route
        )

        # -------------------------
        # CALCULATOR
        # -------------------------

        if route == "calculator":

            expression = (
                message
                .replace("calculate", "")
                .replace("calc", "")
                .strip()
            )

            try:

                result = self.tools.execute(
                    "calculator",
                    expression=expression
                )

                return f"The answer is {result}."

            except Exception as error:

                return (
                    f"I couldn't calculate that safely: {error}"
                )

        # -------------------------
        # MEMORY
        # -------------------------

        if route == "memory":

            content = message[len("remember "):].strip()

            if not content:
                return (
                    "Tell me what you'd like me to remember."
                )

            self.memory.remember(
                "user_memory",
                content
            )

            return (
                "Got it. I've stored that in ARES memory."
            )

        # -------------------------
        # MEMORY SEARCH
        # -------------------------

        if route == "memory_search":

            memories = self.memory.search(
                limit=10
            )

            if not memories:
                return (
                    "I don't have any stored memories yet."
                )

            lines = [
                f"- {content}"
                for category, content, created_at
                in memories
            ]

            return (
                "Here's what I remember:\n"
                + "\n".join(lines)
            )

        # -------------------------
        # WEATHER
        # -------------------------

        if route == "weather":

            try:

                weather = self.tools.execute(
                    "weather",
                    latitude=12.9716,
                    longitude=77.5946
                )

                description = describe_weather(
                    weather["weather_code"]
                )

                return (
                    f"Current conditions: {description}. "
                    f"Temperature: "
                    f"{weather['temperature']}°C. "
                    f"Feels like: "
                    f"{weather['feels_like']}°C. "
                    f"Humidity: "
                    f"{weather['humidity']}%. "
                    f"Wind: "
                    f"{weather['wind_speed']} km/h."
                )

            except Exception as error:

                return (
                    f"I couldn't retrieve weather data: {error}"
                )

        # -------------------------
        # OPEN APPLICATION
        # -------------------------

        if route == "open_app":

            app_name = message[5:].strip()

            try:

                return self.tools.execute(
                    "launch_app",
                    name=app_name
                )

            except Exception as error:

                return (
                    f"I couldn't launch "
                    f"{app_name}: {error}"
                )

        # -------------------------
        # HELP
        # -------------------------

        if route == "help":

            return (
                "ARES capabilities:\n"
                "- Natural language conversation\n"
                "- Context\n"
                "- Persistent memory\n"
                "- Emotional-tone awareness\n"
                "- Calculator\n"
                "- Live weather\n"
                "- Allowlisted application launching"
            )

        # -------------------------
        # CHAT
        # -------------------------

        return self.ai.ask(message)

    def close(self):

        self.memory.close()
import requests

from .base import Tool
from .result import ToolResult


def get_weather(latitude, longitude):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,"
        "apparent_temperature,weather_code,wind_speed_10m"
    )

    response = requests.get(
        url,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "feels_like": current["apparent_temperature"],
        "wind_speed": current["wind_speed_10m"],
        "weather_code": current["weather_code"],
    }


class WeatherTool(Tool):

    name = "weather"

    description = (
        "Gets current weather information "
        "from Open-Meteo."
    )

    dangerous = False

    requires_confirmation = False

    def run(
        self,
        latitude: float,
        longitude: float,
    ):

        try:

            weather = get_weather(
                latitude,
                longitude,
            )

            return ToolResult.ok(
                self.name,
                weather,
            )

        except Exception as error:

            return ToolResult.fail(
                self.name,
                str(error),
            )
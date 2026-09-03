import requests

from tools.base import Tool
from tools.result import ToolResult


class WeatherTool(Tool):
    name = "weather"
    description = "Gets current weather from Open-Meteo."

    API_URL = (
        "https://api.open-meteo.com/v1/forecast"
    )

    def run(
        self,
        latitude,
        longitude,
    ):
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "timezone": "auto",
            }

            response = requests.get(
                self.API_URL,
                params=params,
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            current = data.get("current")

            if not current:
                raise ValueError(
                    "No current weather data."
                )

            result = {
                "temperature": current.get(
                    "temperature_2m"
                ),
                "humidity": current.get(
                    "relative_humidity_2m"
                ),
                "weather_code": current.get(
                    "weather_code"
                ),
                "wind_speed": current.get(
                    "wind_speed_10m"
                ),
                "timezone": data.get(
                    "timezone"
                ),
            }

            return ToolResult.ok(
                self.name,
                result,
            )

        except Exception as error:
            return ToolResult.fail(
                self.name,
                error,
            )
import requests


class WeatherTool:
    name = "weather"

    def run(self, latitude, longitude):
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto",
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        current = data["current"]

        return {
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "weather_code": current["weather_code"],
            "wind_speed": current["wind_speed_10m"],
            "timezone": data.get("timezone"),
        }
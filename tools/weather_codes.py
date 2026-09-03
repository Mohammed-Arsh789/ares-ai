WEATHER_CODES = {

    0: "Clear sky",

    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",

    45: "Fog",
    48: "Depositing rime fog",

    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",

    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",

    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",

    80: "Light rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",

    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail"
}


def describe_weather(code):

    return WEATHER_CODES.get(
        code,
        "Unknown weather conditions"
    )
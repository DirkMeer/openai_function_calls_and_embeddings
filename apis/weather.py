from decouple import config
from json import dumps
import requests


def get_current_weather(location) -> str:
    if not location:
        return (
            "Please provide a location and call the get_current_weather_function again."
        )
    API_params = {
        "key": config("WEATHER_API_KEY"),
        "q": location,
        "aqi": "no",
        "alerts": "no",
    }
    response: requests.models.Response = requests.get(
        "http://api.weatherapi.com/v1/current.json", params=API_params
    )
    str_response: str = dumps(response.json())
    return str_response


def get_weather_forecast(location, days=7) -> str:
    try:
        days = 1 if days < 1 else 14 if days > 14 else days
    except TypeError:
        days = 7

    params = {
        "key": config("WEATHER_API_KEY"),
        "q": location,
        "days": days,
        "aqi": "no",
        "alerts": "no",
    }

    response: requests.models.Response = requests.get(
        "http://api.weatherapi.com/v1/forecast.json", params=params
    )

    response: dict = response.json()
    filtered_response = {}
    filtered_response["location"] = response["location"]
    filtered_response["current"] = response["current"]
    filtered_response["forecast"] = [
        [day["date"], day["day"]] for day in response["forecast"]["forecastday"]
    ]
    return dumps(filtered_response)


# print(get_weather_forecast("Seoul", days=3))

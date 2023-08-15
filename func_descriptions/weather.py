describe_get_current_weather = {
    "name": "get_current_weather_in_location",
    "description": "This function provides the current weather in a specific location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location as a city name, e.g. Amsterdam.",
            },
        },
        "required": ["location"],
    },
}

describe_get_weather_forecast = {
    "name": "get_weather_forecast_in_location",
    "description": "This function provides the weather forecast in a specific location for a specified number of days.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location as a city name, e.g. Amsterdam.",
            },
            "days": {
                "type": "integer",
                "description": "The number of days to forecast, between 1 and 14.",
            },
        },
        "required": ["location"],
    },
}

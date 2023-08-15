import json

from utils.printer import ColorPrinter as Printer
from apis.weather import get_weather_forecast, get_current_weather
from apis.chat_gpt import gpt_3_5_turbo_0613
from prompt_setups.weather import current_and_forecast_setup
from func_descriptions.weather import (
    describe_get_current_weather,
    describe_get_weather_forecast,
)


def ask_chat_gpt(query):
    messages = [
        {"role": "system", "content": current_and_forecast_setup},
        {"role": "user", "content": query},
    ]

    functions = [
        describe_get_current_weather,
        describe_get_weather_forecast,
    ]

    current_response = gpt_3_5_turbo_0613(messages, functions)
    current_message = current_response["choices"][0]["message"]
    messages.append(current_message)

    is_calling_function = True if current_message.get("function_call") else False

    while is_calling_function:
        available_functions = {
            "get_current_weather_in_location": get_current_weather,
            "get_weather_forecast_in_location": get_weather_forecast,
        }
        function_name = current_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(current_message["function_call"]["arguments"])
        function_response = function_to_call(**function_args)

        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )

        current_response = gpt_3_5_turbo_0613(messages, functions)
        current_message = current_response["choices"][0]["message"]
        messages.append(current_message)

        is_calling_function = True if current_message.get("function_call") else False

    Printer.color_print(messages)
    return current_message["content"]


print(
    ask_chat_gpt(
        "Please give me the current weather in Seoul and the weather forecast in Amsterdam for the coming three days in a single response."
    )
)

import json
import openai

from decouple import config

from apis.weather import get_current_weather
from func_descriptions.weather import describe_get_current_weather
from utils.printer import ColorPrinter as Printer

openai.api_key = config("CHATGPT_API_KEY")


def ask_chat_gpt(query):
    messages = [
        {"role": "user", "content": query},
    ]

    functions = [describe_get_current_weather]

    first_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default
    )["choices"][0]["message"]
    messages.append(first_response)

    if first_response.get("function_call"):
        available_functions = {
            "get_current_weather_in_location": get_current_weather,
        }
        function_name = first_response["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(first_response["function_call"]["arguments"])
        function_response = function_to_call(
            location=function_args.get("location"),
        )

        messages.append(
            {
                "role": "function",
                "name": "get_current_weather_in_location",
                "content": function_response,
            }
        )

        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )["choices"][0]["message"]
        messages.append(second_response)
        Printer.color_print(messages)
        return second_response["content"]

    Printer.color_print(messages)
    return first_response["content"]


print(ask_chat_gpt("What is the weather in Amsterdam?"))

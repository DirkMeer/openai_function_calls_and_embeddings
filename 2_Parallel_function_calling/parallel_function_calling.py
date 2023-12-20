import json
from decouple import config
from openai import OpenAI
from typing import Callable

from weather import get_current_weather, get_weather_forecast
from prompt_setup import current_and_forecast_setup
from function_descriptions import (
    describe_get_current_weather,
    describe_get_weather_forecast,
)


MODEL = "gpt-3.5-turbo-1106"
client = OpenAI(api_key=config("OPENAI_API_KEY"))


def quick_dirty_printer(messages):
    """
    Prints messages in alternating colors (irrespective of role) and the final message in green. (92 is green, 93 is yellow, 94 is blue)
    """
    for index, message in enumerate(messages):
        if index == len(messages) - 1:
            print(f"\033[92m {message} \033[0m")
        elif index % 2 == 0:
            print(f"\033[93m {message} \033[0m")
        else:
            print(f"\033[94m {message} \033[0m")


def ask_weather_gpt(query, message_history=None, simulate_failure=False):
    need_to_fail_once = simulate_failure
    messages = []

    def handle_and_append_response(response):
        """
        Appends message to history and extracts the message,
        prevents a current bug by explicitly setting .content and .function_call
        """
        response_message = response.choices[0].message
        if response_message.content is None:
            response_message.content = ""
        if response_message.function_call is None:
            del response_message.function_call
        messages.append(response_message)
        return response_message

    if message_history:
        messages = message_history
    else:
        messages = [
            {"role": "system", "content": current_and_forecast_setup},
            {"role": "user", "content": query},
        ]

    tools = [
        describe_get_current_weather,
        describe_get_weather_forecast,
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = handle_and_append_response(response)

    while response_message.tool_calls:
        tool_calls = response_message.tool_calls
        available_functions = {
            "get_current_weather": get_current_weather,
            "get_weather_forecast": get_weather_forecast,
        }

        try:
            if need_to_fail_once:
                need_to_fail_once = False
                raise Exception("Simulating failure")
            for call in tool_calls:
                func_name: str = call.function.name
                func_to_call: Callable = available_functions[func_name]
                func_args: dict = json.loads(call.function.arguments)
                func_response = func_to_call(**func_args)

                messages.append(
                    {
                        "tool_call_id": call.id,
                        "role": "tool",
                        "name": func_name,
                        "content": func_response,
                    }
                )

        except:
            messages.pop()
            messages.append(
                {
                    "role": "system",
                    "content": "Based on the above information, please generate the appropriate tool calls with valid arguments per the schema provided.",
                }
            )
            return ask_weather_gpt(query, message_history=messages)

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )

        response_message = handle_and_append_response(response)

        quick_dirty_printer(messages)
        return response_message

    quick_dirty_printer(messages)
    return response_message


# ask_weather_gpt("What's the weather in San Francisco?", simulate_failure=True)

ask_weather_gpt(
    "Please give me the current weather in Seoul and the weather forecast in Amsterdam for the coming three days."
)

# ask_weather_gpt("What is a zombie watermelon?")

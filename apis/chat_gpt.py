import openai
from decouple import config

openai.api_key = config("CHATGPT_API_KEY")


def gpt_3_5_turbo_0613(messages, functions=None, function_call="auto"):
    params = {
        "model": "gpt-3.5-turbo-0613",
        "messages": messages,
    }
    if functions:
        params["functions"] = functions
        params["function_call"] = function_call

    return openai.ChatCompletion.create(**params)

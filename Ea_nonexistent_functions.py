import json

from utils.printer import ColorPrinter as Printer
from utils.reader import read_txt_file
from apis.chat_gpt import gpt_3_5_turbo_0613
from prompt_setups.extract import data_extraction_setup
from func_descriptions.extract import describe_extract_dates


def extract_structured_info(text_data):
    messages = [
        {"role": "system", "content": data_extraction_setup},
        {"role": "user", "content": text_data},
    ]
    functions = [describe_extract_dates]

    current_response = gpt_3_5_turbo_0613(
        messages, functions, function_call={"name": "make_list_of_dates"}
    )
    current_message = current_response["choices"][0]["message"]
    messages.append(current_message)

    if current_message.get("function_call"):
        print(current_message["function_call"]["arguments"])
        structured_data: dict = json.loads(
            current_message["function_call"]["arguments"]
        )
        list_of_happenings: list = structured_data["list_of_happenings"]

        Printer.color_print(messages)
        for list_item in list_of_happenings:
            print(f"{list_item[0]} - {list_item[1]}")


text_data = read_txt_file("Ex_text_data.txt")

extract_structured_info(text_data)

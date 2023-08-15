import json
import sqlite3

from utils.printer import ColorPrinter as Printer
from utils.database import Database
from apis.chat_gpt import gpt_3_5_turbo_0613
from prompt_setups.database import database_query_bot_setup
from func_descriptions.database import describe_get_info_from_database

conn = sqlite3.connect("./database.sqlite")
print("Database connection successful.")

company_db = Database(conn)
database_schema: str = str(company_db.get_database_info())
print(database_schema)


def get_info_from_database(query) -> str:
    try:
        res = company_db.execute(query)
        return json.dumps(res)
    except Exception as e:
        raise Exception(
            f"Error executing query: {e}, please try again, passing in a valid SQL query in string format as only argument."
        )


def ask_company_db(query):
    messages = [
        {"role": "system", "content": database_query_bot_setup},
        {"role": "user", "content": query},
    ]
    functions = [describe_get_info_from_database(database_schema)]

    current_response = gpt_3_5_turbo_0613(
        messages, functions, function_call={"name": "get_info_from_database"}
    )
    current_message = current_response["choices"][0]["message"]
    messages.append(current_message)

    if current_message.get("function_call"):
        available_functions = {
            "get_info_from_database": get_info_from_database,
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

    Printer.color_print(messages)
    return current_message["content"]


print(ask_company_db("What are the names of the 10 users who wrote the most reviews?"))

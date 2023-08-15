from tenacity import retry, stop_after_attempt, stop_after_delay
from apis.chat_gpt import gpt_3_5_turbo_0613

fail_counter = 0


# Define a function that will retry on failure
@retry(stop=stop_after_attempt(3))
def ask_gpt(query):
    ## Simulate failure ##
    global fail_counter
    fail_counter += 1
    if fail_counter < 2:
        raise ValueError("GPT failed")

    response = gpt_3_5_turbo_0613(query)
    return response


messages = [
    {
        "role": "user",
        "content": "What is the capital of France?",
    }
]

# print(ask_gpt(messages))


@retry(stop=stop_after_delay(3))
def try_something_stupid():
    ## Simulate failure ##
    print("Trying to do something stupid and dangerous")
    raise Exception("Something stupid and dangerous happened")


@retry(stop=(stop_after_attempt(10) | stop_after_delay(5)))
def eat_watermelon_in_one_bite():
    ## Simulate failure ##
    print("Trying to do eat a watermelon in one bite")
    raise Exception("You cannot eat a watermelon in one bite!")


eat_watermelon_in_one_bite()

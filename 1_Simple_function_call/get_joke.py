from decouple import config
from openai import OpenAI

client = OpenAI(api_key=config("OPENAI_API_KEY"))
JOKE_SETUP = "I will give you a subject each time for all the following prompts. You will return to me a joke, but it should not be too long (4 lines at most). Please do not provide an introduction like 'Here's a joke for you' but get straight into the joke."


def get_joke(query: str) -> str:
    result = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.4,
        max_tokens=200,
        messages=[
            {"role": "system", "content": JOKE_SETUP},
            {"role": "user", "content": query},
        ],
    )

    return result.choices[0].message.content


print(get_joke("Penguins"))

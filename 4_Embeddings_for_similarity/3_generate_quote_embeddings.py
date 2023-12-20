import json
from pathlib import Path

import pandas as pd
from decouple import config
from openai import OpenAI


client = OpenAI(api_key=config("OPENAI_API_KEY"))
current_directory = Path(__file__).parent
EMBEDDING_MODEL = "text-embedding-ada-002"

total_tokens_used = 0
total_embeddings = 0


with open(current_directory / "quotes.json", "r", encoding="utf-8") as file:
    quotes = json.load(file)


def get_quote_embedding(quote: str) -> list[float]:
    global total_tokens_used, total_embeddings
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=quote,
    )
    tokens_used = response.usage.total_tokens
    total_tokens_used += tokens_used
    total_embeddings += 1
    if (total_embeddings % 10) == 0:
        print(
            f"Generated {total_embeddings} embeddings so far with a total of {total_tokens_used} tokens used. ({int((total_embeddings / len(quotes)) * 100)}%)"
        )
    return response.data[0].embedding


embedding_df = pd.DataFrame(columns=["quote", "author", "embedding"])


for index, quote in enumerate(quotes):
    current_quote = quote[0]
    try:
        current_author = quote[1]
    except IndexError:
        current_author = "Unknown"
    embedding = get_quote_embedding(current_quote)
    embedding_df.loc[index] = [current_quote, current_author, embedding]


embedding_df.to_csv(
    current_directory / "embedding_db.csv", index=False, encoding="utf-8"
)

print(
    f"""
Generated {total_embeddings} embeddings with a total of {total_tokens_used} tokens used. (Done!)
Succesfully saved embeddings to embedding_db.csv, printing dataframe head:
{embedding_df.head(5)}

    """
)

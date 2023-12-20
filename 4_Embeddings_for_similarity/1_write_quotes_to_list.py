import json
from pathlib import Path


current_directory = Path(__file__).parent
raw_quotes = []


with open(current_directory / "quotes.txt", "r", encoding="utf-8") as file:
    raw_quotes = file.read().split("\n")


with open(current_directory / "quotes.json", "w", encoding="utf-8") as file:
    quotes: list = []
    for quote in raw_quotes:
        # split the quote only on the first occurrence of the '-' character
        quotes.append(quote.split(" - ", 1))
    json.dump(quotes, file, indent=2)

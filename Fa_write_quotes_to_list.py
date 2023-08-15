quotes = []

with open("Fx_quotes.txt", "r") as file:
    quotes = file.read().split("\n")


with open("Fx_quotes.py", "w") as file:
    file.write("quotes = [\n")
    for quote in quotes:
        # split the quote only on the first occurrence of the '-' character
        quote = quote.split(" - ", 1)
        file.write(f"{quote},\n")
    file.write("]")

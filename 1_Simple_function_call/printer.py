class ColorPrinter:
    _colors = {
        "yellow": "\033[33m",
        "green": "\033[32m",
        "blue": "\033[34m",
        "purple": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "closing_tag": "\033[00m",
    }

    def _get_current_color(index, no_of_messages) -> str:
        if index == 0:
            return ColorPrinter._colors["yellow"]
        elif index == no_of_messages - 1:
            return ColorPrinter._colors["purple"]
        elif index % 2 == 0:
            return ColorPrinter._colors["blue"]
        return ColorPrinter._colors["green"]

    def color_print(messages) -> None:
        no_of_messages = len(messages)
        cyan_open_tag = ColorPrinter._colors["cyan"]
        color_closing_tag = ColorPrinter._colors["closing_tag"]
        print(f"\n{cyan_open_tag}###### Conversation History ######{color_closing_tag}")
        for index, message in enumerate(messages):
            color = ColorPrinter._get_current_color(index, no_of_messages)
            print(f"{color}{message}{color_closing_tag}")
        print(f"{cyan_open_tag}##################################{color_closing_tag}\n")

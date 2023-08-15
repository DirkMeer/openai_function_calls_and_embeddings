class ColorPrinter:
    _color_mapping = {
        "system": "\033[33m",  # Yellow
        "user": "\033[32m",  # Green
        "function": "\033[34m",  # Blue
        "assistant": "\033[35m",  # Purple
        "header": "\033[36m",  # Cyan
        "undefined": "\033[37m",  # White
        "closing_tag": "\033[00m",
    }

    def _color_text_line(message) -> str:
        color_closing_tag = ColorPrinter._color_mapping["closing_tag"]
        try:
            role = message["role"]
            color_open_tag = ColorPrinter._color_mapping[role]
        except KeyError:
            role = "undefined"
            color_open_tag = ColorPrinter._color_mapping[role]
        try:
            if message["content"]:
                message = message["content"]
            else:
                function_name = message["function_call"]["name"]
                function_args = message["function_call"]["arguments"]
                message = f"{function_name}({function_args})"
        except KeyError:
            message = "undefined"
        return f"{color_open_tag}{role} : {message}{color_closing_tag}"

    def color_print(messages) -> None:
        cyan_open_tag = ColorPrinter._color_mapping["header"]
        color_closing_tag = ColorPrinter._color_mapping["closing_tag"]
        print(f"\n{cyan_open_tag}###### Conversation History ######{color_closing_tag}")
        for message in messages:
            print(ColorPrinter._color_text_line(message))
        print(f"{cyan_open_tag}##################################{color_closing_tag}\n")

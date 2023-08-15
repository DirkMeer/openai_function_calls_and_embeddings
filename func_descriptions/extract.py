describe_extract_dates = {
    "name": "make_list_of_dates",
    "description": """
        Use this function to get a nice representation of historical dates and their happenings.

        Input argument instructions:
        The input should be an array containing arrays structured exactly like this ['date', 'happening'].
        Each item in each list should be a string and the date must come first.
        The happening should be single-sentence description (e.g. 'Battle of Waterloo - Napoleon defeated').
        MAKE SURE YOU INCLUDE ALL HAPPENINGS FOR WHICH YOU CAN FIND A DATE (not unknown dates!), but only include happenings you extracted from the user provided text.
        Example: [1592, "Japanese invasions of Korea"],
        """,
    "parameters": {
        "type": "object",
        "properties": {
            "list_of_happenings": {
                "type": "array",
                "description": "an array containing arrays with dates in index 0 and happenings in index 1.",
                "items": {
                    "type": "array",
                    "description": "an array containing a date and a happening. THE DATE ALWAYS COMES FIRST, the happening second.",
                    "items": {
                        "date": {
                            "type": "string",
                            "description": "the date for the happening.",
                        },
                        "happening": {
                            "type": "string",
                            "description": "a single-sentence description for the happening (e.g. 'Battle of Waterloo - Napoleon defeated')",
                        },
                    },
                },
            }
        },
        "required": ["list_of_happenings"],
    },
}

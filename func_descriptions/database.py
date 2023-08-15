def describe_get_info_from_database(schema):
    return {
        "name": "get_info_from_database",
        "description": """Use this function to answer questions about amazon customers' reviews and their helpfulness.
        If the user asks for a customer's name, this will refer to their ProfileName specifically.
        The 'HelpfulnessNumerator' is the number of 'helpful' votes the review has received.
        The 'HelpfulnessDenominator' is the total number 'helpful' or 'unhelpful' votes the review has received.
        The 'Score' column indicates the rating between 1 and 5 the user gave the product in their review.
        You are not to use the 'UserId' column in your queries, use the 'ProfileName' as identifier instead.
        Argument should be a fully formed SQL query.""",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"""
                        SQL query extracting info from the database to answer the user's question.
                        The database schema is as follows:
                        {schema}
                        The query should be returned in string format as a single command.
                        """,
                }
            },
            "required": ["query"],
        },
    }

"""LLM output structure for ReXia.AI."""


class LLMOutput:
    """
    LLM output structure for ReXiaAI.

    This class provides static methods to get the output structure for different types of responses.
    """

    @staticmethod
    def get_output_structure() -> str:
        """
        Get the output structure with examples.

        Returns:
            A string representing the output structure with examples.
        """
        return (
            "{\n"
            '    "question": "string",\n'
            '    "plan": "list",\n'
            '    "answer": "string",\n'
            '    "confidence_score": "number between 0 and 100 percent",\n'
            '    "chain_of_reasoning": ["list"]\n'
            '    "tool_calls": ["list of tool calls, leave blank if you are not a tool calling agent."]\n'
            "}"
        )

    @staticmethod
    def get_json_scehma():
        """
        Get the output schema.

        Returns:
            A string representing the output schema.
        """

        schema = {
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "plan": {"type": "array", "items": {"type": "string"}},
                "answer": {"type": "string"},
                "confidence_score": {"type": "integer"},
                "chain_of_reasoning": {"type": "array", "items": {"type": "string"}},
                "tool_calls": {"type": "array", "items": {"type": "string"}},
            },
            "required": [
                "question",
                "answer",
                "confidence_score",
                "chain_of_reasoning",
                "plan",
                "tool_calls",
            ],
        }

        return schema

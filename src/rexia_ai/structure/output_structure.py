"""LLM output structure for ReXia.AI."""


class LLMOutput:
    """
    LLM output structure for ReXiaAI.

    This class provides static methods to get the output structure for different types of responses.
    """

    @staticmethod
    def get_output_structure() -> str:
        """
        Get the output structure with generic placeholders.

        Returns:
            A string representing the generic output structure.
        """
        return (
            "{\n"
            '    "question": "The task exactly as written",\n'
            '    "plan": [\n'
            '        "Step 1 of the plan",\n'
            '        "Step 2 of the plan",\n'
            '        "Add more steps as needed"\n'
            "    ],\n"
            '    "answer": [\n'
            '        "First line",\n'
            '        "Second line",\n'
            '        "Third line",\n'
            '        "Add more lines as needed, preserving indentation"\n'
            "    ],\n"
            '    "confidence_score": 0.0,\n'
            '    "chain_of_reasoning": [\n'
            '        "First step in the reasoning process",\n'
            '        "Second step in the reasoning process",\n'
            '        "Add more steps as needed"\n'
            "    ],\n"
            '    "tool_calls": [\n'
            '        "First tool call if any",\n'
            '        "Second tool call if any",\n'
            '        "Leave this array empty if no tools were used"\n'
            "    ]\n"
            "}"
        )

    @staticmethod
    def get_json_schema():
        """
        Get the output schema.

        Returns:
            A dict representing the output schema.
        """

        schema = {
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "plan": {"type": "array", "items": {"type": "string"}},
                "answer": {
                    "type": "array",
                    "items": {"oneOf": [{"type": "string"}, {"type": "object"}]},
                },
                "confidence_score": {"type": "number"},
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

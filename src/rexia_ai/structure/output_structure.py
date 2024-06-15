"""LLM output structure for ReXiaAI."""

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
            "    \"question\": \"string\",\n"
            "    \"answer\": \"string\",\n"
            "    \"confidence_score\": \"number between 0 and 100 percent\",\n"
            "    \"chain of reasoning\": [\"string\"]\n"
            "}"
        )

    @staticmethod
    def get_plan_output_structure() -> str:
        """
        Get the plan output structure.

        Returns:
            A string representing the plan output structure.
        """
        return (
            "{\n"
            "    \"task\": \"[Task/Problem Type]\",\n"
            "    \"plan\": {\n"
            "        \"Understand\": \"[Describe the problem and its key elements.]\",\n"
            "        \"Decompose\": \"[Break the problem into manageable parts.]\",\n"
            "        \"Represent\": \"[Represent the problem using appropriate tools or models.]\",\n"
            "        \"Solve\": \"[Apply techniques or algorithms to solve the problem.]\",\n"
            "        \"Verify\": \"[Check the solution against the problem statement.]\"\n"
            "    },\n"
            "    \"confidence_score\": \"[Number between 0 and 100 percent]\",\n"
            "    \"chain_of_reasoning\": \"[Describe the logical steps taken to arrive at the solution.]\"\n"
            "}"
        )
""" llm output structure for ReXiaAI """


class LLMOutput:
    """llm output structure for ReXiaAI"""

    @staticmethod
    def get_output_structure():
        """Get the output structure with examples"""
        return (
            "{\n"
            "    \"question\": \"string\",\n"
            "    \"answer\": \"string\",\n"
            "    \"confidence_score\": \"number between 0 and 100 percent\",\n"
            "    \"chain of reasoning\": [\"string\"]\n"
            "}"
        )

    @staticmethod
    def get_plan_output_structure():
        """Get the plan output structure"""
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

    @staticmethod
    def get_approval_output_structure():
        """Get the approval output structure"""
        return (
            "{\n"
            "    \"task\": \"<Task Name: String>\",\n"
            "    \"approval\": \"<Approval Status: String, either 'COMPLETED' or 'INCOMPLETE'>\",\n"
            "    \"confidence_score\": <Confidence Score: Integer between 0 and 100>,\n"
            "    \"chain_of_reasoning\": [<Reasoning Steps: List of strings, each string is a step in the reasoning process>],\n"
            "    \"accepted_answer\": \"<Answer Value: String, the final answer to the task. If the answer is a list or another data structure, convert it to a string representation.>\"\n"
            "}"
        )
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
            "        \"Understand the Problem\": "
            "\"[Instructions for understanding the problem statement, identifying key information, constraints, and objectives.]\",\n"
            "        \"Break Down the Problem\": "
            "\"[Instructions for decomposing the problem into smaller sub-problems or steps, and identifying relevant concepts, principles, or techniques required for each sub-problem.]\",\n"
            "        \"Represent the Problem\": "
            "\"[Instructions for representing each sub-problem or step mathematically, logically, or visually using appropriate notation, equations, diagrams, or models. Include guidance on defining variables, relationships, or patterns as needed.]\",\n"
            "        \"Apply Techniques and Solve\": "
            "\"[Instructions for applying relevant techniques, operations, or algorithms to solve each sub-problem, and checking the validity and reasonableness of intermediate results.]\",\n"
            "        \"Combine and Verify Solution\": "
            "\"[Instructions for combining the solutions to the sub-problems to obtain the final solution, and verifying the final solution by checking against the problem statement and constraints. Include guidance on revisiting previous steps and refining the approach if the solution is incorrect or unsatisfactory.]\"\n"
            "    },\n"
            "    \"confidence_score\": \"[Number between 0 and 100 percent]\",\n"
            "    \"chain of reasoning\": \"[Chain of Reasoning]\"\n"
            "}"
        )

    @staticmethod
    def get_approval_output_structure():
        """Get the approval output structure"""
        return (
            "{\n"
            "    \"task\": \"<Task Name>\",\n"
            "    \"approval\": \"<Approval Status>\",\n"
            "    \"confidence_score\": <Confidence Score>,\n"
            "    \"chain_of_reasoning\": [<Reasoning Steps>],\n"
            "    \"accepted_answer\": {\n"
            "        \"type\": \"<Answer Type>\",\n"
            "        \"value\": \"<Answer Value>\"\n"
            "    }\n"
            "}"
        )
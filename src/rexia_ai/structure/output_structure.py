""" llm output structure for ReXiaAI """


class LLMOutput:
    """llm output structure for ReXiaAI"""

    @staticmethod
    def get_output_structure():
        """Get the output structure with examples"""
        return """
        Output Structure:
        {
            "question": "string",
            "answer": "string",
            "confidence_score": "number",
            "chain of reasoning": ["string"]
        }
        """

    @staticmethod
    def get_plan_output_structure():
        """Get the plan output structure"""
        return """
        {
            "task": "string",
            "plan": "string",
            "confidence_score": "number"
            "chain of reasoning": ["string"]
        }
        """

    @staticmethod
    def get_approval_output_structure():
        """Get the approval output structure"""
        return """
        {
            "task": "string",
            "approval": "string",
            "confidence_score": "number"
            "chain of reasoning": ["string"]
            "accepted answer": "string"
        }
        """

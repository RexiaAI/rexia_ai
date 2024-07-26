"""Worker class for ReXia.AI's general task execution and problem-solving system."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
## Role Overview
As a worker agent for ReXia.AI, your role is to complete tasks based on the collaboration chat and task context.

## Task Requirements
- Task requirements and output format are provided in the chat.
- Pay attention to constraints and the required detail in your response.
- Pay particularly close attention to the plan and any tool messages in the chat.
- You must follow the given plan and use information from tool messages.

## Task Complexity
Tasks can vary in complexity, from simple ("What is the capital city of France?") to complex ("Analyze the factors that contributed to the French Revolution").

## Limitations Awareness
Be mindful of limitations like resource constraints, time constraints, or ethical considerations.

## Critical Thinking
- Apply critical thinking and problem-solving skills.
- Identify challenges, make informed decisions, and justify your reasoning.

## Response Quality
- Ensure your response is clear, concise, and informative.
- Avoid unnecessary complexity.

## Response Guidelines
- Don't add reasoning outside your chain of reasoning.
- Don't use unexplained abbreviations or shorthand.
- Use messages from tools in your answer.
- Ensure your answer matches the task and is complete and detailed.

## Tool Messages
If there are tool messages provided by tools, you should use them to provide accurate answers.

## Formatting
Apply specific formatting requests only within the answer.
"""


class Worker(BaseWorker):
    """
    A non-specialized worker for ReXia.AI's agent system, designed for general task execution.

    This worker is responsible for processing and completing a wide range of tasks
    based on the collaboration chat, task context, and any additional information
    provided. It's capable of handling tasks varying from simple queries to complex
    analytical problems, ensuring responses are clear, concise, and aligned with
    the given instructions and constraints.

    Attributes:
        model (Any): The language model used for processing tasks and generating responses.
        verbose (bool): Flag for enabling verbose output mode.

    Inherits from:
        BaseWorker: Provides core functionality for AI workers in the ReXia.AI system.
    """

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
    ):
        """
        Initialize a Worker instance.

        Args:
            model (Any): The language model to be used for task processing and response generation.
            verbose (bool, optional): Enable verbose output for debugging. Defaults to False.
        """
        super().__init__(model, verbose=verbose)

    def create_prompt(self, task: str, messages: List[str]) -> str:
        """
        Create a comprehensive prompt for the model based on the task, context, and memory.

        This method combines the predefined prompt with task-specific information,
        relevant messages from the collaboration chat, and any pertinent memory
        to create a detailed prompt for the model to generate an appropriate response.

        Args:
            task (str): The specific task or question to be addressed.
            messages (List[str]): A list of relevant messages from the collaboration chat.

        Returns:
            str: A formatted prompt string for the model to generate a task response.
        """
        prompt = super().create_prompt(PREDEFINED_PROMPT, task, messages)
        return prompt
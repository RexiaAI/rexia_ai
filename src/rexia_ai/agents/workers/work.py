"""Worker class for ReXia.AI."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
As a worker agent for ReXia.AI, your role is to complete tasks based on the collaboration chat and task context.

Task requirements and output format are provided in the chat. Pay attention to constraints and the required
detail in your response. Pay particularly close attention to the plan and any tool messages in the chat,
you must follow the given plan and use information from tool messages.

Tasks can vary in complexity, from simple ("What is the capital city of France?") to complex
("Analyze the factors that contributed to the French Revolution").

Be mindful of limitations like resource constraints, time constraints, or ethical considerations.

Apply critical thinking and problem-solving skills. Identify challenges, make informed decisions, and justify
your reasoning.

Ensure your response is clear, concise, and informative. Avoid unnecessary complexity. 

Don't add reasoning outside your chain of reasoning. Don't use unexplained abbreviations or shorthand. 
Use messages from tools in your answer. Ensure your answer matches the task and is complete and detailed.

Consider and incorporate information from tool messages in the chat. Attribute any data used from these messages.

Apply specific formatting requests only within the answer.
"""


class Worker(BaseWorker):
    """
    A non-specialised worker for a ReXia AI agent.

    This worker is responsible for completing the task based on the
    collaboration chat and the task context.
    """

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
        max_attempts: int = 3,
    ):
        """
        Initialize a Worker instance.

        Args:
            model: The model used by the worker.
            verbose: A flag used for enabling verbose mode. Defaults to False.
        """
        super().__init__(model, verbose=verbose, max_attempts=max_attempts)

    def create_prompt(self, task: str, messages: List[str], memory: Any) -> str:
        """Create a prompt for the model."""
        prompt = super().create_prompt(PREDEFINED_PROMPT, task, messages, memory)

        return prompt

"""Worker class for ReXia.AI."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
    You are a worker agent.
    You are part of a team working on a task.
    Read the collaboration chat and the task fully to understand the context and plan.
    Your job is to complete the task.
    Do not add any explanation or reasoning to your answer outside your chain of reasoning.
    Don't use abbreviations or shorthand in your work if they are not explained in the answer.
    If there is a message from tools in the collaboration chat, you must use the message from tools in your answer.
    Ensure that your answer matches the task you have been given.
    Always give a full and complete response using the data provided in the collaboration chat.
    You should be detailed and provide all information you think is relevant to the task.
    Unless the task specifies summarisation or conciseness, you should provide a detailed response.
"""

class Worker(BaseWorker):
    """
    A non-specialised worker for a ReXia AI agent.

    This worker is responsible for completing the task based on the collaboration chat and the task context.

    Attributes:
        model: The model used by the worker.
    """

    model: Any

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
    ):
        """
        Initialize a Worker instance.

        Args:
            model: The model used by the worker.
            verbose: A flag used for enabling verbose mode. Defaults to False.
        """
        super().__init__(model, verbose=verbose)

    def create_prompt(self, task: str, messages: List[str]) -> str:
        """
        Create a prompt for the model.

        The prompt is created by combining a predefined string with the task
        and the messages from the collaboration chat.

        Args:
            task: The task for which the prompt is created.
            messages: The messages from the collaboration chat.

        Returns:
            The created prompt as a string.
        """
        if not messages:
            raise ValueError("Messages cannot be empty")

        prompt = (
            PREDEFINED_PROMPT
            + "\n\n"
            + self.get_structured_output_prompt()
            + "\n\n"
            + self.format_task_and_messages(task, messages)
        )
        return prompt

    def format_task_and_messages(self, task: str, messages: List[str]) -> str:
        """
        Format the task and messages for the prompt.

        Args:
            task: The task for which the prompt is created.
            messages: The messages from the collaboration chat.

        Returns:
            The formatted task and messages as a string.
        """
        formatted = f"Task: {task}\n\nCollaboration Chat:\n\n" + "\n\n".join(messages)
        return formatted
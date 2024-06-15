"""Module for the FinaliseWorker class in ReXia AI."""

from typing import Any, List
from ...base import BaseWorker


class FinaliseWorker(BaseWorker):
    """
    A specialised reflection worker for a ReXia.AI agent.

    This worker is responsible for reflecting on the collaboration chat and
    providing an improved answer to the task based on this reflection.

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
        Initialize a FinaliseWorker instance.

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
        prompt = (
            f"""
                You are a specialist reflection agent.
                You are part of a team working on a task.
                Your job is to read the collaboration chat and reflect on how to improve the answer to the task.
                Based on your reflection, you should provide a revised answer to the task that
                improves on the original answer.
                Don't use abbreviations or shorthand in your reflection if they are not explained in the answer.
                Don't give instructions on how to improve the answer, just provide the improved answer.
                If there is a message from tools in the collaboration chat, you must use the message from tools in your answer.
                Ensure that your answer matches the task you have been given. 
                Always give a full and complete response using the data provided in the collaboration chat.
                You should be detailed and provide all information you think is relevant to the task.
                Unless the task specifies summarisation or conciseness, you should provide a detailed response.
            """
            + "\n\n"
            + self.get_structured_output_prompt()
            + "\n\n"
            + f"Task: {task}\n\nCollaboration Chat:\n\n" + "\n\n".join(messages)
        )
        return prompt
"""FinaliseWorker class in ReXia.AI."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
You are a specialist reflection agent for the ReXia.AI system.
Your task is to read the collaboration chat and provide a revised and improved
answer to the original task, based on the information and discussions in the chat.

Your revised answer should follow the output structure provided. 
This structure includes fields for the question, answer, confidence score, and
a chain of reasoning.

If there are messages from tools in the collaboration chat, you should
carefully consider and incorporate the information provided by these tools
into your revised answer. Clearly attribute any information or data used from
the tool messages.

Your revised answer should include a clear and logical chain of reasoning that
explains the steps and thought process you followed to arrive at your answer.
This chain of reasoning should be detailed and comprehensive, leaving no gaps
or assumptions.

If the collaboration chat does not provide enough information to fully answer
the task, you should clearly state the limitations and provide the best
possible answer based on the available information.

If there is conflicting information in the collaboration chat, you should
attempt to reconcile the conflicts and provide a coherent answer. If the
conflicts cannot be resolved, you should acknowledge the conflicting
information and provide your best interpretation.

Don't use abbreviations or shorthand in your reflection if they are not
explained in the answer.
Don't give instructions on how to improve the answer, just provide the
improved answer.
Ensure that your answer matches the task you have been given.
Always give a full and complete response using the data provided in the
collaboration chat.
You should be detailed and provide all information you think is relevant to
the task.
Unless the task specifies summarisation or conciseness, you should provide a
detailed response.
"""


class FinaliseWorker(BaseWorker):
    """
    A specialised reflection worker for a ReXia.AI agent.

    This worker is responsible for reflecting on the collaboration chat and
    providing an improved answer to the task based on this reflection.

    Attributes:
        model: The model used by the worker.
        verbose: A flag used for enabling verbose mode.
    """

    model: Any
    verbose: bool

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

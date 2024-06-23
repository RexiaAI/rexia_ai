"""FinaliseWorker class in ReXia.AI."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
As a reflection agent for ReXia.AI, your role is to provide a revised answer based on the collaboration chat.

Pay particularly close attention to the plan and any tool messages in the chat,
you must follow the given plan and use information from tool messages.

Your revised answer should follow the provided output structure.

Include a detailed chain of reasoning in your answer, explaining your thought process. If the chat lacks enough
information for a full answer, state the limitations and provide the best possible answer.

Reconcile any conflicting information in the chat and provide a coherent answer. If conflicts can't be resolved, 
acknowledge them and provide your best interpretation.

Avoid abbreviations or shorthand unless explained in the answer. Don't give instructions to improve the answer, 
just provide the improved one. Ensure your answer matches the task and is complete and detailed.

Apply specific formatting requests only within the answer.
"""


class FinaliseWorker(BaseWorker):
    """
    A specialised reflection worker for a ReXia.AI agent.

    This worker is responsible for reflecting on the collaboration chat and
    providing an improved answer to the task based on this reflection.
    """

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
        max_attempts: int = 3,
    ):
        """
        Initialize a FinaliseWorker instance.

        Args:
            model: The model used by the worker.
            verbose: A flag used for enabling verbose mode. Defaults to False.
            max_attempts: The maximum number of attempts to get a valid response from the model. Defaults to 3.
        """
        super().__init__(model, verbose=verbose, max_attempts=max_attempts)

    def create_prompt(self, task: str, messages: List[str], memory: Any) -> str:
        """Create a prompt for the model."""
        prompt = super().create_prompt(PREDEFINED_PROMPT, task, messages, memory)

        return prompt

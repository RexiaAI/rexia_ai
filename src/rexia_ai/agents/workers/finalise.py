"""FinaliseWorker class for ReXia.AI's reflection and answer refinement process."""

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
    A specialized reflection worker for ReXia.AI's agent system.

    This worker is responsible for analyzing the collaboration chat,
    reflecting on the information provided, and generating an improved,
    comprehensive answer to the given task. It focuses on integrating
    information from various sources, following predefined plans, and
    providing detailed, coherent responses.

    Attributes:
        model (Any): The language model used for generating responses.
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
        Initialize a FinaliseWorker instance.

        Args:
            model (Any): The language model to be used for generating responses.
            verbose (bool, optional): Enable verbose output for debugging. Defaults to False.
        """
        super().__init__(model, verbose=verbose)

    def create_prompt(self, task: str, messages: List[str], memory: Any) -> str:
        """
        Create a prompt for the model to generate a refined answer.

        This method combines the predefined prompt with task-specific information,
        collaboration messages, and any relevant memory to create a comprehensive
        prompt for the model.

        Args:
            task (str): The original task or question to be answered.
            messages (List[str]): A list of messages from the collaboration chat.
            memory (Any): Additional context or information stored in the agent's memory.

        Returns:
            str: A formatted prompt string for the model to generate a refined answer.

        Note:
            The returned prompt includes instructions for the model to follow the
            collaboration plan, integrate tool messages, and provide a detailed,
            well-reasoned response.
        """
        prompt = super().create_prompt(PREDEFINED_PROMPT, task, messages, memory)
        return prompt
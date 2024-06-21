"""FinaliseWorker class in ReXia.AI."""

from typing import Any
from ...base import BaseWorker

PREDEFINED_PROMPT = """
As a reflection agent for ReXia.AI, your role is to provide a revised answer based on the collaboration chat. 

Your revised answer should follow the provided output structure.

Consider and incorporate information from tool messages in the chat. Attribute any data used from these messages.

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

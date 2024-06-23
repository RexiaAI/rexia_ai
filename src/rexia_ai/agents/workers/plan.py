"""PlanWorker class in ReXia.AI."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
As a planning agent for ReXia.AI, your role is to create a prompt-based plan to guide task completion.

You're an advanced large language model, capable of generating clear, best practice, prompt-based plans.

Your plan should instruct a large language model on the fashion in which the task should be completed.

The agents following your plan will have access to tools and a collaboration chat with which to complete the task.

Your plan should be framed as a direct prompt for the large language model, not as an explanation or a narrative.

Your plan should be self-contained, the large language model will receive it as a single prompt and act on it.
Your plan should contain nothing that cannot be performed with a single prompt.
A plan cannot consist of do X then do Y. It must all be achievable in a single execution of the model.

Make sure to utilise best practice prompting techniques in your plan, such as expert roles, context, background, and examples.

"""


class PlanWorker(BaseWorker):
    """
    A specialised planning worker for a ReXia.AI agent.

    This worker is responsible for thinking through the task and creating a plan to complete it.
    """

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
        max_attempts: int = 3,
    ):
        """
        Initialize a PlanWorker instance.

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

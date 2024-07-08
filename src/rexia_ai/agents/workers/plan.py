"""PlanWorker class for ReXia.AI's task planning and prompt generation system."""

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
    A specialized planning worker for ReXia.AI's agent system.

    This worker is responsible for analyzing tasks, devising strategies,
    and creating comprehensive, prompt-based plans to guide the completion
    of tasks within the ReXia.AI ecosystem. It generates plans that can be
    executed by large language models in a single prompt, incorporating
    best practices in AI prompting techniques.

    Attributes:
        model (Any): The language model used for generating plans.
        verbose (bool): Flag for enabling verbose output mode.
        max_attempts (int): Maximum number of attempts to generate a valid plan.

    Inherits from:
        BaseWorker: Provides core functionality for AI workers in the ReXia.AI system.
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
            model (Any): The language model to be used for generating plans.
            verbose (bool, optional): Enable verbose output for debugging. Defaults to False.
            max_attempts (int, optional): Maximum number of attempts to generate a valid plan. Defaults to 3.
        """
        super().__init__(model, verbose=verbose, max_attempts=max_attempts)

    def create_prompt(self, task: str, messages: List[str], memory: Any) -> str:
        """
        Create a prompt for the model to generate a task completion plan.

        This method combines the predefined planning prompt with task-specific information,
        relevant messages, and any pertinent memory to create a comprehensive prompt
        for the model to generate an effective plan.

        Args:
            task (str): The task or problem statement for which a plan is needed.
            messages (List[str]): A list of relevant messages or context for the task.
            memory (Any): Additional context or information stored in the agent's memory.

        Returns:
            str: A formatted prompt string for the model to generate a task completion plan.

        Note:
            The generated plan is designed to be a self-contained, single-prompt instruction
            set that incorporates best practices in AI prompting, including expert roles,
            context setting, and relevant examples when applicable.
        """
        prompt = super().create_prompt(PREDEFINED_PROMPT, task, messages, memory)
        return prompt
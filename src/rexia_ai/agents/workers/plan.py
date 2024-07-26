"""PlanWorker class for ReXia.AI's task planning and prompt generation system."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
## Role and Capabilities
You are a planning agent for ReXia.AI, tasked with creating a prompt-based plan to guide task completion. 
As an advanced large language model, you are capable of generating clear, best practice, prompt-based plans.

## Plan Requirements
Your plan should:
- Instruct a large language model on how to complete the task
- Be framed as a direct prompt, not an explanation or narrative
- Be self-contained and executable in a single prompt
- Not include multi-step instructions (no "do X then do Y")

## Available Resources
Agents following your plan will have access to:
- Tools
- A collaboration chat

## Best Practices
Utilize best practice prompting techniques in your plan, such as:
- Expert roles
- Context
- Background
- Examples

## Important Notes
- Your plan will be received and acted upon by the large language model as a single prompt
- Ensure all instructions can be performed in a single execution of the model
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

    Inherits from:
        BaseWorker: Provides core functionality for AI workers in the ReXia.AI system.
    """

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
    ):
        """
        Initialize a PlanWorker instance.

        Args:
            model (Any): The language model to be used for generating plans.
            verbose (bool, optional): Enable verbose output for debugging. Defaults to False.
        """
        super().__init__(model, verbose=verbose)

    def create_prompt(self, task: str, messages: List[str]) -> str:
        """
        Create a prompt for the model to generate a task completion plan.

        This method combines the predefined planning prompt with task-specific information,
        relevant messages, and any pertinent memory to create a comprehensive prompt
        for the model to generate an effective plan.

        Args:
            task (str): The task or problem statement for which a plan is needed.
            messages (List[str]): A list of relevant messages or context for the task.

        Returns:
            str: A formatted prompt string for the model to generate a task completion plan.

        Note:
            The generated plan is designed to be a self-contained, single-prompt instruction
            set that incorporates best practices in AI prompting, including expert roles,
            context setting, and relevant examples when applicable.
        """
        prompt = super().create_prompt(PREDEFINED_PROMPT, task, messages)
        return prompt
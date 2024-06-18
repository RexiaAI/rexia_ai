"""PlanWorker class in ReXia.AI."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
You are a specialist planning agent for the ReXia.AI system, which is designed
to tackle complex tasks and problems. Your role is to create a comprehensive
plan that will guide the team in completing the given task effectively and
efficiently. 

You are an advanced AI system capable of performing a wide range of tasks. 
Before executing any task, it's important to devise a plan that breaks down the 
problem into a sequence of steps or subtasks that you can execute directly.
When presented with a task, your first step should be to generate a plan that 
outlines the necessary actions you need to take to complete the task successfully. 
This plan should be tailored for your own execution, not for human comprehension.
The plan should be structured as a numbered list of concise, executable instructions. 
Each step should involve specific operations, calculations, logical operations, or
information retrieval that you can perform directly. Avoid including explanations,
rationales, or justifications for each step, as the plan is intended solely for your
own execution.

Keep the plan focused and concise, including only the essential steps required to solve
the problem. The plan should be self-contained and not rely on external resources or human
intervention.

Once you have generated the plan, you can proceed to execute each step sequentially,
using your capabilities to perform the necessary operations and actions.
If any step requires additional planning or decomposition, you should generate
a sub-plan following the same principles.

Remember, the goal is to create a plan that serves as a clear roadmap for your own execution,
without the need for human interpretation or guidance.
"""

class PlanWorker(BaseWorker):
    """
    A specialised planning worker for a ReXia.AI agent.

    This worker is responsible for thinking through the task and creating a plan to complete it.

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
        Initialize a PlanWorker instance.

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
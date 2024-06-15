"""Module for the PlanWorker class in ReXia AI."""

from typing import Any, List
from ...base import BaseWorker
from ...thought_buffer import BufferManager


class PlanWorker(BaseWorker):
    """
    A specialised planning worker for a ReXia.AI agent.

    This worker is responsible for thinking through the task and creating a plan to complete it.

    Attributes:
        model: The model used by the worker.
        buffer: The buffer manager used for storing and retrieving thought templates.
    """

    model: Any
    buffer: BufferManager

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
        self.buffer = BufferManager()

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
                You are a specialist planning agent.
                You are part of a team working on a task.
                Your job is to think through the task and create a plan to complete it.
                If you are provided with a plan, you should review it, check its accuracy, and provide a refined
                version if necessary, or simply supply the plan if it is correct.
                Don't use abbreviations or shorthand in your plan.
                The plan should always be as simple and clear as possible.
            """
            + "\n\n"
            + f"Previous Plan: {self._get_thought_template(task)}"
            + "\n\n"
            + self.get_plan_structured_output_prompt()
            + "\n\n"
            + f"Task: {task}\n\nCollaboration Chat:\n\n" + "\n\n".join(messages)
        )
        return prompt

    def _get_thought_template(self, task: str) -> str:
        """
        Retrieve the thought template for the given task.

        Args:
            task: The task for which the thought template is retrieved.

        Returns:
            The thought template as a string, or a message indicating that no thought template was found.
        """
        thought_template = self.buffer.get_template(task)
        if thought_template:
            thought_template_str = str(thought_template)  # convert ScoredPoint object to string
            start_index = thought_template_str.find("'plan': '") + len("'plan': '")
            end_index = thought_template_str.find("'}", start_index)
            plan = thought_template_str[start_index:end_index]
            return plan
        else:
            return "No thought template found for task."
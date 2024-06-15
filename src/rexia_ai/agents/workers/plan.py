"""PlanWorker class in ReXia.AI."""

from typing import Any, List
from ...base import BaseWorker
from ...thought_buffer import BufferManager

PREDEFINED_PROMPT = """
You are a specialist planning agent for the ReXia.AI system, which is designed
to tackle complex tasks and problems. Your role is to create a comprehensive
plan that will guide the team in completing the given task effectively and
efficiently. The plan should outline a step-by-step approach, breaking down
the task into manageable components and addressing potential challenges or
obstacles. Your plan should be clear, concise, and easy to follow, ensuring
that all team members understand their roles and responsibilities.

It is crucial that your plan follows the structured output format specified by
the get_plan_structured_output_prompt() function. This format includes
sections for understanding the problem, decomposing it into parts,
representing the problem using appropriate tools or models, solving the
problem, and verifying the solution. Adhering to this structure will ensure
that your plan is comprehensive and easy to follow.

Your plan should be as clear and simple as possible, avoiding unnecessary
jargon or complexity. Use plain language and straightforward explanations to
ensure that your plan can be easily understood and followed by all team
members, regardless of their technical expertise.

If an existing plan or thought template is provided, carefully review it for
accuracy and completeness. Identify any areas that may require refinement or
additional details. If the existing plan is satisfactory, you may choose to
provide it as is. However, if you believe improvements can be made, provide a
refined version of the plan that addresses any shortcomings or gaps.

Don't use abbreviations or shorthand in your plan unless they are clearly
explained. The plan should always be as simple and clear as possible.
"""

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
            PREDEFINED_PROMPT
            + "\n\n"
            + f"Previous Plan: {self._get_thought_template(task)}"
            + "\n\n"
            + self.get_plan_structured_output_prompt()
            + "\n\n"
            + self.format_task_and_messages(task, messages)
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
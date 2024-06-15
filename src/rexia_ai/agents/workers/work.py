"""Worker class for ReXia.AI."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
You are a worker agent for the ReXia.AI system, an advanced AI platform
designed to tackle complex tasks and problems. Your role is crucial in
completing the given task effectively and efficiently, based on the
collaboration chat and the task context.

The task requirements and expected output format will be provided in the
collaboration chat. Pay close attention to any constraints or limitations, as
well as the level of detail or conciseness required in your response.

Remember, you are part of a collaborative team. Communicate effectively with
other team members, share relevant information, and coordinate your efforts to
ensure a cohesive and efficient approach to the task. Do not hesitate to seek
clarification or additional input from the team when needed.

You can take an iterative approach to completing the task, refining your
approach and incorporating feedback or additional information from the
collaboration chat as needed.

Here is an example of a task with varying levels of complexity:

Simple Task: "What is the capital city of France?"
Moderate Task: "Provide a brief overview of the French Revolution, including
the key events, leaders, and its impact on France and Europe."
Complex Task: "Analyze the social, political, and economic factors that
contributed to the outbreak of the French Revolution, and discuss how its
ideals and consequences influenced subsequent revolutions and democratic
movements around the world."

Be mindful of potential limitations or constraints, such as resource
constraints, time constraints, or ethical considerations, and adjust your
approach accordingly.

Apply critical thinking and problem-solving skills when completing the task.
Identify and address potential challenges, make informed decisions, and
justify your approach or reasoning.

Ensure that your response is clear, concise, and easy to understand. Avoid
unnecessary verbosity or complexity, and focus on providing a well-structured
and informative answer.

Do not add any explanation or reasoning to your answer outside your chain of
reasoning.
Don't use abbreviations or shorthand in your work if they are not explained in
the answer.
If there is a message from tools in the collaboration chat, you must use the
message from tools in your answer.
Ensure that your answer matches the task you have been given.
Always give a full and complete response using the data provided in the
collaboration chat.
You should be detailed and provide all information you think is relevant to
the task.
Unless the task specifies summarisation or conciseness, you should provide a
detailed response.
"""

class Worker(BaseWorker):
    """
    A non-specialised worker for a ReXia AI agent.

    This worker is responsible for completing the task based on the
    collaboration chat and the task context.

    Attributes:
        model: The model used by the worker.
    """

    model: Any

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
    ):
        """
        Initialize a Worker instance.

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
        formatted = f"Task: {task}\n\nCollaboration Chat:\n\n"
        formatted += "\n\n".join(messages)
        return formatted
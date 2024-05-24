"""Planner Agent for ReXia AI."""

from ..llms import RexiaAIChatOpenAI
from ..common import WorkflowStateSchema, TaskStatus
from ..base import BaseAgent


class PlanAgent(BaseAgent):
    """Planner Agent for ReXia AI."""

    def __init__(self, model: RexiaAIChatOpenAI, verbose: bool = False):
        super().__init__(model, verbose=verbose)
        self.name = "Planner"

    def action(self, agency_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Work on the current task."""
        if self.verbose:
            print(
                f"Planner working on task: {self.get_value_or_default(agency_state, 'task')}"
            )

        return self._plan_task(agency_state)

    def _plan_task(self, agency_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Handle the task when its status is PENDING."""
        agency_state["task_status"] = TaskStatus.WORKING
        prompt = self._create_plan_prompt(
            self.get_value_or_default(agency_state, "task")
        )
        planner_guidelines = self._invoke_model(prompt, "guidelines")
        agency_state["guidelines"] = self.get_value_or_default(
            planner_guidelines, "guidelines"
        )
        if self.verbose:
            print(
                f"Planner guidelines: {self.get_value_or_default(planner_guidelines, 'guidelines')}"
            )
        return agency_state

    def _create_plan_prompt(self, task: str) -> dict:
        """Create a prompt for a pending task."""
        return {
            "instructions": (
                "Read the task, explain to an AI your guidelines on how to complete it. "
                "All guidelines should be something that can be completed by an AI. "
                "Use the response format provided."
                "Always respond in valid JSON format."
            ),
            "task": task,
            "response format": {"guidelines": "Your guidelines here"},
            "examples": {
                "example response 1": {"guidelines": "Your guidelines here"},
                "example response 2": {
                    "guidelines": """To complete this task of answering the sum of 2+2, follow these simple guidelines: 
            1. Understand that the task requires you to perform a basic arithmetic operation.
            2. Recognize that the problem is asking for the result of adding two numbers together - in this case, 2 and 2.
            3. Apply your knowledge of addition or use an appropriate computational method to determine the sum.
            4. Return the answer as a single numerical value."""
                },
                "example response 3": {
                    "guidelines": """To complete this task, follow these guidelines:
            1. Read the task carefully and understand the requirements.
            2. Identify the key elements of the task, such as the input values and the operation to be performed.
            3. Perform the required calculation using the appropriate method.
            4. Check your answer for accuracy and correctness."""
                },
                "example response 4": {
                    "guidelines": """To complete this task, follow these guidelines:
            1. Read the task carefully and understand the requirements.
            2. Identify the key elements of the task, such as the input values and the operation to be performed.
            3. Perform the required calculation using the appropriate method.
            4. Check your answer for accuracy and correctness.
            5. Provide a clear and concise explanation of your solution."""
                },
                "example response 5": {
                    "guidelines": """To complete this task, follow these guidelines:
            1. Read the task carefully and understand the requirements.
            2. Identify the key elements of the task, such as the input values and the operation to be performed.
            3. Perform the required calculation using the appropriate method.
            4. Check your answer for accuracy and correctness.
            5. Provide a clear and concise explanation of your solution.
            6. Format your response according to the provided instructions."""
                },
            },
        }

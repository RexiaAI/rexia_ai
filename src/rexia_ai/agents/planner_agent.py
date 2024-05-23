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
            ),
            "task": task,
            "response format": {"guidelines": "Your guidelines here"},
            "example response": {"guidelines": "Your guidelines here"},
        }

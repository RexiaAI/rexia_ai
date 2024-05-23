"""Review Agent class for ReXia AI."""

from ..llms import RexiaAIChatOpenAI
from ..common import WorkflowStateSchema, TaskStatus
from ..base import BaseAgent


class ReviewAgent(BaseAgent):
    """Review Agent for ReXia AI."""

    def __init__(self, model: RexiaAIChatOpenAI, verbose: bool = False):
        super().__init__(model, verbose=verbose)
        self.name = "Reviewer"

    def action(self, agency_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Work on the current task."""
        if self.verbose:
            print(
                f"Reviewer working on task: {self.get_value_or_default(agency_state, 'task')}"
            )
        return self._handle_review(agency_state)

    def _handle_review(self, agency_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Handle the review of the task thus far."""
        prompt = self._create_review_prompt(agency_state)
        reviewer_approval = self._invoke_model(prompt, "status")

        if self.verbose:
            print(
                f"Reviewer approval: {self.get_value_or_default(reviewer_approval, 'status')}"
            )
            print(
                f"Reviewer feedback: {self.get_value_or_default(reviewer_approval, 'feedback')}"
            )

        if self.get_value_or_default(reviewer_approval, "status") == "COMPLETED":
            agency_state["task_status"] = TaskStatus.COMPLETED
        else:
            agency_state["task_status"] = TaskStatus.WORKING

        agency_state["feedback"] = self.get_value_or_default(
            reviewer_approval, "feedback"
        )

        return agency_state

    def _handle_completed_task(
        self, agency_state: WorkflowStateSchema
    ) -> WorkflowStateSchema:
        """Handle the task when it is marked as COMPLETED."""
        agency_state["task_status"] = TaskStatus.COMPLETED

        return agency_state

    def _create_review_prompt(self, agency_state: WorkflowStateSchema) -> dict:
        """Create a prompt for a working task."""
        return {
            "instructions": (
                "Read the messages and decide if they represent a completion "
                "of the task as per the guidelines. If it is complete then mark the task as "
                "complete by returning COMPLETED. If it is not complete, then return "
                "REJECTED, using the response format provided."
            ),
            "task": self.get_value_or_default(agency_state, "task"),
            "guidelines": self.get_value_or_default(agency_state, "guidelines"),
            "messages": self.get_value_or_default(agency_state, "messages"),
            "response format": {
                "status": "COMPLETED or REJECTED",
                "feedback": "Your feedback here",
            },
            "example response": {
                "status": "COMPLETED",
                "feedback": "The task has been completed. Well done!",
            },
            "example response 2": {
                "status": "REJECTED",
                "feedback": "The task has not been completed. Please try again.",
            },
        }

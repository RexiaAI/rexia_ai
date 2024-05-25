"""Review Agent class for ReXia AI."""

from ..llms import RexiaAIChatOpenAI
from ..common import WorkflowStateSchema, TaskStatus
from ..base import BaseAgent


class ReviewAgent(BaseAgent):
    """Review Agent for ReXia AI."""

    def __init__(self, model: RexiaAIChatOpenAI, verbose: bool = False):
        super().__init__(model, verbose=verbose)
        self.name = "Reviewer"

    def action(self, graph_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Work on the current task."""
        if self.verbose:
            print(
                f"Reviewer working on task: {graph_state['task']}"
            )
        return self._handle_review(graph_state)

    def _handle_review(self, graph_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Handle the review of the task thus far."""
        prompt = self._create_prompt(graph_state)
        reviewer_approval = self._invoke_model(prompt)

        if self.verbose:
            print(
                f"Reviewer approval: {reviewer_approval}"
            )

        if "COMPLETED" in reviewer_approval:
            graph_state["task_status"] = TaskStatus.COMPLETED
        else:
            graph_state["task_status"] = TaskStatus.WORKING

        graph_state["feedback"] = reviewer_approval
        return graph_state

    def _create_prompt(self, graph_state: WorkflowStateSchema) -> dict:
        """Create a prompt for a working task."""
        prompt = f"""role: You are a helpful reviewer, you always explain your reasoning step by step.\n\n
                task: {graph_state["task"]},\n\n
                guidelines: {graph_state["guidelines"]},\n\n
                instructions: {self.instructions}\n
                Read the messages and decide if they represent a completion 
                of the task as per the guidelines. If the task is complete, mark the task as
                'COMPLETED'. If it is not complete, then mark as 'REJECTED'.
                Respond with only a single instance of 'COMPLETED' or 'REJECTED'.
                If the messages do not follow the guidelines, provide feedback on how to improve and mark as 'REJECTED'.
                """

        return prompt

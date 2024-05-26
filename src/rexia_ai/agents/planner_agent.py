"""Planner Agent for ReXia AI."""

from ..llms import ReXiaAIChatOpenAI
from ..common import WorkflowStateSchema, TaskStatus
from ..base import BaseAgent


class PlanAgent(BaseAgent):
    """Planner Agent for ReXia AI."""

    def __init__(self, model: ReXiaAIChatOpenAI, verbose: bool = False):
        super().__init__(model, verbose=verbose)
        self.name = "Planner"

    def action(self, graph_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Work on the current task."""
        if self.verbose:
            print(
                f"Planner working on task: {graph_state['task']}"
            )

        return self._plan_task(graph_state)

    def _plan_task(self, graph_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Handle the task when its status is PENDING."""
        graph_state["task_status"] = TaskStatus.WORKING
        prompt = self._create_prompt(graph_state)
        planner_guidelines = self._invoke_model(prompt)
        graph_state["guidelines"] = planner_guidelines
        if self.verbose:
            print(
                f"Planner guidelines: {planner_guidelines}"
            )
        return graph_state

    def _create_prompt(self, graph_state: str) -> dict:
        """Create a prompt for a planning task."""
        prompt = f"""
            role: "You are a helpful planner who always generates detailed chain of 
            thought plans that complete the given task.\n\n
            task: {graph_state['task']}\n\n
            instructions:\n
            The plan should always result in a completed task.\n\n
            For example, if the task is to write a blog post, the guidelines should result in a finished blog post.
            If the task is to write a code snippet, the guidelines should result in a working code snippet.
            If the task is to write a report, the guidelines should result in a completed report.
            Each step in the plan be an action to be taken.
            All plans should be detailed and actionable.
            Do not add any extra information that is not part of the plan, or required to complete the task.
            Respond only with your plan and nothing else.\n\n
        """

        return prompt

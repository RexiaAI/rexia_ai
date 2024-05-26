"""Review Agent class for ReXia AI."""

from ..llms import ReXiaAIChatOpenAI
from ..common import WorkflowStateSchema, TaskStatus
from ..base import BaseAgent


class ObserverAgent(BaseAgent):
    """Review Agent for ReXia AI."""

    def __init__(self, model: ReXiaAIChatOpenAI, verbose: bool = False):
        super().__init__(model, verbose=verbose)
        self.name = "Oberserver"

    def action(self, graph_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Work on the current task."""
        if self.verbose:
            print(
                f"Observing task progess: {graph_state['task']}"
            )
        return self._handle_review(graph_state)

    def _handle_review(self, graph_state: WorkflowStateSchema) -> WorkflowStateSchema:
        """Handle the review of the task thus far."""
        prompt = self._create_prompt(graph_state)
        observation_approval = self._invoke_model(prompt)

        if self.verbose:
            print(
                f"Observer: {observation_approval}"
            )

        if "COMPLETED" in observation_approval:
            graph_state["task_status"] = TaskStatus.COMPLETED
        else:
            graph_state["task_status"] = TaskStatus.WORKING

        graph_state["messages"].append(observation_approval)
        return graph_state

    def _create_prompt(self, graph_state: WorkflowStateSchema) -> dict:
        """Create a prompt for a review task."""
        prompt = f"""role: You are a helpful observer, you observe the messages and decide if the task has been completed
                or if more steps need to be taken.\n\n
                task: {graph_state["task"]},\n\n
                messages: {graph_state["messages"]},\n\n
                respond in this format:
                    observation: the observation you have made about the task. 
                    COMPLETED if the task is complete, WORKING if more steps are needed.
                    Only respond with 'COMPLETED' or 'WORKING'.
                """

        return prompt

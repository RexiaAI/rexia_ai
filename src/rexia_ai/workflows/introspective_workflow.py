"""Reflectiove Workflow for ReXia AI."""

from textwrap import dedent
from langgraph.graph import END
from ..agents import PlanAgent, ReviewAgent, WorkAgent
from ..base import BaseWorkflow
from ..common import WorkflowState, WorkflowStateSchema, TaskStatus


class IntrospectiveWorkflow(BaseWorkflow):
    """Agency Class for ReXia AI, refactored for better design principles."""

    def __init__(
        self,
        planner: PlanAgent,
        reviewer: ReviewAgent,
        worker: WorkAgent,
        introspection: WorkAgent,
        task: str,
        verbose: bool = False,
        guidelines: str = "",
    ):
        super().__init__(task)
        self.agents = {
            "Planner": planner,
            "Reviewer": reviewer,
            "Worker": worker,
            "Introspection": introspection,
        }
        self.task = task
        self.verbose = verbose
        self.workflow = WorkflowState(self.task)
        self.guidelines = guidelines

    def launch(self) -> WorkflowStateSchema:
        """Launch the agency."""
        self._create_task_graph()
        runnable = self.workflow.compile()
        result = runnable.invoke(self.workflow.state)
        return result

    def _create_task_graph(self) -> None:
        """Create a task graph with dynamic agent addition."""
        for agent_name, agent in self.agents.items():
            self.workflow.add_node(agent_name, agent.action)

        self.workflow.set_entry_point("Planner")
        self.workflow.add_edge("Planner", "Worker")
        self.workflow.add_edge("Worker", "Introspection")
        self.workflow.add_edge("Introspection", "Reviewer")
        self.workflow.add_conditional_edges(
            "Reviewer", self._router, {"END": END, "CONTINUE": "Worker"}
        )

    def _router(self, state: WorkflowStateSchema) -> str:
        """Route the workflow based on task status."""
        task_status = state["task_status"]
        if self.verbose:
            self._log_decision(task_status, state)

        if task_status == TaskStatus.COMPLETED:
            return "END"
        elif task_status == TaskStatus.WORKING:
            return "CONTINUE"
        else:
            return "END"

    def _log_decision(
        self, task_status: TaskStatus, state: WorkflowStateSchema
    ) -> None:
        """Log the decision process based on task status."""
        status_messages = {
            TaskStatus.COMPLETED: "Task has been completed. Ending workflow.",
            TaskStatus.WORKING: "Task has not been completed. Continuing workflow.",
            "default": "Task status is neither working nor completed. Something has gone wrong. Ending workflow.",
        }
        message = status_messages.get(task_status, status_messages["default"])
        print(
            dedent(
                f"""
            {message}
            Task: {state['task']}
            Task status: {state['task_status']}
            Guidelines: {state['guidelines']}
            Messages: {state['messages']}
        """
            )
        )

"""Agency class for ReXia AI."""

import textwrap
from typing import List
from langgraph.graph import END
from ..agents import PlanningAgent, RexiaAIAgent, ReviewAgent
from ..common import AgencyState, AgencyStateSchema, TaskStatus


class Agency:
    """Agency Class for ReXia AI."""

    def __init__(
        self,
        planner: PlanningAgent,
        reviewer: ReviewAgent,
        agents: List[RexiaAIAgent],
        task: str,
        verbose: bool = False,
        guidelines: str = "",
    ):
        self.planner = planner
        self.reviewer = reviewer
        self.agents = agents
        self.task = task
        self.verbose = verbose
        self.workflow = AgencyState(self.task)
        self.guidelines = guidelines

    def launch(self) -> AgencyStateSchema:
        """Launch the agency."""
        self.create_task_graph()
        runnable = self.workflow.compile()
        result = runnable.invoke(self.workflow.state)
        return result

    def create_task_graph(self) -> None:
        """Create a task graph."""
        self._add_agent_nodes()
        self._add_planner_node()
        self._add_reviewer_node()
        self.workflow.set_entry_point("Planner")

    def _add_planner_node(self) -> None:
        """Add the manager node to the workflow."""
        self.workflow.add_node("Planner", self.planner.work)
        self.workflow.add_edge("Planner", self.agents[0].name)

    def _add_reviewer_node(self) -> None:
        """Add the planner node to the workflow."""
        self.workflow.add_node("Reviewer", self.reviewer.work)
        self.workflow.add_edge(self.agents[-1].name, "Reviewer")
        self.workflow.add_conditional_edges(
            "Reviewer", self.router, {"END": END, "CONTINUE": self.agents[0].name}
        )

    def _add_agent_nodes(self) -> None:
        """Add agent nodes to the workflow."""
        for i, agent in enumerate(self.agents):
            self.workflow.add_node(agent.name, agent.work)
            if i != len(self.agents) - 1:
                next_agent = self.agents[i + 1]
                self.workflow.add_edge(agent.name, next_agent.name)

    def router(self, state: AgencyStateSchema) -> str:
        """Decide whether to end the graph or keep working."""
        if self.verbose:
            print(f"Deciding if task is complete: {state['task']}")
        if state["task_status"] == TaskStatus.COMPLETED:
            if self.verbose:
                print(
                    textwrap.dedent(
                        f"""
                      Task has been completed. Ending workflow.
                      Task: {state['task']}
                      Task status: {state['task_status']}
                      Guidelines: {state['guidelines']}
                      Messages: {state['messages']}
                      """
                    )
                )
            return "END"
        elif state["task_status"] == TaskStatus.WORKING:
            if self.verbose:
                print(
                    textwrap.dedent(
                        f"""
                      Task has not been completed. Continuing workflow.
                      Task: {state['task']}
                      Task status: {state['task_status']}
                      Guidelines: {state['guidelines']}
                      Messages: {state['messages']}
                      """
                    )
                )
            return "CONTINUE"
        else:
            if self.verbose:
                print(
                    textwrap.dedent(
                        f"""
                    Task status is neither working or completed. Something has gone wrong. Ending worflow.
                    Task: {state['task']}
                    Task status: {state['task_status']}
                    Guidelines: {state['guidelines']}
                    Messages: {state['messages']}
                    """
                    )
                )

            return "END"

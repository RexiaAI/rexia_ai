"""Manager Agent for ReXia AI."""

from typing import List
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from ..common import (
    AgencyStateSchema,
    TaskStatus,
)


class ManagerAgent():
    """Manager Agent for ReXia AI."""

    model: ChatOpenAI
    tools: List[Tool]

    @property
    def __name__(self):
        return self.name

    def __init__(self, model: ChatOpenAI, verbose: bool = False):
        self.name = "Manager"
        self.model = model
        self.verbose = verbose

    def __eq__(self, other):
        if isinstance(other, ManagerAgent):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def work(self, agency_state: AgencyStateSchema) -> AgencyStateSchema:
        """Work on the current task."""
        graph_state = agency_state
        
        if self.verbose:
            print(f"Manager working on task: {graph_state['task']}")

        if graph_state["task_status"] == TaskStatus.PENDING:
            graph_state["task_status"] = TaskStatus.WORKING
            return graph_state
        elif graph_state["task_status"] == TaskStatus.WORKING:
            manager_feedback = self.model.invoke(
                f"""
                Your Instructions: Read the messages and decide if the task is complete. If it is complete
                then mark the task as complete by returning COMPLETED. If it is not complete, then return
                REJECTED. Only responsd with COMPLETED or REJECTED.
                Your Task: {graph_state['task']}
                Messages: {graph_state['messages']}
                """
            )
            
            if self.verbose:
                print(f"Manager feedback: {manager_feedback.content}")

            if "COMPLETED" in manager_feedback.content:
                graph_state["task_status"] = TaskStatus.COMPLETED
                return graph_state
            else:
                graph_state["task_status"] = TaskStatus.REJECTED
                graph_state["messages"].append(manager_feedback.content)
                return graph_state

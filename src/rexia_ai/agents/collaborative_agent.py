"""Collaborative Agent for ReXia AI."""

from typing import List, Optional
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from ..common import AgencyStateSchema


class CollaborativeAgent:
    """Collaborative Agent for ReXia AI."""

    model: ChatOpenAI
    tools: Optional[List[Tool]]

    @property
    def __name__(self):
        return self.name

    def __init__(self, agent_name: str, model: ChatOpenAI, instructions: str = "", verbose: bool = False):
        self.name = agent_name
        self.model = model
        self.instructions = instructions
        self.verbose = verbose

    def __eq__(self, other):
        if isinstance(other, CollaborativeAgent):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def work(self, agency_state: AgencyStateSchema) -> AgencyStateSchema:
        """Work on the current task."""
        graph_state = agency_state
        
        if self.verbose:
            print(f"{self.name} working on task: {graph_state['task']}")
            
        response = self.model.invoke(
            f"""
            Your Instructions: {self.instructions}
            Your Task: {graph_state['task']}
            Messages: {graph_state['messages']}
            """
        )
        
        if self.verbose:
            print(f"{self.name} response: {response.content}")

        graph_state["messages"].append(response.content)
        return graph_state
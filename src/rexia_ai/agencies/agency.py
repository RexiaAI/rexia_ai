"""Agency class for ReXia AI."""

from typing import List
from langgraph.graph import END
from ..agents import (
    ManagerAgent,
    CollaborativeAgent
)
from ..common import (
    AgencyState,
    TaskStatus
)


class Agency:
    """Agency Class."""
    def __init__(self, manager: ManagerAgent, agents: List[CollaborativeAgent], task: str, verbose: bool = False):
        self.manager = manager
        self.agents = agents
        self.task = task
        self.verbose = verbose

    def launch(self):
        """Launch the agency."""
        graph = self.create_task_graph()
        runnable = graph.compile()
        
        result = runnable.invoke(graph.state)
        
        return result
    
    def create_task_graph(self) -> AgencyState:
        """Create a task graph."""
        workflow = AgencyState(self.task)

        workflow.add_node("Manager", self.manager.work)
                
        for i, agent in enumerate(self.agents):
            workflow.add_node(agent.name, agent.work)
            
            if i == len(self.agents) - 1:
                workflow.add_edge(agent.name, "Manager")
            else:
                next_agent = self.agents[i + 1]
                workflow.add_edge(agent.name, next_agent.name)
        
        workflow.add_conditional_edges('Manager',
                                   (lambda task_status: "accept" if task_status == TaskStatus.COMPLETED else "revise"),
                                   {"accept": END, "revise": self.agents[0].name})
        
        workflow.add_edge("Manager", self.agents[0].name)
        workflow.set_entry_point("Manager")

        return workflow
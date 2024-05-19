"""Manager Agent for ReXia AI."""

from llama_index.core.agent import StructuredPlannerAgent
from llama_index.core.agent import ReActAgentWorker
from llama_index.core.tools import BaseTool
from ..tasks import AgencyTask


class ManagerAgent(StructuredPlannerAgent):
    """Manager Agent for ReXia AI."""

    def __init__(self, agent_worker: ReActAgentWorker, tools: list[BaseTool], verbose: bool = True):
        """Initialize the Manager Agent."""
        super().__init__(agent_worker=agent_worker, tools=tools, verbose=verbose)

    def plan(self, tasks: list[AgencyTask]):
        """Create a plan for the tasks."""
        tasks_str = "\n".join(str(t) for t in tasks)
        tasks_prompt = f"""tasks
            Create a plan for the following tasks, taking into account the dependencies between them and their priority.
            1 is high priority, 2 is medium priority, 3 is low priority.
            
            Tasks:
            {tasks_str}
        """
        return super().chat(tasks_prompt)

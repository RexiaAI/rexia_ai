# custom_function_calling_agent_worker.py
from llama_index.core.agent import CustomSimpleAgentWorker, Task, AgentChatResponse
from llama_index.core.tools.types import BaseTool
from typing import List, Any

class RexiaAIFunctionCallingAgentWorker(CustomSimpleAgentWorker):
    """Custom function calling agent worker for ReXia AI."""

    def __init__(self, tools: List[BaseTool], llm: Any, verbose: bool = True):
        """Initialize the custom function calling agent worker."""
        super().__init__(tools=tools, llm=llm, verbose=verbose)

    def run_step(self, task: Task) -> AgentChatResponse:
        """Run a step for the given task."""
        return self.run_step(task)

    def finalize_response(self, task_id: str) -> AgentChatResponse:
        """Finalize the response for the given task ID."""
        return self.finalize_response(task_id)

    def list_tasks(self) -> List[Task]:
        """List all tasks."""
        return self.list_tasks()

    def get_completed_steps(self, task_id: str) -> List[AgentChatResponse]:
        """Get all completed steps for the given task ID."""
        return self.get_completed_steps(task_id)
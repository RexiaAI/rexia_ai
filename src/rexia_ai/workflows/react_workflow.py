"""ReAct Workflow for ReXia AI."""
from textwrap import dedent
from langgraph.graph import END
from ..agents import ObserverAgent, ThoughtAgent, ActionAgent
from ..base import BaseWorkflow
from ..common import WorkflowState, WorkflowStateSchema, TaskStatus

class ReActWorkflow(BaseWorkflow):
    """ReAct Workflow for ReXia AI."""
    def __init__(self, thought: ThoughtAgent, action: ActionAgent, observation: ObserverAgent, task: str, verbose: bool = False):
        super().__init__(task, verbose)
        self.thought = thought
        self.action = action
        self.observation = observation
        self.workflow = WorkflowState(self.task)
    
    def _create_task_graph(self) -> None:
        """Create a task graph with dynamic agent addition."""
        self.workflow.add_node("Thought", self.thought.action)
        self.workflow.add_node("Action", self.action.action)
        self.workflow.add_node("Observe", self.observation.action)

        self.workflow.set_entry_point("Thought")
        self.workflow.add_edge("Thought", "Action")
        self.workflow.add_edge("Action", "Observe")
        self.workflow.add_conditional_edges(
            "Observe", self._router, {"END": END, "CONTINUE": "Thought"}
        )

        
    def launch(self) -> WorkflowStateSchema:
        """Launch the agency."""
        self._create_task_graph()
        runnable = self.workflow.compile()
        result = runnable.invoke(self.workflow.state)
        return result
    
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
            Messages: {state['messages']}
        """
            )
        )
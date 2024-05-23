"""Base Workflow for ReXia AI."""

from ..common import WorkflowState, WorkflowStateSchema


class BaseWorkflow:
    """BaseWorkFlow Class for ReXia AI, refactored for better design principles."""

    def __init__(
        self,
        task: str,
        verbose: bool = False,
    ):
        self.task = task
        self.verbose = verbose
        self.workflow = WorkflowState(self.task)

    def launch(self) -> WorkflowStateSchema:
        """Launch the workflow."""
        self._create_task_graph()
        runnable = self.workflow.compile()
        result = runnable.invoke(self.workflow.state)
        return result

    def _create_task_graph(self) -> None:
        pass

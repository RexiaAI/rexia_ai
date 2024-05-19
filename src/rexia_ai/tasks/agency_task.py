"""Agency Task class for ReXia AI."""

from llama_index.core.agent import AgentRunner
from ..common import (
    TaskPriority,
    TaskStatus
)

class AgencyTask():
    """
    AgencyTask is a subclass of BaseTask that provides additional attributes and methods
    specific to tasks that are managed by agencies in ReXia AI.
    """

    def __init__(
        self,
        task_id: str,
        task_name: str,
        task_description: str,
        task_type: int,
        task_priority: int = TaskPriority.MEDIUM,
        task_status: str = TaskStatus.PENDING,
        task_context: str = "",
        agent: AgentRunner = None
    ):
        """
        Initialize the AgencyTask object.

        Args:
            task_id (str): The unique identifier for the task.
            task_name (str): The name of the task.
            task_description (str): The description of the task.
            task_type (int): The type of the task.
            task_priority (int, optional): The priority of the task. Defaults to Priority.MEDIUM.
            task_status (str, optional): The status of the task. Defaults to Status.PENDING.
            task_context (str, optional): The context of the task. Defaults to "".
            agent (AgentRunner): The agent assigned to the task. Defaults to "".
            tools (str, optional): The tools avalable to be used to perform the task. Defaults to "".
        """
        self.task_id=task_id,
        self.task_name=task_name,
        self.task_description=task_description,
        self.task_type=task_type,
        self.task_priority=task_priority,
        self.task_status=task_status,
        self.task_context=task_context,
        self.agent = agent

    def __str__(self):
        return f"AgencyTask: {self.task_name} Description:({self.task_description}) Type:({self.task_type}) Priority:({self.task_priority}) Status:({self.task_status}) Context:({self.task_context})"
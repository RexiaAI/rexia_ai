"""Base Task Class for ReXia AI."""

from rexia_ai.tasks import Status, Priority


class BaseTask:
    """
    BaseTask is a base class for tasks in ReXia AI. It provides the basic attributes
    and methods that all tasks should have, such as task_id, task_name, task_description,
    task_type, task_priority, task_status, and task_context.
    """

    def __init__(
        self,
        task_id: str,
        task_name: str,
        task_description: str,
        task_type: int,
        task_priority: int = Priority.MEDIUM,
        task_status: str = Status.PENDING,
        task_context: str = "",
    ):
        """
        Initialize the BaseTask object.

        Args:
            task_id (str): The unique identifier for the task.
            task_name (str): The name of the task.
            task_description (str): The description of the task.
            task_type (int): The type of the task.
            task_priority (int, optional): The priority of the task. Defaults to Priority.MEDIUM.
            task_status (str, optional): The status of the task. Defaults to Status.PENDING.
            task_context (str, optional): The context of the task. Defaults to "".
        """
        self.task_id = task_id
        self.task_name = task_name
        self.task_description = task_description
        self.task_type = task_type
        self.task_priority = task_priority
        self.task_status = task_status
        self.task_context = task_context

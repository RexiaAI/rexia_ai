# base_task.py
from rexia_ai.tasks import Status, Priority, TaskType

class BaseTask():
    def __init__(self, task_id: str, task_name: str, task_description: str, task_type: int, task_priority: int = Priority.MEDIUM, task_status: str = Status.PENDING, task_context: str = ""):
        """Initialize the task."""
        self.task_id = task_id
        self.task_name = task_name
        self.task_description = task_description
        self.task_type = task_type
        self.task_priority = task_priority
        self.task_status = task_status
        self.task_context = task_context
        
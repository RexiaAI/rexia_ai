# base_task.py

class BaseTask():
    def __init__(self, task_id: str, task_name: str, task_description: str, task_type: str, task_priority: int, task_status: str, task_data: dict):
        """Initialize the task."""
        self.task_id = task_id
        self.task_name = task_name
        self.task_description = task_description
        self.task_type = task_type
        self.task_priority = task_priority
        self.task_status = task_status
        self.task_data = task_data
        
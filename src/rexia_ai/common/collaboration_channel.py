"""Collaboration Channel class."""

from ..common import TaskStatus

class CollaborationChannel:
    """A channel for communication within the team."""
    def __init__(self, task: str):
        self.task = task
        self.messages = []
        self.status = TaskStatus.PENDING

    def put(self, item):
        """Put an item into the Channel."""
        self.messages.append(item)

    def get_messages(self):
        """Get the current messages in the Channel."""
        return list(self.messages)

    def get_status(self):
        """Get the current status of the Channel."""
        return self.status

    def get_task(self):
        """Get the current task of the Channel."""
        return self.task

    def update_status(self, new_status):
        """Update the status of the Channel."""
        self.status = new_status
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
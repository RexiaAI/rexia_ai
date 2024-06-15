"""Collaboration Channel class."""

from typing import Any
from ..common import TaskStatus


class CollaborationChannel:
    """
    A channel for communication within the team.

    Attributes:
        task: The task that the channel is associated with.
        messages: A list of messages in the channel.
        status: The status of the task.
    """
    def __init__(self, task: str):
        """
        Initialize a CollaborationChannel instance.

        Args:
            task: The task that the channel is associated with.
        """
        self.task = task
        self.messages = []
        self.status = TaskStatus.PENDING

    def put(self, item: Any):
        """
        Put an item into the channel.

        Args:
            item: The item to put into the channel.
        """
        self.messages.append(item)
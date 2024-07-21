"""Collaboration Channel class for ReXia.AI."""

import logging
from typing import Any, List
from ..common import TaskStatus

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class CollaborationChannel:
    """
    A channel for communication within the team.

    Attributes:
        task: The task that the channel is associated with.
        messages: A list of messages in the channel.
        status: The status of the task.
    """
    task: str
    messages: List[Any]
    status: TaskStatus
    
    def __init__(self, task: str):
        """
        Initialize a CollaborationChannel instance.

        Args:
            task: The task that the channel is associated with.
        """
        self.task = task
        self.messages: List[Any] = []
        self.status = TaskStatus.PENDING

    def put(self, item: Any):
        """
        Put an item into the channel.

        Args:
            item: The item to put into the channel.
        """
        if item:
            self.messages.append(item)
        else:
            logger.error("Error: Cannot add empty item to the channel.")

    def clear_messages(self) -> None:
        """
        Clear all messages from the channel.

        Returns:
            None
        """
        try:
            self.messages.clear()
        except Exception as e:
            logger.error(f"Error occurred while clearing messages: {str(e)}")
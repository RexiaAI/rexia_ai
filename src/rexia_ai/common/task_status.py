"""This module contains the TaskStatus enum."""

from enum import Enum


class TaskStatus(Enum):
    """
    Enum representing the status of a task.

    Attributes:
        PENDING: The task is pending.
        WORKING: The task is being worked on.
        COMPLETED: The task has been completed.
    """
    PENDING = 1
    WORKING = 2
    COMPLETED = 3
"""This module contains the TaskStatus enum."""

from enum import Enum


class TaskStatus(Enum):
    """
    Represents the status of a task.

    Attributes:
        PENDING: The task is pending.
        WORKING: The task is being worked on by the agency.
        COMPLETED: The task has been accepted by the reviewer.
    """

    PENDING = 1
    WORKING = 2
    COMPLETED = 3

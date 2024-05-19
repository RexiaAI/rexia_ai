"""This module contains the TaskStatus enum."""

from enum import Enum


class TaskStatus(Enum):
    """
    Represents the status of a task.

    Attributes:
        PENDING: The task is pending.
        IN_PROGRESS: The task is in progress.
        COMPLETED: The task is completed.
        FAILED: The task has failed.
    """

    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    FAILED = 4

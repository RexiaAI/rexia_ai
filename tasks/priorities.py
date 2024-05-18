"""This module contains the Priority enumeration."""

from enum import Enum


class Priority(Enum):
    """
    An enumeration representing different priority levels.

    Attributes:
        HIGH (int): Represents a high priority level.
        MEDIUM (int): Represents a medium priority level.
        LOW (int): Represents a low priority level.
    """

    HIGH = 1
    MEDIUM = 2
    LOW = 3

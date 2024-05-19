"""Agency status module for ReXia AI."""

from enum import Enum


class AgencyStatus(Enum):
    """
    Represents the status of an agency.

    Attributes:
        IDLE (int): Represents the idle status.
        WORKING (int): Represents the working status.
        COMPLETED (int): Represents the completed status.
        FAILED (int): Represents the failed status.
    """

    IDLE = 1
    WORKING = 2
    COMPLETED = 3
    FAILED = 4

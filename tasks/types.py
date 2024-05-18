# types.py
from enum import Enum

class TaskType(Enum):
    """
    An enumeration representing different types of tasks.

    Attributes:
        REFLEX_TASK (int): Represents a reflex task.
        MODEL_REFLEX_TASK (int): Represents a model-reflex task.
        GOAL_ORIENTED_TASK (int): Represents a goal-oriented task.
        UTILITY_DRIVEN_TASK (int): Represents a utility-driven task.
        LEARNING_TASK (int): Represents a learning task.
    """
    REFLEX_TASK = 1
    MODEL_REFLEX_TASK = 2
    GOAL_ORIENTED_TASK = 3
    UTILITY_DRIVEN_TASK = 4
    LEARNING_TASK = 5
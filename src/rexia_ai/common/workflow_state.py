"""This module contains the state of the tasks."""

from typing import (
    TypedDict,
    Annotated,
    List,
)
from dataclasses import dataclass
from langgraph.graph import StateGraph
from . import TaskStatus


def add_message(left: list, right: list):
    """Add-don't-overwrite."""
    return left + right


@dataclass
class WorkflowStateSchema(TypedDict):
    """The schema for the state of the tasks."""

    task: Annotated[str, "The task to be completed"]
    task_status: Annotated[TaskStatus, "The status of the task"]
    messages: Annotated[List[str], add_message]
    guidelines: Annotated[str, "guidelines on completing the task"]
    feedback: Annotated[str, "Feedback from the reviewer"]


class WorkflowState(StateGraph):
    """The state of all tasks to be performed."""

    def __init__(self, task: str):
        """
        Initialize the state of the tasks.
        """
        state_schema = WorkflowStateSchema(
            task=task,
            task_status=TaskStatus.PENDING,
            messages=[],
            guidelines="",
            feedback="",
        )
        super().__init__(state_schema=state_schema)

        self.state = state_schema

    def has_node(self, node) -> bool:
        """Check if a node exists in the graph."""
        return node in self.nodes

"""PlanWorker class in ReXia.AI."""

from typing import Any
from ...base import BaseWorker

PREDEFINED_PROMPT = """
As a planning agent for ReXia.AI, your role is to create a detailed plan to guide task completion.

You're an advanced AI capable of various tasks. Before starting, devise a plan breaking down the problem into executable steps.
This plan, structured as a numbered list of instructions, should be tailored for your execution, not human comprehension.

Each step should involve specific operations or information retrieval that you can perform directly. 
Avoid explanations or justifications, as the plan is for your execution.

Keep the plan concise and self-contained, not relying on external resources or human intervention.

After generating the plan, execute each step sequentially. If a step requires further planning, generate a sub-plan.

The goal is to create a clear roadmap for your execution, without human interpretation or guidance.

Apply specific formatting requests only within the answer.
"""


class PlanWorker(BaseWorker):
    """
    A specialised planning worker for a ReXia.AI agent.

    This worker is responsible for thinking through the task and creating a plan to complete it.

    Attributes:
        model: The model used by the worker.
        verbose: A flag used for enabling verbose mode.
    """

    model: Any
    verbose: bool

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
    ):
        """
        Initialize a PlanWorker instance.

        Args:
            model: The model used by the worker.
            verbose: A flag used for enabling verbose mode. Defaults to False.
        """
        super().__init__(model, verbose=verbose)

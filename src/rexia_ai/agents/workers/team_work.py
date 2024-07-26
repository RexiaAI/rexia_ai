"""TeamWorker class for ReXia.AI's collaborative problem-solving simulation."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
You are an AI tasked with simulating a team of five distinct personalities working together to solve a problem. 
The team will plan, discuss, and execute a solution in a single, cohesive process.

## The Team

1. **Dr. Amelia Thornton (The Analytical Thinker)**
   - Data scientist, precise and logical
2. **Jack "Maverick" Rodriguez (The Creative Innovator)**
   - Entrepreneur and artist, thinks outside the box
3. **Dr. Zara Patel (The Empathetic Mediator)**
   - Psychologist, focuses on team dynamics
4. **Commander Sarah Chen (The Strategic Leader)**
   - Ex-military strategist, action-oriented
5. **Professor Kwame Osei (The Philosophical Visionary)**
   - Philosophy professor and futurist, big-picture thinker

## Task

1. Analyze the given problem.
2. Have each team member propose a solution approach.
3. Simulate a team discussion to evaluate and refine these proposals.
4. Develop a consensus plan.
5. Execute the plan, showing how the team works through each step.
6. Address any challenges that arise during execution.
7. Produce a final, comprehensive solution to the problem.

## Output Structure

Use the following JSON structure for your output:

```json
{
    "question": "The original problem statement",
    "plan": ["Step 1 of the agreed and executed plan", "Step 2", ...],
    "answer": "The comprehensive final solution to the problem",
    "confidence_score": "Team's confidence in the solution (0-100)",
    "chain_of_reasoning": [
        "Dr. Thornton's initial proposal",
        "Jack Rodriguez's creative approach",
        "Dr. Patel's team-focused suggestion",
        "Commander Chen's strategic plan",
        "Professor Osei's philosophical perspective",
        "Key points from team discussion",
        "Consensus plan formation",
        "Execution of step 1 with team insights",
        "Execution of step 2 with team insights",
        ...,
        "Challenge encountered and how it was addressed",
        "Final solution refinement and implementation"
    ],
    "tool_calls": []
}
"""


class TeamWorker(BaseWorker):
    """
    A specialized worker for ReXia.AI's agent system that simulates collaborative problem-solving.

    This worker is responsible for simulating a diverse team of five personalities
    working together to analyze, plan, and execute solutions to complex problems.
    It generates a comprehensive simulation of team dynamics, problem-solving processes,
    and final solution implementation.

    Attributes:
        model (Any): The language model used for generating the team simulation.
        verbose (bool): Flag for enabling verbose output mode.

    Inherits from:
        BaseWorker: Provides core functionality for AI workers in the ReXia.AI system.
    """

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
    ):
        """
        Initialize a TeamWorker instance.

        Args:
            model (Any): The language model to be used for generating the team simulation.
            verbose (bool, optional): Enable verbose output for debugging. Defaults to False.
        """
        super().__init__(model, verbose=verbose)

    def create_prompt(self, task: str, messages: List[str]) -> str:
        """
        Create a prompt for the model to generate a team problem-solving simulation.

        This method combines the predefined team simulation prompt with task-specific information,
        relevant messages, and any pertinent memory to create a comprehensive prompt
        for the model to generate a detailed team problem-solving scenario.

        Args:
            task (str): The problem or challenge to be addressed by the simulated team.
            messages (List[str]): A list of relevant messages or context for the task.

        Returns:
            str: A formatted prompt string for the model to generate a team problem-solving simulation.
        """
        prompt = super().create_prompt(PREDEFINED_PROMPT, task, messages)
        return prompt

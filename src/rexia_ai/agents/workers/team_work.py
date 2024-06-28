"""TeamWorker class for ReXia.AI."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
# AI Team Problem-Solving Simulation

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

## Guidelines

- Maintain each character's unique voice, expertise, and perspective throughout the entire process.
- Show how the team's diverse skills contribute to both planning and execution.
- Demonstrate realistic team dynamics, including potential disagreements and their resolutions.
- Ensure the final solution comprehensively addresses the original problem.
- The "chain_of_reasoning" should clearly show the progression from initial ideas through planning, execution, and final solution.
- Adjust the confidence score based on the team's overall satisfaction with the process and outcome.

Remember to keep the interaction realistic, showcasing both the benefits and challenges 
of a diverse team working together on a complex problem from start to finish.
"""


class TeamWorker(BaseWorker):
    """
    A worker for a ReXia AI agent.

    This worker is responsible for completing the task based on the
    collaboration chat and the task context.
    """

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
        max_attempts: int = 3,
    ):
        """
        Initialize a Worker instance.

        Args:
            model: The model used by the worker.
            verbose: A flag used for enabling verbose mode. Defaults to False.
        """
        super().__init__(model, verbose=verbose, max_attempts=max_attempts)

    def create_prompt(self, task: str, messages: List[str], memory: Any) -> str:
        """Create a prompt for the model."""
        prompt = super().create_prompt(PREDEFINED_PROMPT, task, messages, memory)

        return prompt

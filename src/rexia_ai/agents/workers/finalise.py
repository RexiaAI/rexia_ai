"""FinaliseWorker class for ReXia.AI's reflection and answer refinement process."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
As a reflection agent for ReXia.AI, your role is to provide a revised, comprehensive answer based on
the collaboration chat. Follow these guidelines:

### Key Responsibilities
1. **Analyze Chat Content**:
   - Pay close attention to the plan and tool messages in the chat.
   - Adhere strictly to the given plan and utilize information from tool messages.

2. **Provide Revised Answer**:
   - Follow the provided output structure precisely.
   - Ensure the answer is a direct completion of the task, not a description of actions or a statement of completion.

3. **Explain Reasoning**:
   - Include a detailed chain of reasoning in your answer.
   - Clearly explain your thought process and decision-making.

4. **Handle Information Gaps**:
   - If the chat lacks sufficient information, state the limitations explicitly.
   - Provide the best possible answer based on available information.

5. **Reconcile Conflicting Information**:
   - Address and resolve any conflicting information in the chat.
   - If conflicts cannot be resolved, acknowledge them and provide your best interpretation.

6. **Maintain Clarity**:
   - Avoid abbreviations or shorthand unless explicitly explained in the answer.
   - Do not give instructions to improve the answer; instead, provide the improved answer directly.

7. **Ensure Relevance and Completeness**:
   - Verify that your answer directly addresses the task.
   - Provide a complete and detailed response.

### Output Guidelines
1. **Structure**:
   - Follow the provided output structure meticulously.
   - Organize your response logically and coherently.

2. **Formatting**:
   - Apply specific formatting requests only within the answer section.

3. **Content**:
   - Provide a direct completion of the task.
   - Include all necessary details, explanations, and supporting information.
"""


class FinaliseWorker(BaseWorker):
    """
    A specialized reflection worker for ReXia.AI's agent system.

    This worker is responsible for analyzing the collaboration chat,
    reflecting on the information provided, and generating an improved,
    comprehensive answer to the given task. It focuses on integrating
    information from various sources, following predefined plans, and
    providing detailed, coherent responses.

    Attributes:
        model (Any): The language model used for generating responses.
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
        Initialize a FinaliseWorker instance.

        Args:
            model (Any): The language model to be used for generating responses.
            verbose (bool, optional): Enable verbose output for debugging. Defaults to False.
        """
        super().__init__(model, verbose=verbose)

    def create_prompt(self, task: str, messages: List[str]) -> str:
        """
        Create a prompt for the model to generate a refined answer.

        This method combines the predefined prompt with task-specific information,
        collaboration messages, and any relevant memory to create a comprehensive
        prompt for the model.

        Args:
            task (str): The original task or question to be answered.
            messages (List[str]): A list of messages from the collaboration chat.

        Returns:
            str: A formatted prompt string for the model to generate a refined answer.

        Note:
            The returned prompt includes instructions for the model to follow the
            collaboration plan, integrate tool messages, and provide a detailed,
            well-reasoned response.
        """
        prompt = super().create_prompt(PREDEFINED_PROMPT, task, messages)
        return prompt
"""CodeWorker class for ReXia.AI's code generation system."""

from typing import Any, List
from ...base import BaseWorker

PREDEFINED_PROMPT = """
As a software developer for ReXia.AI, your role is to write high-quality, clean, and efficient code based
on the provided task context. Follow these guidelines to ensure your code meets the highest standards:

### Task Execution
1. **Analyze Requirements**:
   - Thoroughly understand the task requirements and constraints.
   - Pay attention to any specific instructions or details provided in the task description.

2. **Plan Your Approach**:
   - Outline a clear plan before you start coding.
   - Break down the task into smaller, manageable subtasks if necessary.

### Code Quality
1. **Readability and Maintainability**:
   - Write clean, readable, and maintainable code.
   - Follow language-specific conventions and style guides.
   - Use meaningful and descriptive variable and function names.
   - Keep functions small and focused on a single task.
   - Avoid code duplication; use DRY (Don't Repeat Yourself) principles.

2. **Documentation**:
   - Include clear, concise comments where necessary.
   - Write descriptive docstrings for functions and classes.
   - Explain complex algorithms or non-obvious code sections.

3. **Error Handling**:
   - Implement proper error handling and exception management.
   - Use try-except blocks judiciously.
   - Provide informative error messages.

4. **Performance**:
   - Write efficient code, but not at the expense of readability.
   - Consider time and space complexity in your algorithms.
   - Optimize only when necessary and after profiling.

5. **Testing**:
   - Write unit tests for your code.
   - Ensure edge cases are covered in your tests.
   - Aim for high test coverage.

6. **Security**:
   - Be aware of common security vulnerabilities.
   - Sanitize inputs and validate data.
   - Follow secure coding practices.

7. **Version Control**:
   - Write clear, descriptive commit messages.
   - Make small, focused commits.

8. **Code Review**:
   - Be open to feedback and prepared to explain your code choices.

### Task Completion
1. **Implementation**:
   - Implement the solution step by step according to your plan.
   - Test your code rigorously to ensure it works as expected.
   - Refactor for improved quality if needed.

2. **Final Output**:
   - Provide complete, runnable code solutions unless specified otherwise.
   - Include necessary imports, class definitions, and example usage where appropriate.
   - Ensure your code is well-documented and tested.

### Example of a Good Task Description
- **Task**: Implement a Snake game in Python.
- **Requirements**:
  - Create a `Snake` class with the following attributes and methods:
    - `position` (list of coordinates)
    - `direction` (UP, DOWN, LEFT, RIGHT)
    - `length` (initial value: 3)
    - `move()`: Update snake's position based on current direction.
    - `grow()`: Increase snake's length when it eats food.
    - `check_collision()`: Detect collisions with self or game boundaries.
  - The game board should be a 20x20 grid.
- **Output**: Provide complete Python code with proper documentation and unit tests.

### Example of a Poor Task Description
- **Task**: Implement the Snake class as discussed earlier, with the previously mentioned attributes and methods.

### Additional Guidelines
- If you need clarification on any aspect of the task, ask specific, targeted questions.
- Apply your expertise to deliver code that not only works but exemplifies best practices in software development.

Ensure your response is clear, concise, and informative. Avoid unnecessary complexity. 
Use messages from tools in your answer. Ensure your answer matches the task and is complete and detailed.
"""


class CodeWorker(BaseWorker):
    """
    A specialised code worker for ReXia.AI's agent system, designed for generating code.

    Attributes:
        model (Any): The language model used for processing tasks and generating responses.
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
        Initialize a CodeWorker instance.

        Args:
            model (Any): The language model to be used for task processing and response generation.
            verbose (bool, optional): Enable verbose output for debugging. Defaults to False.
        """
        super().__init__(model, verbose=verbose)

    def create_prompt(self, task: str, messages: List[str]) -> str:
        """
        Create a comprehensive prompt for the model based on the task, context, and memory.

        This method combines the predefined prompt with task-specific information,
        relevant messages from the collaboration chat, and any pertinent memory
        to create a detailed prompt for the model to generate an appropriate response.

        Args:
            task (str): The specific task or question to be addressed.
            messages (List[str]): A list of relevant messages from the collaboration chat.

        Returns:
            str: A formatted prompt string for the model to generate a task response.
        """
        prompt = super().create_prompt(PREDEFINED_PROMPT, task, messages)
        return prompt
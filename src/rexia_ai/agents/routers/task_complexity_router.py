"""TaskComplexityRouter class for ReXia.AI

This module provides a routing mechanism to direct tasks to appropriate language models
based on their complexity. It uses a separate router model to assess task complexity
and then chooses between a base model and a complex model for task execution.
"""

import json
from typing import Dict, Any
from ...llms import RexiaAIOpenAI

PREDEFINED_PROMPT = """
You are a task complexity analyzer. Your job is to assess the given task and assign it a complexity
score between 1 and 100. Consider the following factors:

1. Input length: How long is the input text?
2. Expected output length: How long should the response be?
3. Task type: Is it simple classification, generation, summarization, etc.?
4. Domain specificity: Is it a general topic or a specialized field?
5. Reasoning depth: How much logical reasoning is required?
6. Contextual understanding: How much context or background knowledge is needed?
7. Creativity level: Does it require creative or original thinking?
8. Factual knowledge: How much factual information is necessary?

After analyzing the task, provide your response in the following JSON format:

{
  "complexity_score": <integer between 1 and 100>,
  "explanation": "<brief explanation of the scoring>",
  "factors": {
    "input_length": <integer between 1 and 100>,
    "output_length": <integer between 1 and 100>,
    "task_type": "<string describing the task type>",
    "domain_specificity": <integer between 1 and 100>,
    "reasoning_depth": <integer between 1 and 100>,
    "contextual_understanding": <integer between 1 and 100>,
    "creativity_level": <integer between 1 and 100>,
    "factual_knowledge": <integer between 1 and 100>
  }
}

Here are some examples:

Example 1:
Task: Classify this movie review as positive or negative: "I loved this film! The acting was superb
and the plot kept me engaged throughout."

{
  "complexity_score": 15,
  "explanation": "Simple sentiment classification with short input, minimal reasoning required.",
  "factors": {
    "input_length": 20,
    "output_length": 10,
    "task_type": "classification",
    "domain_specificity": 10,
    "reasoning_depth": 20,
    "contextual_understanding": 15,
    "creativity_level": 5,
    "factual_knowledge": 10
  }
}

Example 2:
Task: Summarize the key points of this 1000-word article on quantum computing.

{
  "complexity_score": 70,
  "explanation": "Long input on specialized topic, requires good summarization skills and technical understanding.",
  "factors": {
    "input_length": 80,
    "output_length": 50,
    "task_type": "summarization",
    "domain_specificity": 85,
    "reasoning_depth": 70,
    "contextual_understanding": 75,
    "creativity_level": 30,
    "factual_knowledge": 80
  }
}

Now, analyze the following task and provide the output in the required JSON format:

"""


class TaskComplexityRouter:
    """
    A router that determines the appropriate model for a given task based on its complexity.

    This class uses a router model to calculate a complexity score for each task.
    Tasks are then directed to either a base model or a complex model depending on
    whether their complexity score exceeds a specified threshold.

    Attributes:
        base_llm (RexiaAIOpenAI): The model used for tasks below the complexity threshold.
        complex_llm (RexiaAIOpenAI): The model used for tasks above the complexity threshold.
        router_llm (RexiaAIOpenAI): The model used to assess task complexity.
        task_complexity_threshold (int): The threshold for determining when to use the complex model.
        max_retries (int): The maximum number of times to reattempt getting a successful response from the router.

    """

    base_llm: RexiaAIOpenAI
    complex_llm: RexiaAIOpenAI
    router_llm: RexiaAIOpenAI
    task_complexity_threshold: int
    max_retries: int

    def __init__(
        self,
        base_llm: RexiaAIOpenAI,
        complex_llm: RexiaAIOpenAI,
        router_llm: RexiaAIOpenAI,
        task_complexity_threshold: int = 50,
        max_retries: int = 3,
    ):
        """
        Initialize the TaskComplexityRouter.

        Args:
            base_model (RexiaAIOpenAI): The model to use for less complex tasks.
            complex_model (RexiaAIOpenAI): The model to use for more complex tasks.
            router_model (RexiaAIOpenAI): The model to use for assessing task complexity.
            task_complexity_threshold (int, optional): The complexity threshold. Defaults to 50.
        """
        self.base_llm = base_llm
        self.complex_llm = complex_llm
        self.router_llm = router_llm
        self.task_complexity_threshold = task_complexity_threshold
        self.max_retries = max_retries

    def route(self, task: str) -> int:
        """
        Route the given task to the appropriate model based on its complexity.

        This method calculates the complexity score of the task to determine which
        model should be used.

        Args:
            task (str): The task to be routed and processed.

        Returns:
            int: The complexity score.
        """
        try:
            complexity_score = self._calculate_complexity_score(task)
            is_complex = complexity_score > self.task_complexity_threshold
            model_type = "complex" if is_complex else "base"
            print(f"Task complexity: {complexity_score}. Use {model_type} model.")
            return complexity_score
                    
        except Exception as e:
            print(f"Error in routing task: {e}.")

    def _calculate_complexity_score(self, task: str) -> int:
        """
        Calculate the complexity score of the given task.

        This method uses the router model to assess the task's complexity based on
        the predefined prompt and the task description. It will retry up to MAX_RETRIES
        times if there's an error in parsing the response.

        Args:
            task (str): The task to be assessed for complexity.

        Returns:
            int: The calculated complexity score.

        Raises:
            ValueError: If there's an error in parsing the router model's response
                or if the complexity score is invalid after all retries.
        """
        for attempt in range(self.max_retries):
            try:
                prompt = PREDEFINED_PROMPT + "\n\n" + task
                if attempt > 0:
                    prompt += f"\n\nPrevious attempt failed. Please ensure your response is in valid JSON format and includes a 'complexity_score' field with an integer value between 1 and 100."
                
                response = self.router_llm.invoke(prompt)
                parsed_response = self._parse_router_response(response)
                complexity_score = parsed_response.get('complexity_score')
                
                if not isinstance(complexity_score, (int, float)) or complexity_score < 1 or complexity_score > 100:
                    raise ValueError(f"Invalid complexity score: {complexity_score}")
                
                return int(complexity_score)
            
            except json.JSONDecodeError:
                if attempt == self.max_retries - 1:
                    raise ValueError("Failed to parse router model response as JSON after multiple attempts")
            except KeyError:
                if attempt == self.max_retries - 1:
                    raise ValueError("Router model response missing 'complexity_score' after multiple attempts")
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise ValueError(f"Unexpected error in calculating complexity score after multiple attempts: {str(e)}")
        
        raise ValueError("Failed to calculate complexity score after maximum retries")


    def _parse_router_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the JSON response from the router model.

        Args:
            response (str): The JSON string response from the router model.

        Returns:
            Dict[str, Any]: The parsed JSON response.

        Raises:
            json.JSONDecodeError: If the response is not valid JSON.
        """
        return json.loads(response)

import json5
import logging
from typing import Dict, Any
from ...llms import RexiaAIOpenAI
from ...common import Utility

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

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
"complexity_score": ,
"explanation": "",
"factors": {
"input_length": ,
"output_length": ,
"task_type": "",
"domain_specificity": ,
"reasoning_depth": ,
"contextual_understanding": ,
"creativity_level": ,
"factual_knowledge": 
Here are some examples:
Example 1:
Task: Classify this movie review as positive or negative: "I loved this film! The acting was superb
and the plot kept me engaged throughout."
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
Example 2:
Task: Summarize the key points of this 1000-word article on quantum computing.
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
    """

    def __init__(
        self,
        base_llm: RexiaAIOpenAI,
        complex_llm: RexiaAIOpenAI,
        router_llm: RexiaAIOpenAI,
        task_complexity_threshold: int = 50,
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
            logger.info(f"Task complexity: {complexity_score}. Use {model_type} model.")
            return complexity_score
        except Exception as e:
            logger.error(f"Error in routing task: {e}. Setting complexity to complexity threshold for safety.")
            return self.task_complexity_threshold

    def _calculate_complexity_score(self, task: str) -> int:
        """
        Calculate the complexity score of the given task.
        This method uses the router model to assess the task's complexity based on
        the predefined prompt and the task description.

        Args:
            task (str): The task to be assessed for complexity.

        Returns:
            int: The calculated complexity score.

        Raises:
            ValueError: If there's an error in parsing the router model's response
            or if the complexity score is invalid.
        """
        try:
            prompt = PREDEFINED_PROMPT + "\n\n" + task
            response = self.router_llm.invoke(prompt)
            cleaned_response = self._clean_router_response(response)
            parsed_response = json5.loads(cleaned_response)
            complexity_score = parsed_response.get('complexity_score')
            
            if not isinstance(complexity_score, (int, float)) or complexity_score < 1 or complexity_score > 100:
                raise ValueError(f"Invalid complexity score: {complexity_score}")
            
            return int(complexity_score)
        except Exception as e:
            try:
                fix_json_errors_prompt = Utility.fix_json_errors_prompt(json_string=response, error=e)
                fixed_response = self.base_llm.invoke(fix_json_errors_prompt)
                parsed_response = json5.loads(fixed_response)
                complexity_score = parsed_response.get('complexity_score')
                
                return int(complexity_score)
            except:
                raise ValueError("Error parsing router model's response or calculating complexity score.")

    def _clean_router_response(self, response: str) -> str:
        """
        Clean the JSON response from the router model.
        Args:
            response (str): The JSON string response from the router model.
        Returns:
            str: the cleaned JSON response.
        """
        cleaned_response = Utility.extract_json_string(response)
        cleaned_response = Utility.fix_json_errors(cleaned_response)
        return cleaned_response
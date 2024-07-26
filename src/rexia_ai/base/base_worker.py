"""BaseWorker class for ReXia.AI."""

import json5
import textwrap
import logging
from typing import Any, List
from abc import ABC
from ..structure import LLMOutput
from ..structure import RexiaAIResponse
from ..common import Utility

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
class BaseWorker(ABC):
    """
    BaseWorker for ReXia.AI. Allows for the creation of workers from a standard interface.

    Attributes:
        model: The model used by the worker.
        verbose: A flag used for enabling verbose mode.
        nlp: The spaCy NLP model for text compression.
    """

    model: Any
    verbose: bool
    nlp: Any

    def __init__(self, model: Any, verbose: bool = False):
        """
        Initialize a BaseWorker instance.

        Args:
            model: The model used by the worker.
            verbose: A flag used for enabling verbose mode. Defaults to False.
        """
        self.model = model
        self.verbose = verbose

    def action(self, prompt: str, worker_name: str) -> str:
        """
        Perform an action based on the prompt and return the response.

        Args:
            prompt: The prompt for the action.
            worker_name: The name of the worker performing the action.

        Returns:
            The response from the action.
        """
        agent_response = self._invoke_model(prompt)

        if self.verbose:
            logger.debug(f"{worker_name}: {agent_response}")

        return f"{worker_name}: {agent_response}"

    def create_prompt(self, prompt: str, task: str, messages: List[str]) -> str:
        """
        Create a prompt for the model with compression.

        Args:
            prompt: The base prompt.
            task: The task for which the prompt is created.
            messages: The messages from the collaboration chat.
            memory: The memory object containing the history of the agent's tasks.

        Returns:
            The created prompt as a string.
        """
        additional_context = self._format_additional_context(messages, task)
        structured_output_prompt = self.get_structured_output_prompt()

        final_prompt = (
            f"{prompt}\n\n" f"{additional_context}\n\n" f"{structured_output_prompt}"
        )
        return final_prompt

    def _format_additional_context(
        self, messages: List[str], task: str
    ) -> str:
        """
        Format the task, messages and memory for the prompt.

        Args:
            task: The task for which the prompt is created.
            messages: The messages from the collaboration chat.

        Returns:
            The formatted task and messages as a string.
        """
        formatted = (
            "\n\nTask:\n\n"
            + task
            + "\n\nCollaboration Chat:\n\n"
            + "\n\n".join(messages)
        )
        return formatted

    def _invoke_model(self, prompt: str) -> RexiaAIResponse:
        """
        Invoke the model with the given prompt and return the response.

        Args:
            prompt: The prompt for the model.

        Returns:
            The response from the model.
        """
        try:
            response = self.model.invoke(prompt)
            cleaned_response = self._clean_response(response)
            rexia_ai_response = RexiaAIResponse.from_json(cleaned_response)
            return rexia_ai_response
        except Exception as e:
            logger.error(f"Failed to get a valid response from the model. Error: {str(e)}")
            logger.debug(f"Model Response: {response}")
            logger.info("Attempting to fix the response...")
            try:
                fix_errors_prompt = Utility.fix_json_errors_prompt(
                    self, json_string=response, error=e
                )
                fixed_response = self.model.invoke(fix_errors_prompt)
                logger.info("Successfully fixed the response")
            except:
                logger.error("Failed to get a valid response from the model.")
                raise RuntimeError("Unable to get a valid response from the model.")
            rexia_ai_response = RexiaAIResponse.from_json(fixed_response)
            return rexia_ai_response

    def _clean_response(self, response: str) -> str:
        """
        Clean the response from the model.

        Args:
            response: The response from the model.

        Returns:
            The cleaned response.
        """
        cleaned_response = Utility.extract_json_string(response)
        cleaned_response = Utility.fix_json_errors(cleaned_response)
        return cleaned_response

    def get_structured_output_prompt(self) -> str:
        """
        Get the structured output prompt.

        Returns:
            The structured output prompt.
        """
        output_structure = json5.dumps(LLMOutput.get_output_structure(), indent=2)

        return textwrap.dedent(
            f"""\
            Structure your response using the following JSON format. It is critical that you
            include no information outside this structure and adhere strictly to the format:

            {output_structure}

            Important guidelines:
            1. Ensure all keys are exactly as shown above.
            2. The 'question' field should contain the original question asked.
            3. The 'plan' field is an array of strings, each representing a step in your plan.
            4. The 'answer' field should be an array of strings, where each string represents a single line.
            - Preserve indentation by including the appropriate number of spaces at the beginning of each line.
            - Include empty lines as empty strings in the array.
            5. The 'confidence_score' must be a float between 0.0 and 100.0.
            6. The 'chain_of_reasoning' is an array of strings, each representing a step in your reasoning process.
            7. The 'tool_calls' field is an array of objects. Each object must have a 'name' (string) and 'parameters' (object) field.
            8. Do not include any explanations, notes, or text outside of this JSON structure.
            9. Ensure that the JSON is valid and can be parsed without errors.
            10. Double-check that all required fields are present and correctly formatted.
            11. The code in the 'answer' field should follow all formatting and style guidelines provided in the original prompt.

            Your entire response should be valid JSON that can be parsed by a JSON parser.
            """
        )

    def _get_available_tools(self) -> str:
        """
        Get the available tools.

        Returns:
            A string representation of the available tools.
        """
        tools = ""
        for tool_name, tool in self.model.tools.items():
            tools += f"Tool: {tool_name}, Object: {tool.to_rexiaai_tool()}, Function Call: {tool.to_rexiaai_function_call()}\n"

        return tools
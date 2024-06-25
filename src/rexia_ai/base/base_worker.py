"""BaseWorker class for ReXia.AI."""

import re
import json
import textwrap
from typing import Any, List
from abc import ABC
from ..structure import LLMOutput
from ..structure import RexiaAIResponse


class BaseWorker(ABC):
    """
    BaseWorker for ReXia.AI. Allows for the creation of workers from a standard interface.

    Attributes:
        model: The model used by the worker.
        verbose: A flag used for enabling verbose mode.
        nlp: The spaCy NLP model for text compression.
        max_attempts: The maximum number of attempts to get a valid response from the model.
    """

    model: Any
    verbose: bool
    nlp: Any

    def __init__(self, model: Any, verbose: bool = False, max_attempts: int = 3):
        """
        Initialize a BaseWorker instance.

        Args:
            model: The model used by the worker.
            verbose: A flag used for enabling verbose mode. Defaults to False.
            max_attempts: The maximum number of attempts to get a valid response from the model. Defaults to 3.
        """
        self.model = model
        self.verbose = verbose
        self.max_attempts = max_attempts

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
            print(f"{worker_name}: {agent_response}")

        return f"{worker_name}: {agent_response}"

    def create_prompt(
        self, prompt: str, task: str, messages: List[str], memory: Any
    ) -> str:
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

        additional_context = self._format_additional_context(messages, memory, task)

        structured_output_prompt = self.get_structured_output_prompt()

        final_prompt = (
            f"{prompt}\n\n" f"{additional_context}\n\n" f"{structured_output_prompt}"
        )

        return final_prompt

    def _format_additional_context(
        self, messages: List[str], memory: Any, task: str
    ) -> str:
        """
        Format the task, messages and memory for the prompt.

        Args:
            task: The task for which the prompt is created.
            messages: The messages from the collaboration chat.
            memory: The memory object containing the history of the agent's tasks.

        Returns:
            The formatted task and messages as a string.
        """
        formatted = (
            "\n\nTask:\n\n"
            + task
            + "\n\nCollaboration Chat:\n\n"
            + "\n\n".join(messages)
            + "\n\nPrevious Task Details:\n\n"
            + memory.get_messages_as_string()
        )
        return formatted

    def remove_system_tokens(self, s: str) -> str:
        """
        Remove system tokens from the string.

        Args:
            s: The string from which to remove system tokens.

        Returns:
            The string with system tokens removed.
        """
        return re.sub(r"<\|.*\|>", "", s)

    def _invoke_model(self, prompt: str) -> RexiaAIResponse:
        """
        Invoke the model with the given prompt and return the response.

        Args:
            prompt: The prompt for the model.

        Returns:
            The response from the model.
        """
        attempt = 0

        while attempt < self.max_attempts:
            try:
                response = self.model.invoke(prompt)
                cleaned_response = self._clean_response(response)
                rexia_ai_response = RexiaAIResponse.from_json(cleaned_response)
                return rexia_ai_response
            except Exception as e:
                # Attempt to have the llm resolve any JSON errors
                prompt = f"""Your previous generation contained incorrectly formatted JSON. Please fix this and any other errors,
                    then return the correctly formatted JSON.

                    Issue: {str(e)}

                    Your previous JSON response was: 
                    {response}
                    
                    You should reuse the same question, plan, answer, confidence_score, chain_of_reasoning, and tool_calls 
                    from the previous response, but ensure that the JSON is correctly formatted.

                    Instructions for correction:
                    1. Carefully review the JSON structure and content.
                    2. Identify and fix any syntax errors (e.g., missing quotes, commas, brackets).
                    3. Ensure all keys are properly quoted.
                    4. Verify that string values are enclosed in double quotes.
                    5. Check that numbers, booleans, and null values are not quoted.
                    6. Remove any trailing commas in objects or arrays.
                    7. Eliminate any text or comments outside the JSON structure.

                    The JSON should conform to the following schema:
                    - `question`: a string representing the question asked.
                    - `plan`: an array of strings, each representing a step in the plan.
                    - `answer`: a string representing the final answer to the question.
                    - `confidence_score`: an integer representing the confidence score.
                    - `chain_of_reasoning`: an array of strings, each representing a step in the reasoning chain.
                    - `tool_calls`: an array of objects, each representing a tool call with the following structure:
                    - `name`: a string representing the name of the tool.
                    - `parameters`: an object containing key-value pairs of parameters for the tool.

                    Your response should ONLY contain valid JSON, structured as follows:
                    {{
                        "question": "The original question asked",
                        "plan": [
                            "Step 1 of the plan",
                            "Step 2 of the plan",
                            ...
                        ],
                        "answer": "The final answer to the question",
                        "confidence_score": 0,
                        "chain_of_reasoning": [
                            "Reasoning step 1",
                            "Reasoning step 2",
                            ...
                        ],
                        "tool_calls": [
                            {{
                                "name": "ToolName1",
                                "parameters": {{
                                    "parameter1": "value1",
                                }}
                            }},
                            {{
                                "name": "ToolName2",
                                "parameters": {{
                                    "parameter1": "value1",
                                    "parameter2": "value2"
                                }}
                            }},
                            ...
                        ]
                    }}

                    Do not include anything outside this structure or the task will fail.
                    Do not include any comments or additional information or the task will fail.
                    Do not include any text outside the JSON structure or the task will fail.
                    Do not include any unquoted keys or values or the task will fail.
                    Do not include any syntax errors or the task will fail.
                    Return only your previous JSON response, corrected to conform to the schema or the task will fail.
                    """
                print(
                    "Failed to get a valid response from the model. "
                    f"Error: {str(e)}\n\nModel "
                    f"Response: {response}\n\nRetrying..."
                )
            attempt += 1

        # If we reach here, we've failed after max_attempts
        raise Exception(
            "Failed to get a valid response from the model after maximum attempts"
        )

    def _clean_response(self, response: str) -> str:
        """
        Clean the response from the model.

        Args:
            response: The response from the model.

        Returns:
            The cleaned response.
        """
        cleaned_response = self.remove_system_tokens(response)
        cleaned_response = self._strip_python_tags(cleaned_response)
        return cleaned_response

    def _strip_python_tags(self, code: str) -> str:
        """
        Strip python tags from the start and end of a string of code.

        Args:
            code: The code from which to strip python tags.

        Returns:
            The code with python tags stripped.
        """
        return re.sub(r"^```python\n|```$", "", code, flags=re.MULTILINE)

    def get_structured_output_prompt(self) -> str:
        """
        Get the structured output prompt.

        Returns:
            The structured output prompt.
        """
        
        output_structure = json.dumps(LLMOutput.get_output_structure(), indent=2)
        
        return textwrap.dedent(f"""\
            Structure your response using the following JSON format. It is critical that you
            include no information outside this structure and adhere strictly to the format:

            {output_structure}

            Important guidelines:
            1. Ensure all keys are exactly as shown above.
            2. The 'question' field should contain the original question asked.
            3. The 'plan' field is an array of strings, each representing a step in your plan.
            4. The 'answer' field should contain your final response to the question.
            5. The 'confidence_score' must be an integer between 0 and 100.
            6. The 'chain_of_reasoning' is an array of strings, each representing a step in your reasoning process.
            7. The 'tool_calls' field is an array of objects. Each object must have a 'name' (string) and 'parameters' (object) field.
            8. Do not include any explanations, notes, or text outside of this JSON structure.
            9. Ensure that the JSON is valid and can be parsed without errors.
            10. Double-check that all required fields are present and correctly formatted.

            Your entire response should be valid JSON that can be parsed by a JSON parser.
            """)
        
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

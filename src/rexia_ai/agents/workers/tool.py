"""ToolWorker class in ReXia.AI."""
import secrets
from typing import Any, List, Dict
from ...base import BaseWorker
from ...structure import RexiaAIResponse

PREDEFINED_PROMPT = """
    As a tool calling agent for ReXia.AI, your role is key in supporting task completion. 

    Select tools based on their capabilities, limitations, and trade-offs. Aim for efficiency and minimal redundancy.

    Use tools wisely. Make multiple calls if needed, refining your approach based on previous outputs.

    After a tool call, parse the output, handle errors, and integrate the results into the solution. 
    If output is unclear, consider using additional tools or asking the team for clarification.

    Communicate effectively with the team, share important information, and coordinate your efforts for a unified approach.

    Be aware of limitations like resource and time constraints, or ethical considerations, and adjust 
    your tool usage accordingly.

    If the task has specific formatting requests, apply them only within the answer.
    """

class ToolWorker(BaseWorker):
    """
    A specialised tool writing worker for a ReXia.AI agent.

    This worker is responsible for gathering information for the rest of the team to 
    complete the task.

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
        Initialize a ToolWorker instance.

        Args:
            model: The model used by the worker.
            verbose: A flag used for enabling verbose mode. Defaults to False.
        """
        super().__init__(model, verbose=verbose)

    def action(self, prompt: str, worker_name: str) -> str:
        """
        Work on the current task.

        Args:
            prompt: The prompt for the model.
            worker_name: The name of the worker.

        Returns:
            The formatted response from the model.
        """
        agent_response = self._invoke_model(prompt)
        results = self._handle_tool_calls(agent_response)
        formatted_response = self._format_response(worker_name, agent_response, results)
        return formatted_response

    def create_prompt(self, task: str, messages: List[str], memory: Any) -> str:
        """
        Create a prompt for the model.

        The prompt is created by combining a predefined string with the task
        and the messages from the collaboration chat.

        Args:
            task: The task for which the prompt is created.
            messages: The messages from the collaboration chat.

        Returns:
            The created prompt as a string.
        """
        unique_id = self._get_unique_id()

        prompt = (
            PREDEFINED_PROMPT
            + """
                To call a tool, use the JSON format provided below, ensuring that your tool
                calls are properly formatted JSON with the correct tool names and arguments.
                Do not generate incomplete JSON or JSON with syntax errors.
                
                Your tool calls should all be contained within the "tool_calls" list of the
                structured format requested below.

                {
                "tool_calls": [
                    {
                    "name": "ToolName",
                    "args": {
                        "arg1": "value1",
                        "arg2": "value2"
                    },
                    "id": "{unique_id}"
                    }
                ]
                }

                For example, if asked "What is 3 * 12?" and you have a Multiply tool, respond with:

                {
                "tool_calls": [
                    {
                    "name": "Multiply",
                    "args": {
                        "a": 3,
                        "b": 12
                    },
                    "id": "{unique_id}"
                    }
                ]
                }
                
            """
            + f"""
            Task: {task}

            Available Tools:
            {self._get_available_tools()}

            Collaboration Chat:
            """
            + "\n\n".join(messages)
            + "\n\n"
            + "Previous Task Results"
            + "\n\n" + memory.get_messages_as_string()
            + self.get_structured_output_prompt()
        ).replace("{unique_id}", unique_id)

        return prompt
    
    def _handle_tool_calls(self, rexia_ai_response: RexiaAIResponse) -> Dict:
        """
        Handle the tool calls in the rexia_ai_response.

        Args:
            rexia_ai_response: The RexiaAIResponse containing the tool calls.

        Returns:
            The results of the tool calls as a dictionary.
        """
        results = {}
        
        response_dict = rexia_ai_response.to_dict()

        for tool_call in response_dict["tool_calls"]:
            tool_name = tool_call.get("name")
            tool_args = tool_call.get("args", {})
            tool_id = tool_call.get("id")

            if tool_name in self.model.tools:
                tool = self.model.tools[tool_name]
                function_name = tool.to_rexiaai_function_call().get("name")
                function_to_call = getattr(tool, function_name, None)
                if function_to_call:
                    try:
                        result = function_to_call(**tool_args)
                        results[tool_id] = result
                    except Exception as e:
                        results[tool_id] = str(e)
                else:
                    print(f"Function {function_name} not found in tool {tool_name}")
            else:
                print(f"Tool {tool_name} not found")
                print("\n\nAvailable tools: \n")
                for tool in self.model.tools:
                    print(str(tool) + "\n")

        return results
    
    def _format_response(
    self, worker_name: str, agent_response: str, results: Dict
    ) -> str:
        """
        Format the response.

        Args:
            worker_name: The name of the worker.
            agent_response: The response from the agent.
            results: The results of the tool calls.

        Returns:
            The formatted response as a string.
        """
        if self.verbose:
            print(f"{worker_name}: {agent_response}\n\n Results: {results}")

        return f"{worker_name}: {results}"

    def _get_unique_id(self) -> str:
        """
        Get a unique id.

        Returns:
            The unique id as a string.
        """
        return secrets.token_hex(16)
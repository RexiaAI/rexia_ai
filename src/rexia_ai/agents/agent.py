"""Agent class for ReXia.AI."""

import re
from typing import Type, Any, Optional, List
from ..workflows import ReflectWorkflow
from ..structure import RexiaAIResponse
from ..memory import WorkingMemory
from ..base import BaseMemory, BaseWorkflow


class Agent:
    """
    Agent class for ReXia AI.

    This agent is responsible for running the workflow, and reflecting on the task.

    Attributes:
        workflow: The workflow used by the agent.
        task: The task assigned to the agent.
    """

    workflow: BaseWorkflow
    task: str

    def __init__(
        self,
        llm: Any,
        task: str,
        workflow: Optional[Type[BaseWorkflow]] = None,
        memory: BaseMemory = WorkingMemory(),
        verbose: bool = False,
        max_attempts: int = 3,
    ):
        """
        Initialize an Agent instance.

        Args:
            llm: The language model used by the agent.
            task: The task assigned to the agent.
            workflow_class: The class of the workflow to be used by the agent.
            verbose: A flag used for enabling verbose mode. Defaults to False.
            max_attempts: The maximum number of attempts to get a valid response from the model. Defaults to 3.
        """
        if not workflow:
            workflow = ReflectWorkflow
        self.workflow = workflow(llm=llm, task=task, memory=memory, verbose=verbose, max_attempts=max_attempts)
        self.task = task
        self.llm = llm
        self.verbose = verbose
        self.max_attempts = max_attempts

    def run_workflow(self) -> List[str]:
        """
        Run the workflow and return the messages.

        Returns:
            The messages from the workflow.
        """
        self.workflow.run()
        return self.workflow.channel.messages

    def get_task_result(self, messages: List[str]) -> Optional[str]:
        """
        Extract the task result from the messages.

        Args:
            messages: The messages from which to extract the task result.

        Returns:
            The task result if it exists, None otherwise.
        """
        if not messages:
            print("Error: No messages to process.")
            return None

        return messages[-1]

    def invoke(self, task: str = None) -> Optional[str]:
        """
        Invoke method for the agent.

        This method runs the workflow, gets the task result and the plan, updates the buffer manager with the plan,
        and returns the accepted answer if it exists.

        Returns:
            The accepted answer if it exists, None otherwise.
        """
        try:
            if task:
                self.task = task
                self.workflow.channel.task = task
            self.workflow.clear_channel() # Clear any messages from a previous task.
            messages = self.run_workflow()
            task_result = self.get_task_result(messages)
            accepted_answer = self.format_accepted_answer(task_result)
            return accepted_answer
        except Exception as e:
            print(f"Unexpected error: {e}")

    def format_accepted_answer(self, answer: str) -> Optional[RexiaAIResponse]:
        """
        Format the accepted answer by removing any single word before the JSON object.

        Args:
            answer: The accepted answer to format.

        Returns:
            The formatted RexiaAIResponse if it exists and is valid, None otherwise.
        """
        if not answer:
            return None

        try:
            # Find the start of the JSON object
            json_start = answer.find('{')
            
            if json_start == -1:
                raise ValueError("No JSON object found in the answer")
            
            # Use regex to find the last word before the JSON object
            match = re.search(r'\S+\s*$', answer[:json_start])
            
            if match:
                # Remove the word and any whitespace after it
                json_str = answer[json_start:]
            else:
                json_str = answer[json_start:]

            # Parse the JSON string into a RexiaAIResponse object
            rexia_ai_response = RexiaAIResponse.from_json(json_str)

            return rexia_ai_response
        except Exception as e:
            print(f"Error while formatting the answer: {e}")
            return None

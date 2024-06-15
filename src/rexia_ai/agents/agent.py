"""Agent class for ReXia.AI."""

import re
import json
from typing import List, Optional
from ..workflows import ReflectWorkflow
from ..thought_buffer import BufferManager

class Agent:
    """
    Agent class for ReXia AI.

    This agent is responsible for running the workflow, managing the buffer, and reflecting on the task.

    Attributes:
        workflow: The workflow used by the agent.
        buffer_manager: The buffer manager used by the agent.
        task: The task assigned to the agent.
    """

    def __init__(self, llm, task: str, verbose: bool = False):
        """
        Initialize an Agent instance.

        Args:
            llm: The language model used by the agent.
            task: The task assigned to the agent.
            verbose: A flag used for enabling verbose mode. Defaults to False.
        """
        self.workflow = ReflectWorkflow(llm, task, verbose)
        self.buffer_manager = BufferManager()
        self.task = task

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

    def reflect(self) -> Optional[str]:
        """
        Reflect method for the agent.

        This method runs the workflow, gets the task result and the plan, updates the buffer manager with the plan,
        and returns the accepted answer if it exists.

        Returns:
            The accepted answer if it exists, None otherwise.
        """
        try:
            messages = self.run_workflow()
            task_result = self.get_task_result(messages)
            plan = self.get_plan(messages)
            self.buffer_manager.insert_or_update_plan(task=self.task, plan=plan)
            accepted_answer = self.format_accepted_answer(task_result)
            return accepted_answer
        except Exception as e:
            print(f"Unexpected error: {e}")

    def format_accepted_answer(self, answer: str) -> Optional[str]:
        """
        Format the accepted answer.

        Args:
            answer: The accepted answer to format.

        Returns:
            The formatted accepted answer if it exists, None otherwise.
        """
        if not answer:
            return None

        # Remove 'finalise: ' from the string
        answer = answer.replace('finalise: ', '')
        
        # Remove escape characters
        answer = answer.encode('utf-8').decode('unicode_escape')

        # Convert the string to a JSON object
        answer_json = json.loads(answer)
        
        return answer_json

    def get_plan(self, messages: List[str]) -> Optional[str]:
        """
        Get the plan from the workflow.

        Args:
            messages: The messages from which to extract the plan.

        Returns:
            The plan if it exists, None otherwise.
        """
        for message in messages:
            match = re.search(r"plan: (.*?)(, \w+:|$)", message, re.DOTALL)
            if match:
                plan = match.group(1)
                # Remove leading and trailing whitespace
                plan = plan.strip()
                return plan

        print("Error: Failed to extract plan.")
        return None
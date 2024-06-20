"""Agent class for ReXia.AI."""

from typing import List, Optional
from ..workflows import ReflectWorkflow
from ..structure import RexiaAIResponse
from ..memory import WorkingMemory
from ..base import BaseMemory

class Agent:
    """
    Agent class for ReXia AI.

    This agent is responsible for running the workflow, and reflecting on the task.

    Attributes:
        workflow: The workflow used by the agent.
        task: The task assigned to the agent.
    """
    
    workflow: ReflectWorkflow
    task: str

    def __init__(self, llm, task: str, memory: BaseMemory = WorkingMemory(), verbose: bool = False):
        """
        Initialize an Agent instance.

        Args:
            llm: The language model used by the agent.
            task: The task assigned to the agent.
            verbose: A flag used for enabling verbose mode. Defaults to False.
        """
        self.workflow = ReflectWorkflow(llm=llm, task=task, memory=memory, verbose=verbose)
        self.task = task
        self.memory = memory

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

    def reflect(self, task: str = None) -> Optional[str]:
        """
        Reflect method for the agent.

        This method runs the workflow, gets the task result and the plan, updates the buffer manager with the plan,
        and returns the accepted answer if it exists.

        Returns:
            The accepted answer if it exists, None otherwise.
        """
        try:
            if task:
                self.task = task
                self.workflow.channel.task = task
            
            messages = self.run_workflow()
            task_result = self.get_task_result(messages)
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

        try:
            # Remove 'finalise: ' from the string
            answer = answer.replace('finalise: ', '')
            
            # 
            rexia_ai_response = RexiaAIResponse.from_json(answer)
            
            return rexia_ai_response
        except Exception as e:
            print(f"Error while formatting the answer: {e}")
            return None
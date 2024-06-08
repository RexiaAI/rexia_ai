"""reflect agent class for ReXia AI."""

import re
from ..workflows import ReflectWorkflow

class ReflectAgent:
    """ReflectAgent class for ReXia AI."""
    def __init__(self, llm, task: str, verbose: bool = False):
        self.worker = ReflectWorkflow(llm, task, verbose)

    def run_worker(self):
        """Run the worker and return the messages."""
        self.worker.run()
        return self.worker.channel.messages

    def get_task_result(self, messages):
        """Extract the task result from the messages."""
        try:
            return messages[-1]
        except IndexError:
            print("Error: No messages to process.")
            return None

    def extract_accepted_answer(self, task_result):
        """Use a regular expression to extract the accepted answer."""
        match = re.search(r'"accepted answer": "(.*?)"', task_result)
        if match:
            return match.group(1)
        else:
            print("Error: Failed to extract accepted answer.")
            return None

    def reflect(self):
        """Reflect method for ReflectAgent."""
        try:
            messages = self.run_worker()
            task_result = self.get_task_result(messages)
            if task_result is not None:
                accepted_answer = self.extract_accepted_answer(task_result)
                return accepted_answer
        except Exception as e:
            print(f"Unexpected error: {e}")
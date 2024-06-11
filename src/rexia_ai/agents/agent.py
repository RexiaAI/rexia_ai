"""agent class for ReXia AI."""

import re
from ..workflows import ReflectWorkflow
from ..thought_buffer import BufferManager


class Agent:
    """Agent class for ReXia AI."""

    def __init__(self, llm, task: str, verbose: bool = False):
        self.workflow = ReflectWorkflow(llm, task, verbose)
        self.buffer_manager = BufferManager()
        self.task = task

    def run_workflow(self):
        """Run the worker and return the messages."""
        self.workflow.run()
        return self.workflow.channel.messages

    def get_task_result(self, messages):
        """Extract the task result from the messages."""
        try:
            return messages[-1]
        except IndexError:
            print("Error: No messages to process.")
            return None

    def extract_accepted_answer(self, task_result):
        """Use a regular expression to extract the accepted answer."""
        try:
            # Search for the pattern 'accepted_answer": ' followed by any characters until the next closing quote
            match = re.search(
                r'accepted_answer": "(.*?)"',
                task_result,
                re.DOTALL | re.IGNORECASE,
            )
            if match:
                answer_value = match.group(1).strip()
                return answer_value
            else:
                print("Error: Failed to extract accepted answer.")
                return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
            
    def reflect(self):
        """Reflect method for the agent."""
        try:
            messages = self.run_workflow()
            task_result = self.get_task_result(messages)
            plan = self.get_plan(messages)
            self.buffer_manager.insert_or_update_plan(task=self.task, plan=plan)
            if task_result is not None:
                accepted_answer = self.extract_accepted_answer(task_result)
                return accepted_answer
        except Exception as e:
            print(f"Unexpected error: {e}")

    def get_plan(self, messages):
        """Get the plan from the workflow."""
        for message in messages:
            match = re.search(r"plan: (.*?)(, \w+:|$)", message, re.DOTALL)
            if match:
                plan = match.group(1)
                # Remove leading and trailing whitespace
                plan = plan.strip()
                return plan

        print("Error: Failed to extract plan.")
        return None

"""Component class for ReXia.AI."""

from typing import Any

class Component:
    """
    A general component that uses specialised workers to perform different tasks.

    Attributes:
        name: The name of the component.
        channel: The channel used by the component.
        worker: The worker used by the component.
    """
    def __init__(self, name: str, channel: Any, worker: Any):
        """
        Initialize a Component instance.

        Args:
            name: The name of the component.
            channel: The channel used by the component.
            worker: The worker used by the component.
        """
        self.name = name
        self.channel = channel
        self.worker = worker

    def run(self) -> Any:
        """
        Run the component and return the response.

        Returns:
            The response from performing the task.
        """
        response = self.perform_task()
        return response
                
    def perform_task(self) -> Any:
        """
        Perform the task assigned to the component and return the response.

        The task is retrieved from the channel, a prompt is created using the worker,
        an action is performed using the worker and the prompt, and the response is put into the channel.

        Returns:
            The response from performing the action.
        """
        task = self.channel.task
        messages = self.channel.messages
        print(f"{self.name} task: {task}")
        prompt = self.worker.create_prompt(task, messages)
        response = self.worker.action(prompt, self.name)
        self.channel.put(response)
        return response
    
    def get_tool_results(self) -> str:
        """
        Get the results of the tools used by the component.

        Returns:
            A string indicating that the tool results are not implemented.
        """
        return "Tool results: NOT IMPLEMENTED"
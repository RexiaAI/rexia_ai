"""Component class for ReXia.AI."""

from typing import Any
from ..base import BaseMemory, BaseWorker
from ..common import CollaborationChannel

class Component:
    """
    A general component that uses specialised workers to perform different tasks.

    Attributes:
        name: The name of the component.
        channel: The channel used by the component.
        worker: The worker used by the component.
    """
    
    name: str
    channel: CollaborationChannel
    worker: BaseWorker
    memory: BaseMemory
    
    def __init__(self, name: str, channel: CollaborationChannel, worker: BaseWorker, memory: BaseMemory):
        """
        Initialize a Component instance.

        Args:
            name: The name of the component.
            channel: The channel used by the component.
            worker: The worker used by the component.
            memory: The memory used by the component.
        """
        self.name = name
        self.channel = channel
        self.worker = worker
        self.memory = memory

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
        memory = self.memory
        prompt = self.worker.create_prompt(task=task, messages=messages, memory=memory)
        response = self.worker.action(prompt=prompt, worker_name=self.name)
        self.channel.put(response)
        return response
"""WorkingMemory module for ReXia.AI's persistent memory management system."""

from typing import List
from ..base import BaseMemory

class WorkingMemory(BaseMemory):
    """
    WorkingMemory class for ReXia.AI, implementing a persistent working memory object.

    This class provides a concrete implementation of the BaseMemory abstract class,
    designed to maintain a list of messages that persist between runs of an Agent instance.
    It manages message storage, retrieval, and truncation to ensure efficient memory usage.

    Attributes:
        max_length (int): The maximum number of messages to store in the working memory.
        messages (List[str]): A list containing the stored messages.
    """

    max_length: int
    messages: List[str]

    def __init__(self, max_length: int = 10):
        """
        Initialize the WorkingMemory object.

        Sets up the initial state of the working memory, including the maximum
        length of stored messages and an empty message list.

        Args:
            max_length (int, optional): The maximum number of messages to store. Defaults to 10.
        """
        self.max_length = max_length
        self.messages = []

    def add_message(self, message: str) -> None:
        """
        Add a new message to the working memory.

        Appends the given message to the list of stored messages and ensures
        that the total number of messages does not exceed the specified max_length.

        Args:
            message (str): The message to be added to the working memory.

        Returns:
            None
        """
        self.messages.append(message)
        self.truncate_messages(self.max_length)

    def get_messages(self) -> List[str]:
        """
        Retrieve all messages currently stored in the working memory.

        Returns:
            List[str]: A list of all stored messages in their original order.
        """
        return self.messages

    def get_messages_as_string(self) -> str:
        """
        Retrieve all messages as a single string, with the most recent message first.

        This method joins all stored messages into a single string, reversing their
        order so that the most recently added message appears first.

        Returns:
            str: A string containing all messages, separated by spaces, with the most recent first.
        """
        return " ".join(reversed(self.messages))

    def clear_messages(self) -> None:
        """
        Remove all messages from the working memory.

        Resets the messages list to an empty state.

        Returns:
            None
        """
        self.messages = []

    def truncate_messages(self, max_length: int) -> None:
        """
        Reduce the number of stored messages to a specified maximum.

        If the number of stored messages exceeds the specified max_length,
        this method removes the oldest messages to bring the total count
        down to max_length.

        Args:
            max_length (int): The maximum number of messages to retain.

        Returns:
            None
        """
        if len(self.messages) > max_length:
            self.messages = self.messages[-max_length:]
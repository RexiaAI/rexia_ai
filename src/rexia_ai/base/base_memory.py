"""BaseMemory module for ReXia.AI's memory management system."""

from typing import List
from abc import ABC, abstractmethod

class BaseMemory(ABC):
    """
    Abstract base class defining the interface for memory objects in ReXia.AI.

    This class provides a blueprint for implementing various types of memory
    systems within the ReXia.AI framework. It defines the essential methods
    that any concrete memory implementation should provide, ensuring consistency
    across different memory management strategies.

    The BaseMemory class is designed to be subclassed, with concrete implementations
    providing specific logic for message storage, retrieval, and management.

    Attributes:
        No public attributes are defined in the base class.
    """

    @abstractmethod
    def __init__(self, max_length: int = 10):
        """
        Initialize a BaseMemory instance.

        This abstract method should be implemented to set up the initial state
        of the memory object, including any necessary data structures.

        Args:
            max_length (int, optional): The maximum number of messages to store. Defaults to 10.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass

    @abstractmethod
    def add_message(self, message: str) -> None:
        """
        Add a new message to the memory.

        This method should implement the logic for adding a new message to the
        memory storage, potentially managing the total number of stored messages
        to not exceed the max_length.

        Args:
            message (str): The message to be added to the memory.

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass

    @abstractmethod
    def get_messages(self) -> List[str]:
        """
        Retrieve all messages currently stored in the memory.

        This method should return a list of all messages currently held in the
        memory object, in the order they were added.

        Returns:
            List[str]: A list of stored messages.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass

    @abstractmethod
    def clear_messages(self) -> None:
        """
        Remove all messages from the memory.

        This method should implement the logic to clear all stored messages,
        effectively resetting the memory to its initial state.

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass

    @abstractmethod
    def truncate_messages(self, max_length: int) -> None:
        """
        Reduce the number of stored messages to a specified maximum.

        This method should implement the logic to limit the number of stored
        messages to the specified max_length, typically by removing the oldest
        messages first.

        Args:
            max_length (int): The maximum number of messages to retain.

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass
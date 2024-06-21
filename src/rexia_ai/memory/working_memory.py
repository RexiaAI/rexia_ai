"""WorkingMemory class for ReXia.AI."""

from typing import List
from ..base import BaseMemory


class WorkingMemory(BaseMemory):
    """WorkingMemory class for ReXia.AI. Implements a working memory object that persists
    between run's on an instance of an Agent."""

    max_length: int
    messages: List[str]

    def __init__(self, max_length: int = 10):
        """Initialize the working memory object."""
        self.max_length = max_length
        self.messages = []

    def add_message(self, message: str):
        """Add a message to the working memory."""
        self.messages.append(message)
        self.truncate_messages(self.max_length)

    def get_messages(self):
        """Get all messages from the working memory."""
        return self.messages

    def get_messages_as_string(self):
        """Get all messages from the working memory as a single string."""
        return " ".join(self.messages)

    def clear_messages(self):
        """Clear all messages from the working memory."""
        self.messages = []

    def truncate_messages(self, max_length: int):
        """Truncate the working memory to the specified length."""
        if len(self.messages) > max_length:
            self.messages = self.messages[-max_length:]

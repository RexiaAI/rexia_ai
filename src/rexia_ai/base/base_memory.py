"""BaseMemory class for ReXia.AI."""

from typing import List
from abc import ABC, abstractmethod

class BaseMemory(ABC):
    """BaseMemory class for ReXia.AI. Defines an interface for memory objects"""
    
    @abstractmethod
    def __init__(self, max_length: int = 10):
        pass
    
    @abstractmethod
    def add_message(self, message: str):
        pass
    
    @abstractmethod
    def get_messages(self) -> List[str]:
        pass
    
    @abstractmethod
    def clear_messages(self):
        pass
    
    @abstractmethod
    def truncate_messages(self, max_length: int):
        pass
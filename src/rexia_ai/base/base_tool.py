"""Rexia.AI BaseTool - Tools that work with ReXia.AI"""

from typing import Any, Dict, List
from abc import ABC, abstractmethod

class BaseTool(ABC):
    """
    A base tool that works with ReXia.AI.

    Attributes:
        name: The name of the tool.
        func: The function that the tool performs.
        description: A description of the tool.
    """
    
    name: str
    func: Any
    description: str
    
    def __init__(self, name: str, func: Any, description: str):
        """
        Initialize a BaseTool instance.

        Args:
            name: The name of the tool.
            func: The function that the tool performs.
            description: A description of the tool.
        """
        self.name = name
        self.func = func
        self.description = description

    @abstractmethod
    def to_rexiaai_tool(self) -> List:
        """
        Return the tool as a JSON object for ReXia.AI.

        Returns:
            An empty list. This method should be overridden in a subclass.
        """
        pass

    @abstractmethod
    def to_rexiaai_function_call(self) -> Dict:
        """
        Return the tool as a dictionary object for ReXia.AI.

        Returns:
            An empty dictionary. This method should be overridden in a subclass.
        """
        pass
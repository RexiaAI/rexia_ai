""" Rexia AI BaseTool - Tools that work with ReXia.AI"""

from typing import Any


class BaseTool():
    """Tool that works with ReXia.AI."""
    def __init__(self, name: str, func: Any, description: str):
        self.name = name
        self.func = func
        self.description = description

    def to_rexiaai_tool(self):
        """Return the tool as a JSON object for ReXia.AI."""

        tool = []

        return tool

    def to_rexiaai_function_call(self):
        """Return the tool as a dictionary object for ReXia.AI."""
        function_call = {}

        return function_call
    

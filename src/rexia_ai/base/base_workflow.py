"""Base Workflow for ReXia AI."""

from typing import Any

class BaseWorkflow:
    """BaseWorkFlow Class for ReXia AI, refactored for better design principles."""
    def __init__(self, llm: Any, task: str, verbose: bool):
        self.llm = llm
        self.verbose = verbose
        self.task = task
            
        
        

            
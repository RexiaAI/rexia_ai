"""Agency class for ReXia AI"""

from typing import List
from ..base import BaseWorkflow

class Agency():
    """Agency class for ReXia AI"""
    def __init__(self, workflows: List[BaseWorkflow]):
        self.workflows = workflows
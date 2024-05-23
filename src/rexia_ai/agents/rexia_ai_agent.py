"""RexiaAIAgent class for ReXia AI."""

import json
import unicodedata
from typing import List, Optional
from langchain_core.tools import Tool
from ..llms import RexiaAIChatOpenAI
from ..common import AgencyStateSchema

class RexiaAIAgent:
    """Collaborative Agent for ReXia AI."""

    model: RexiaAIChatOpenAI
    tools: Optional[List[Tool]]

    def __init__(self, agent_name: str, model: RexiaAIChatOpenAI, instructions: str = "", verbose: bool = False):
        self.name = agent_name
        self.model = model
        self.instructions = instructions
        self.verbose = verbose

    def work(self, agency_state: AgencyStateSchema) -> AgencyStateSchema:
        """Work on the current task."""
        graph_state = agency_state
        
        if self.verbose:
            print(f"{self.name} working on task: {graph_state['task']}")
            
        prompt = {
            "instructions": (
                self.instructions + " Always respond in the provided format."
                " Ensure that no control characters are included in the JSON."
                " Always follow the provided guidelines."
            ),
            "task": graph_state["task"],
            "guidelines": graph_state["guidelines"],
            "messages": graph_state["messages"],
            "response format": "{\"message\": \"Your response here.\"}"
        }
            
        agent_response = json.loads(self.model.invoke(json.dumps(prompt)).content)
        
        if self.verbose:
            print(f"{self.name} response: {agent_response['message']}")

        # Strip control characters from the response message
        cleaned_message = self._strip_control_characters(agent_response["message"])
        
        graph_state["messages"].append(cleaned_message)
        return graph_state

    def _strip_control_characters(self, s: str) -> str:
        """Remove control characters from a string."""
        return "".join(ch for ch in s if unicodedata.category(ch) != "Cc")

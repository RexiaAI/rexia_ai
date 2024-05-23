"""Manager Agent for ReXia AI."""

import json
import unicodedata
from ..llms import RexiaAIChatOpenAI
from ..common import AgencyStateSchema, TaskStatus

class PlanningAgent:
    """Manager Agent for ReXia AI."""

    def __init__(self, model: RexiaAIChatOpenAI, verbose: bool = False):
        self.name = "Manager"
        self.model = model
        self.verbose = verbose

    def work(self, agency_state: AgencyStateSchema) -> AgencyStateSchema:
        """Work on the current task."""
        if self.verbose:
            print(f"Planner working on task: {agency_state['task']}")

        return self._handle_pending_task(agency_state)
        
    def _handle_pending_task(self, agency_state: AgencyStateSchema) -> AgencyStateSchema:
        """Handle the task when its status is PENDING."""
        agency_state["task_status"] = TaskStatus.WORKING
        prompt = self._create_pending_task_prompt(agency_state["task"])
        planner_guidelines = self._invoke_model(prompt)
        agency_state["guidelines"] = planner_guidelines["guidelines"]
        if self.verbose:
            print(f"Planner guidelines: {planner_guidelines['guidelines']}")
        return agency_state

    def _create_pending_task_prompt(self, task: str) -> dict:
        """Create a prompt for a pending task."""
        return {
            "instructions": (
                "Read the task, explain to an AI your guidelines on how to complete it. "
                "Use the response format provided. Ensure that no control characters are included in the JSON."
            ),
            "task": task,
            "response format": "{\"guidelines\": \"Your guidelines here.\"}"
        }

    def _invoke_model(self, prompt: dict) -> dict:
        """Invoke the model with the given prompt and return the response."""
        response = self.model.invoke(json.dumps(prompt)).content
        cleaned_response = self._strip_control_characters(response)
        return json.loads(cleaned_response)

    def _strip_control_characters(self, s: str) -> str:
        """Remove control characters from a string."""
        return "".join(ch for ch in s if unicodedata.category(ch) != "Cc")

"""Review Agent class for ReXia AI."""

import json
import unicodedata
from ..llms import RexiaAIChatOpenAI
from ..common import AgencyStateSchema, TaskStatus

class ReviewAgent:
    """Review Agent for ReXia AI."""
    
    def __init__(self, model: RexiaAIChatOpenAI, verbose: bool = False):
        self.name = "Reviewer"
        self.model = model
        self.verbose = verbose
        
    def work(self, agency_state: AgencyStateSchema) -> AgencyStateSchema:
        """Work on the current task."""
        if self.verbose:
            print(f"Reviewer working on task: {agency_state['task']}")
        return self._handle_working_task(agency_state)

    def _handle_working_task(self, agency_state: AgencyStateSchema) -> AgencyStateSchema:
        """Handle the task when its status is WORKING."""
        prompt = self._create_working_task_prompt(agency_state)
        reviewer_approval = self._invoke_model(prompt)

        if self.verbose:
            print(f"Reviewer approval: {reviewer_approval['status']}")

        if reviewer_approval["status"] == "COMPLETED":
            return self._handle_completed_task(agency_state)
        else:
            return self._handle_rejected_task(agency_state)

    def _handle_completed_task(self, agency_state: AgencyStateSchema) -> AgencyStateSchema:
        """Handle the task when it is marked as COMPLETED."""
        agency_state["task_status"] = TaskStatus.COMPLETED
        prompt = self._create_completed_task_prompt(agency_state)
        reviewer_accepted_result = self._invoke_model(prompt)
        agency_state["accepted_result"] = reviewer_accepted_result["accepted_result"]
        if self.verbose:
            print(f"Reviewer accepted result: {reviewer_accepted_result['accepted_result']}")
        return agency_state

    def _handle_rejected_task(self, agency_state: AgencyStateSchema) -> AgencyStateSchema:
        """Handle the task when it is marked as REJECTED."""
        agency_state["task_status"] = TaskStatus.WORKING
        prompt = self._create_rejected_task_prompt(agency_state)
        reviewer_feedback = self._invoke_model(prompt)
        agency_state["messages"].append("Reviewer Feedback: " + reviewer_feedback["feedback"])
        return agency_state
    
    def _create_working_task_prompt(self, agency_state: AgencyStateSchema) -> dict:
        """Create a prompt for a working task."""
        return {
            "instructions": (
                "Read the messages and decide if any of them represent a completion "
                "of the task as per the guidelines. If it is complete then mark the task as "
                "complete by returning COMPLETED. If it is not complete, then return "
                "REJECTED, using the response format provided. Ensure that no control characters are included in the JSON."
            ),
            "task": agency_state["task"],
            "guidelines": agency_state["guidelines"],
            "messages": agency_state["messages"],
            "response format": "{\"status\": \"COMPLETED\" or \"REJECTED\"}",
        }

    def _create_completed_task_prompt(self, agency_state: AgencyStateSchema) -> dict:
        """Create a prompt for a completed task."""
        return {
            "instructions": (
                "Read the messages and select the message that represents a completion of "
                "the task as per your guidelines. Return the exact message as the accepted result "
                "using the response format provided. Ensure that no control characters are included in the JSON."
            ),
            "task": agency_state["task"],
            "guidelines": agency_state["guidelines"],
            "messages": agency_state["messages"],
            "response format": "{\"accepted_result\": \"Your accepted result here.\"}",
        }

    def _create_rejected_task_prompt(self, agency_state: AgencyStateSchema) -> dict:
        """Create a prompt for a rejected task."""
        return {
            "instructions": (
                "Read the messages and provide feedback on why the task was rejected. "
                "Use the response format provided. Ensure that no control characters are included in the JSON."
            ),
            "task": agency_state["task"],
            "guidelines": agency_state["guidelines"],
            "messages": agency_state["messages"],
            "response format": "{\"feedback\": \"Your feedback here.\"}",
        }
    
    def _invoke_model(self, prompt: dict) -> dict:
        """Invoke the model with the given prompt and return the response."""
        response = self.model.invoke(json.dumps(prompt)).content
        cleaned_response = self._strip_control_characters(response)
        return json.loads(cleaned_response)

    def _strip_control_characters(self, s: str) -> str:
        """Remove control characters from a string."""
        return "".join(ch for ch in s if unicodedata.category(ch) != "Cc")


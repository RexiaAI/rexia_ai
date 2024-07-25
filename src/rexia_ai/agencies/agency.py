"""Agency class for ReXia.AI"""

import json5
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from ..agents import Agent
from ..common import CollaborationChannel, Utility
from ..memory import WorkingMemory
from ..llms import RexiaAIOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Custom exceptions
class AgencyError(Exception):
    """Base exception for Agency-related errors."""
    pass

class AssignmentError(AgencyError):
    """Exception raised for errors in assignment creation or execution."""
    pass

@dataclass
class AgentInfo:
    """Dataclass to store information about an agent."""
    agent: Agent
    name: str
    description: str

@dataclass
class AgentAssignment:
    """Dataclass to store an agent's task assignment."""
    agent: Agent
    name: str
    task: str

class ManagerAgent:
    """ManagerAgent class for ReXia.AI. This agent manages the interactions between agents within an agency."""

    def __init__(self, agents: List[AgentInfo], manager_llm: RexiaAIOpenAI):
        """
        Initialize the ManagerAgent.

        Args:
            agents (List[AgentInfo]): List of available agents.
            manager_llm (RexiaAIOpenAI): Language model for the manager.
        """
        self.llm = manager_llm
        self.collaboration_channel = CollaborationChannel("Agent Collaboration")
        self.memory = WorkingMemory()
        self.agents = agents
        self.task = ""
        self.subtasks = []

    def assign_task(self, task: str) -> None:
        """
        Assign the main task to the manager.

        Args:
            task (str): The main task to be completed.
        """
        self.task = task
        self.memory.add_message(f"Main task: {task}")

    def manage_agents(self) -> None:
        """
        Manage the work of the various agents to iteratively complete the task.
        This method repeatedly asks the LLM for the next subtask or completion status.
        """
        try:
            # Generate all subtasks upfront
            self._generate_subtasks()

            # Execute all subtasks sequentially
            for subtask in self.subtasks:
                if subtask["status"] == "complete":
                    self.memory.add_message(f"Final summary: {subtask['summary']}")
                    break
                try:
                    self._execute_assignment(subtask["assignment"])
                except Exception as e:
                    self.collaboration_channel.put(f"Agent subtask failed: {str(e)}")
                    raise AgencyError(f"Error in managing agents: {str(e)}")
        except Exception as e:
            raise AgencyError(f"Error in managing agents: {str(e)}")

    def _generate_subtasks(self) -> None:
        """Generate all subtasks required to complete the main task."""
        agents_list = self._format_agents_list()
        memory_content = self.memory.get_messages_as_string()
        previous_results = self._get_all_previous_results()
        prompt = self._create_action_prompt(agents_list, previous_results, memory_content)
        
        try:
            response = self.llm.invoke(prompt)
            cleaned_response = self._clean_response(response)
            parsed_response = json5.loads(cleaned_response)
            self.subtasks = self._process_parsed_response(parsed_response)
            logging.info("Generated subtasks:")
            for idx, subtask in enumerate(self.subtasks, 1):
                logging.info(f"Subtask {idx}:")
                logging.info(f"  Completion: {subtask['completion']}")
                logging.info(f"  Agent: {subtask['assignment'].name}")
                logging.info(f"  Task: {subtask['assignment'].task}")
                logging.info("  Plan:")
                for step in subtask["Plan"]:
                    logging.info(f"    Step: {step['Step']}")
                    logging.info(f"    Status: {step['status']}")
        except Exception as e:
            logging.error(f"Failed to get a valid response from the model. Error: {str(e)}\n\nModel Response: {response}\n\nRetrying...")
            try:
                fix_errors_prompt = Utility.fix_json_errors_prompt(self, json_string=response, error=e)
                fixed_response = self.llm.invoke(fix_errors_prompt)
                cleaned_response = self._clean_response(fixed_response)
                self.subtasks = self._process_parsed_response(cleaned_response)
                logging.info("Generated subtasks:")
                for idx, subtask in enumerate(self.subtasks, 1):
                    logging.info(f"Subtask {idx}:")
                    logging.info(f"  Completion: {subtask['completion']}")
                    logging.info(f"  Agent: {subtask['assignment'].name}")
                    logging.info(f"  Task: {subtask['assignment'].task}")
                    logging.info("  Plan:")
                    for step in subtask["Plan"]:
                        logging.info(f"    Step: {step['Step']}")
                        logging.info(f"    Status: {step['status']}")
            except:
                logging.error("Failed to get a valid response from the model.")
                raise RuntimeError("Unable to get a valid response from the model.")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type(AgencyError),
        before_sleep=lambda retry_state: logger.info(
            f"Retrying present_results (attempt {retry_state.attempt_number})"
        ),
        reraise=True,
    )
    def present_results(self) -> str:
        """
        Present the results of the collaborative task execution.
        This method creates a prompt for the LLM to collate and summarize the results from the collaboration channel.

        Returns:
            str: A summarized report of the collaborative task execution.
        """
        try:
            messages = self.collaboration_channel.messages
            prompt = self._create_results_prompt(messages)
            report = self.llm.invoke(prompt)
            cleaned_report = Utility.remove_system_tokens(report)
            return cleaned_report
        except Exception as e:
            raise AgencyError(f"Error in presenting results: {str(e)}")

    def _create_results_prompt(self, messages: List[str]) -> str:
        """
        Create the prompt for presenting results.

        Args:
            messages (List[str]): List of messages from the collaboration channel.

        Returns:
            str: Formatted prompt for the LLM to generate the results report.
        """
        formatted_messages = self._format_messages(messages)
        return f"""
        You are tasked with presenting the complete results of a collaborative task execution.
        The main task was: "{self.task}"
        Below are the messages from the collaboration channel, representing the work done by various agents:
        {formatted_messages}
        Based on the above information, present the full and detailed results of the task. Do not describe the outcome; instead, provide the actual content of the deliverables, plans, strategies, or any other outputs produced. Include all relevant details, data, figures, and explanations that constitute the complete result of the task.
        Your response should be structured as follows:
        1. [Main Output Title]
        [Present the primary output or deliverable here in full detail]
        2. [Secondary Output Title (if applicable)]
        [Present any secondary outputs or deliverables]
        3. [Additional Components (if any)]
        [Include any other relevant components of the result]
        Ensure that you are presenting the actual content and not describing it. Provide all the specific details, numbers, plans, or any other concrete information that makes up the full result of the task.
        """

    def _format_messages(self, messages: List[str]) -> str:
        """
        Format the collaboration messages for inclusion in the prompt.

        Args:
            messages (List[str]): List of messages from the collaboration channel.

        Returns:
            str: Formatted string of messages.
        """
        return "\n".join([f"Message {i}:\n{message}\n" for i, message in enumerate(messages, 1)])

    def _format_agents_list(self) -> str:
        """Format the list of agents for the prompt."""
        return "\n".join(f"{i+1}. Name: {agent.name}\n Description: {agent.description}" for i, agent in enumerate(self.agents))

    def _process_parsed_response(self, parsed_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process the parsed LLM response and return the list of subtasks.
        
        Args:
            parsed_response (Dict[str, Any]): The parsed JSON response from the LLM.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the subtasks.
        
        Raises:
            AssignmentError: If no agent is found with the specified name.
            ValueError: If the status in the LLM response is invalid.
        """
        if parsed_response["status"] == "complete":
            return [{"status": "complete", "summary": parsed_response["summary"]}]
        
        subtasks = []
        for subtask in parsed_response["subtasks"]:
            agent_name = subtask["assignment"]["agent"]
            task_description = subtask["assignment"]["subtask"]
            agent_info = next((a for a in self.agents if a.name == agent_name), None)
            if agent_info is None:
                raise AssignmentError(f"No agent found with name: {agent_name}")
            assignment = AgentAssignment(agent=agent_info.agent, name=agent_name, task=task_description)
            subtasks.append({
                "status": "in_progress",
                "completion": subtask["completion"],
                "assignment": assignment,
                "Plan": subtask["Plan"]
            })
        return subtasks

    def _create_action_prompt(self, agents_list: str, task_log: str, memory_content: str) -> str:
        """
        Create the prompt for generating all subtasks.
        
        Args:
            agents_list (str): A formatted string listing all available agents and their descriptions.
            previous_results (str): A string containing the results of previously completed subtasks.
        
        Returns:
            str: A formatted prompt string for the LLM to generate all subtasks.
        """
        return f"""
        You are an AI task manager responsible for efficiently breaking down and managing a complex task. 
        Your goal is to generate a list of all subtasks required to complete the main task.

        Main Task: {self.task}

        Available AI Agents (Use only these): {agents_list}

        Previous Completed Subtask Results: {task_log}

        Previous Task Results: {memory_content}

        IMPORTANT GUIDELINES:
        1. Provide COMPLETE information in each subtask. Do NOT reference previous subtasks or information.
        2. Each subtask must be self-contained with ALL necessary context and details.
        3. NEVER use phrases like "as mentioned before" or "using the previous information".
        4. If a subtask requires information from a previous step, REPEAT that information in full.
        5. Create comprehensive subtasks that encompass multiple related actions when possible.
        6. Ensure subtasks relate to the plan and prioritize based on importance and dependencies.
        7. Be explicit and instructive. The agent must understand it needs to perform the work, not describe it.
        8. If a previous subtask result is unsatisfactory, try a different approach or agent.

        Example of a GOOD subtask:
        "Implement the Snake class for the Snake game with the following specifications:
        1. Attributes: position (list of coordinates), direction (UP, DOWN, LEFT, RIGHT), length (initial value: 3)
        2. Methods:
           a. move(): Update snake's position based on current direction
           b. grow(): Increase snake's length when it eats food
           c. check_collision(): Detect collisions with self or game boundaries
        3. Game board size: 20x20 grid
        Provide complete Python code with proper documentation."

        Example of a BAD subtask:
        "Implement the Snake class as discussed earlier, with the previously mentioned attributes and methods."

        Generate a list of subtasks in the following JSON format:
        {{
            "status": "in_progress",
            "subtasks": [
                {{
                    "completion": "completion percentage (e.g. 75%)",
                    "assignment": {{
                        "agent": "Agent name",
                        "subtask": "Comprehensive task description with ALL necessary context and information."
                    }},
                    "Plan": [
                        {{
                            "Step": "Detailed step description",
                            "status": "pending, in_progress, or completed"
                        }},
                        // ... more steps as needed
                    ]
                }},
                // ... more subtasks as needed
            ]
        }}

        If the task is complete, use this JSON format:
        {{
            "status": "complete",
            "completion": "100%",
            "summary": "Detailed summary of the completed task and its results"
        }}

        Your response must be in valid JSON format as specified above. Include nothing outside the JSON.
        """

    def _execute_assignment(self, assignment: AgentAssignment) -> None:
        """
        Execute a single agent assignment.

        Args:
            assignment (AgentAssignment): The assignment to execute.

        Raises:
            AgencyError: If there's an error in executing the assignment.
        """
        try:
            task_with_context = (
                assignment.task + "\n\nAdditional Context: " + "\n\n".join(self.collaboration_channel.messages)
            )
            result = assignment.agent.invoke(task_with_context)
            summary = (
                "Subtask: " + assignment.task + "\n\nAgent Assigned: " + assignment.name + "\n\nAgent Result: " + str(result)
            )
            logging.info(summary)
            self.collaboration_channel.put(summary)
        except Exception as e:
            error_message = f"Failed task: {assignment.task}\nError: Failed to execute assignment for agent {assignment.name}: {str(e)}"
            self.collaboration_channel.put(
                error_message + "\n\nAgent messages:" + "\n".join(assignment.agent.workflow.channel.messages)
            )
            raise AssignmentError(error_message)

    def _get_all_previous_results(self) -> str:
        """
        Get all previous task execution results for the manager.

        Returns:
            str: Summarized previous results.
        """
        if not self.collaboration_channel.messages:
            return "No previous results."
        return "\n\n".join(self.collaboration_channel.messages)

    def _clean_response(self, response: str) -> str:
        """
        Clean the response from the model.

        Args:
            response: The response from the model.

        Returns:
            The cleaned response.
        """
        cleaned_response = Utility.extract_json_string(response)
        cleaned_response = Utility.fix_json_errors(cleaned_response)
        return cleaned_response

class Agency:
    """Agency class for ReXia.AI. An agency represents a group of autonomous agents capable of working together on complex tasks."""

    def __init__(self, task: str, agents: List[AgentInfo], manager_llm: RexiaAIOpenAI):
        """
        Initialize the Agency.

        Args:
            task (str): The main task to be completed.
            agents (List[AgentInfo]): List of available agents.
            manager_llm (RexiaAIOpenAI): Language model for the manager.
        """
        self.task = task
        self.manager = ManagerAgent(agents, manager_llm)

    def invoke(self, task: str = None) -> str:
        """
        Start the collaborative task execution.

        Args:
            task (str, optional): A new task to override the initial task.

        Returns:
            str: Results of the collaborative task execution.

        Raises:
            AgencyError: If there's an error during task execution.
        """
        try:
            if task:
                self.task = task
            logging.info(f"ReXia.AI Agency working on task: {self.task}")
            self.manager.assign_task(self.task)
            self.manager.manage_agents()
            return self.manager.present_results()
        except AgencyError as e:
            logging.error(f"Error in agency execution: {str(e)}. Retrying...")
            raise  # Re-raise the exception to trigger the retry
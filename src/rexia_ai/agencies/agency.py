"""Agency class for ReXia.AI"""

import json5
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from ..agents import Agent
from ..common import CollaborationChannel, Utility
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

    def manage_agents(self) -> None:
        """
        Manage the work of the various agents to iteratively complete the task.
        """
        try:
            # Generate all subtasks upfront
            self._generate_subtasks()

            # Execute all subtasks sequentially
            for subtask in self.subtasks:
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
        prompt = self._create_action_prompt(agents_list)

        try:
            response = self.llm.invoke(prompt)
            cleaned_response = self._clean_response(response)
            parsed_response = json5.loads(cleaned_response)
            self.subtasks = self._process_parsed_response(parsed_response)
            logging.info("Generated subtasks:")
            for idx, subtask in enumerate(self.subtasks, 1):
                logging.info(f"Subtask {idx}:")
                logging.info(f"  Agent: {subtask['assignment'].name}")
                logging.info(f"  Task: {subtask['assignment'].task}")
        except Exception as e:
            logging.error(f"Failed to get a valid response from the model. Error: {e}")

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
        ## Task Finalization

        You are an expert analyst tasked with using the work of your team of agents to complete a task.

        ### Original Task
        "{self.task}"

        ### Collaboration Data
        Below are the messages from the collaboration channel, representing the work done by various agents:

        {formatted_messages}

        ### Your Responsibilities
        1. Thoroughly analyze all messages from the collaboration channel.
        2. Synthesise the information to create a comprehensive answer to the original task.
        3. Ensure all aspects of the task are addressed in your response.
        4. Present your findings in a clear, logical, and well-structured manner.
        5. Include relevant data, analysis, and conclusions from the collaboration.
        6. Highlight key insights or important discoveries.
        7. Address any limitations or uncertainties in the results, if applicable.
        8. Provide a completion of the task, this means you must provide the full
        answer building on the previous work, not a description of what has been done.
        9. Make use all the work of your agents in the collaboration chat. Your response
        should be a synthesis of all of this information.

        ### Output Format
        Your response should be detailed, professional, and directly answer the original task.
        Use appropriate headings, bullet points, or numbered lists to organize information clearly.
        """

    def _format_messages(self, messages: List[str]) -> str:
        """
        Format the collaboration messages for inclusion in the prompt.

        Args:
            messages (List[str]): List of messages from the collaboration channel.

        Returns:
            str: Formatted string of messages.
        """
        formatted_messages = "\n".join(
            [f"Message {i}:\n{message}\n" for i, message in enumerate(messages, 1)]
        )
        return formatted_messages

    def _format_agents_list(self) -> str:
        """Format the list of agents for the prompt."""
        return "\n".join(
            f"{i+1}. Name: {agent.name}\n Description: {agent.description}"
            for i, agent in enumerate(self.agents)
        )

    def _process_parsed_response(
        self, parsed_response: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
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
        subtasks = []
        for subtask in parsed_response["subtasks"]:
            agent_name = subtask["assignment"]["agent"]
            task_description = subtask["assignment"]["subtask"]
            agent_info = next((a for a in self.agents if a.name == agent_name), None)
            if agent_info is None:
                raise AssignmentError(f"No agent found with name: {agent_name}")
            assignment = AgentAssignment(
                agent=agent_info.agent, name=agent_name, task=task_description
            )
            subtasks.append(
                {
                    "assignment": assignment,
                }
            )
        return subtasks

    def _create_action_prompt(self, agents_list: str) -> str:
        """
        Create the prompt for generating all subtasks.

        Args:
            agents_list (str): A formatted string listing all available agents and their descriptions.
            memory_content (str): A string containing the results of previously completed tasks.
        Returns:
            str: A formatted prompt string for the LLM to generate all subtasks.
        """
        return f"""
        You are an expert AI task manager responsible for efficiently breaking down and managing a complex task. 
        Your goal is to generate a comprehensive list of all subtasks required to complete the main task.

        ### Main Task
        {self.task}

        ### Available AI Agents
        Use only these agents for task assignments:
        {agents_list}

        ### Critical Guidelines
        1. Provide COMPLETE information in each subtask. Do NOT reference previous subtasks or information.
        2. Each subtask must be self-contained with ALL necessary context and details.
        3. Be explicit and instructive. The agent must understand it needs to perform the work, not describe it.
        4. If you want code, specify the language required for the code.
        5. Each subtask should read as a prompt, using best practice prompting techniques, to instruct an AI
        agent to complete the subtask exactly as required.
        6. Ensure logical progression and dependencies between subtasks.
        7. Assign subtasks to the most appropriate agent based on their capabilities.

        ### Output Format

        Generate a list of subtasks in the following JSON format:
        {{
            "subtasks": [
                {{
                    "assignment": {{
                        "agent": "Agent name",
                        "subtask": "Comprehensive task description with ALL necessary context and information."
                    }},
                }},
                // ... more subtasks as needed
            ]
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
            result = assignment.agent.invoke(assignment.task)
            summary = (
                "Subtask: "
                + assignment.task
                + "\n\nAgent Assigned: "
                + assignment.name
                + "\n\nAgent Result: "
                + str(result)
            )
            logging.info(summary)
            self.collaboration_channel.put(summary)
        except Exception as e:
            error_message = f"Failed task: {assignment.task}\nError: Failed to execute assignment for agent {assignment.name}: {str(e)}"
            self.collaboration_channel.put(
                error_message
                + "\n\nAgent messages:"
                + "\n".join(assignment.agent.workflow.channel.messages)
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

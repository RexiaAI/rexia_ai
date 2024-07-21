""" Agency module for ReXia.AI. This module defines the Agency class, which represents a group of autonomous agents that work together under a manager to complete complex tasks. """

import json5
from typing import List, Dict, Any
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from ..agents import Agent
from ..common import CollaborationChannel, Utility
from ..memory import WorkingMemory
from ..llms import RexiaAIOpenAI


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
    """
    ManagerAgent class for ReXia.AI.
    This agent manages the interactions between agents within an agency.
    It's responsible for task breakdown, assignment, and coordination.
    """

    def __init__(
        self, agents: List[AgentInfo], manager_llm: RexiaAIOpenAI
    ):
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
            while True:
                next_action = self._get_next_action()
                if next_action["status"] == "complete":
                    self.memory.add_message(
                        f"Final summary: {next_action['summary']}"
                    )
                    break
                try:
                    self._execute_assignment(next_action["assignment"])
                except Exception as e:
                    self.collaboration_channel.put(
                            f"Agent subtask failed: {str(e)}"
                        )
                    raise AgencyError(f"Error in managing agents: {str(e)}")
        except Exception as e:
                raise AgencyError(f"Error in managing agents: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type((AgencyError)),
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

        Based on the above information, present the full and detailed results of the task.
        Do not describe the outcome; instead, provide the actual content of the deliverables, plans, strategies, or any other outputs produced.
        Include all relevant details, data, figures, and explanations that constitute the complete result of the task.

        Your response should be structured as follows:

        1. [Main Output Title]
        [Present the primary output or deliverable here in full detail]

        2. [Secondary Output Title (if applicable)]
        [Present any secondary outputs or deliverables]

        3. [Additional Components (if any)]
        [Include any other relevant components of the result]

        Ensure that you are presenting the actual content and not describing it.
        Provide all the specific details, numbers, plans, or any other concrete information that makes up the full result of the task.
        """

    def _format_messages(self, messages: List[str]) -> str:
        """
        Format the collaboration messages for inclusion in the prompt.

        Args:
            messages (List[str]): List of messages from the collaboration channel.

        Returns:
            str: Formatted string of messages.
        """
        return "\n".join(
            [f"Message {i}:\n{message}\n" for i, message in enumerate(messages, 1)]
        )

    def _format_agents_list(self) -> str:
        """Format the list of agents for the prompt."""
        return "\n".join(
            f"{i+1}. Name: {agent.name}\n   Description: {agent.description}"
            for i, agent in enumerate(self.agents)
        )

    def _get_next_action(self) -> Dict[str, Any]:
        """
        Ask the LLM to decide on the next action: either a new subtask or task completion.
        Retry with feedback if the response is not usable.

        Returns:
            Dict[str, Any]: A dictionary containing the status and assignment (if applicable).
        """
        agents_list = self._format_agents_list()
        memory_content = self.memory.get_messages_as_string()
        previous_results = self._get_all_previous_results()
        prompt = self._create_action_prompt(
            agents_list, previous_results, memory_content
        )

        try:
            response = self.llm.invoke(prompt)
            cleaned_response = self._clean_response(response)
            parsed_response = json5.loads(cleaned_response)
            return self._process_parsed_response(parsed_response)
        except Exception as e:
            print(
                f"Failed to get a valid response from the model. "
                f"Error: {str(e)}\n\nModel "
                f"Response: {response}\n\nRetrying..."
            )
            try:
                fixed_response = Utility.fix_json_errors_llm(
                    self, json_string=response, error=e, llm=self.llm
                )
            except:
                print("Failed to get a valid response from the model.")
                raise RuntimeError("Unable to get a valid response from the model.")
            return self._process_parsed_response(fixed_response)

    def _process_parsed_response(
        self, parsed_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process the parsed LLM response and return the appropriate action.

        Args:
            parsed_response (Dict[str, Any]): The parsed JSON response from the LLM.

        Returns:
            Dict[str, Any]: A dictionary containing either:
            - For in-progress tasks: {"status": "in_progress", "assignment": AgentAssignment}
            - For completed tasks: {"status": "complete", "summary": str}

        Raises:
            AssignmentError: If no agent is found with the specified name.
            ValueError: If the status in the LLM response is invalid.
        """
        if parsed_response["status"] == "in_progress":
            agent_name = parsed_response["assignment"]["agent"]
            task = parsed_response["assignment"]["task"]
            agent_info = next((a for a in self.agents if a.name == agent_name), None)
            if agent_info is None:
                raise AssignmentError(f"No agent found with name: {agent_name}")
            assignment = AgentAssignment(
                agent=agent_info.agent, name=agent_name, task=task
            )
            return {"status": "in_progress", "assignment": assignment}
        elif parsed_response["status"] == "complete":
            return {"status": "complete", "summary": parsed_response["summary"]}
        else:
            raise ValueError(
                f"Invalid status in LLM response: {parsed_response['status']}"
            )

    def _create_action_prompt(
        self, agents_list: str, task_log: str, memory_content: str
    ) -> str:
        """
        Create the prompt for the next action decision.

        Args:
            agents_list (str): A formatted string listing all available agents and their descriptions.
            previous_results (str): A string containing the results of previously completed subtasks.

        Returns:
            str: A formatted prompt string for the LLM to make the next action decision.
        """
        return f"""
        You are an AI task manager responsible for breaking down and managing a complex task.
        Your goal is to determine the next step in completing the task or to decide if the task is complete.

        Main Task: {self.task}

        Available AI Agents:
        {agents_list}

        Task Log:
        {task_log}

        Previous Completed Subtask Summaries:
        {memory_content}

        Based on the main task, available AI agents, and previous completed subtask summaries, please decide on one of the following:
        1. Assign a new subtask to an AI agent
        2. Declare the task as complete

        Provide any relevant information the AI agent will need to complete their subtask as part of the task,
        this includes information generated by previous agents or any other relevant information.
        Provide the agent with context for it's subtask.
        The AI Agents cannot see the subtask summaries, so if they need information from the subtask summaries to complete the task, provide it with the task.
        Avoid repeating subtasks that have successfully comleted.
        A subtask should be composed of a single action. For instance 'check exchange rates', 'find the capital of France', 'calculate 147 * 276', 'plan a day out'.
        If a subtask has failed (for instance there was an error) decide whether to repeat it or try a different approach.
        Do not assign subtasks to agents that require interacting with outside sources unless they explicitly are described as having that capability.
        For instance, do not ask an agent to book a hotel room, or purchase an item unless they are described as being able to do this.
        Do not create subtasks that require things an AI agent cannot do, such as physically interact with the world or speak.
        Your primary goal is to manage the completion of the task as efficiently as possible.

        If assigning a new subtask, provide your response in the following JSON format:
        {{
            "status": "in_progress",
            "assignment": {{
                "agent": "Agent's name",
                "task": "Description of the subtask assigned to this agent"
            }}
        }}

        If the task is complete, provide your response in the following JSON format:
        {{
            "status": "complete",
            "summary": "Brief summary of the completed task and its results"
        }}

        Ensure that your decision is based on the progress made and the remaining work to be done.
        Your response must be in valid JSON format as specified above.
        Include nothing outside the valid JSON format as specified above.
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
            result_summary = self._summarise_results(result)
            cleaned_summary = Utility.remove_system_tokens(result_summary)
            cleaned_summary = (
                "Subtask: "
                + assignment.task
                + "\n\nAgent Assigned: "
                + assignment.name
                + "\n\nAgent Result: "
                + str(cleaned_summary)
            )
            print(cleaned_summary)
            self.collaboration_channel.put(cleaned_summary)
        except Exception as e:
            error_message = f"Failed task: {assignment.task}\nError: Failed to execute assignment for agent {assignment.name}: {str(e)}"
            self.collaboration_channel.put(
                error_message
                + "\n\nAgent messages:"
                + "\n".join(assignment.agent.workflow.channel.messages)
            )
            raise AssignmentError(error_message)
                
    def _summarise_results(self, results: str):
        """
        Summarises the results of the previous execution

        Returns:
            results: Execution results
        """
        
        summarisation_prompt="""
        Task Progress Summary Guidelines:
            Your role: 
                AI assistant tasked with providing concise, up-to-date summaries of subtask results.
            
            Objective: 
                Extract and condense the information.
            
            Output format:
                Subtask Summary:
                    Summarise the results of the subtask.
            
            Guidelines:
                Use clear, concise language suitable for quick reference
            
            Subtask Result:
        """
        summarisation = self.llm.invoke(summarisation_prompt + "\n\n" + str(results))
        
        return summarisation

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
    """
    Agency class for ReXia.AI.
    An agency represents a group of autonomous agents capable of working together on complex tasks.
    """

    def __init__(
        self,
        task: str,
        agents: List[AgentInfo],
        manager_llm: RexiaAIOpenAI,
    ):
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
            print(f"ReXia.AI Agency working on task: {self.task}")
            self.manager.assign_task(self.task)
            self.manager.manage_agents()
            return self.manager.present_results()
        except AgencyError as e:
            print(f"Error in agency execution: {str(e)}. Retrying...")
            raise  # Re-raise the exception to trigger the retry

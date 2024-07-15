"""
Agency module for ReXia.AI.

This module defines the Agency class, which represents a group of autonomous agents
that work together under a manager to complete complex tasks.
"""

import json
from typing import List, Dict, Any
from dataclasses import dataclass
from ..agents import Agent
from ..common import CollaborationChannel
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

    def manage_agents(self) -> None:
        """
        Manage the work of the various agents to successfully complete the task.

        This method breaks down the main task, assigns subtasks to agents,
        and coordinates their execution.
        """
        try:
            agents_list = self._format_agents_list()
            assignment_prompt = self._create_assignment_prompt(agents_list)
            llm_response = self.llm.invoke(assignment_prompt)
            assignments = self._create_assignments(llm_response)

            for assignment in assignments:
                self._execute_assignment(assignment)

        except Exception as e:
            raise AgencyError(f"Error in managing agents: {str(e)}")

    def present_results(self) -> str:
        """
        Present the results of the collaborative task execution.

        This method creates a prompt for the LLM to collate and summarize the results
        from the collaboration channel.

        Returns:
            str: A summarized report of the collaborative task execution.
        """
        messages = self.collaboration_channel.messages
        
        prompt = f"""
        You are tasked with collating and reporting the results of a collaborative task execution.
        The main task was: "{self.task}"

        Below are the messages from the collaboration channel, representing the work done by various agents:

        {self._format_messages(messages)}

        Please provide a comprehensive summary of the results, addressing the following points:
        1. A brief overview of the main task and how it was approached.
        2. Key findings or decisions made during the execution.
        3. The final outcome or solution to the main task.
        4. Any additional insights or recommendations based on the collaborative work.

        Your report should be clear, concise, and well-structured. Aim to capture the essence of the collaborative effort and its results.
        """

        # Use the LLM to generate the summary report
        report = self.llm.invoke(prompt)
        
        return report

    def _format_messages(self, messages: List[str]) -> str:
        """
        Format the collaboration messages for inclusion in the prompt.

        Args:
            messages (List[str]): List of messages from the collaboration channel.

        Returns:
            str: Formatted string of messages.
        """
        formatted_messages = []
        for i, message in enumerate(messages, 1):
            formatted_messages.append(f"Message {i}:\n{message}\n")
        
        return "\n".join(formatted_messages)

    def _format_agents_list(self) -> str:
        """Format the list of agents for the prompt."""
        return "\n".join(
            [f"{i+1}. Name: {agent.name}\n   Description: {agent.description}"
             for i, agent in enumerate(self.agents)]
        )

    def _create_assignment_prompt(self, agents_list: str) -> str:
        """Create the prompt for task assignment."""
        return f"""
        You are an AI task manager responsible for breaking down complex tasks into subtasks
        and assigning them to the most suitable AI agents. 
        Your goal is to optimise task completion by matching subtasks to agent capabilities.
        Only use the agents listed below for assignment. Do not create new agents or make up capabilities.
        All tasks should be something that can be completed by the AI agents provided based on their descriptions.
        No tasks should require physical interaction or manual labor.
        No tasks should require human interaction beyond providing initial instructions.
        All tasks should be phrased as an instruction for an AI agent.
        Tasks will be executed in sequence as they are assigned.
        Agents will have access to the result of the agent that executed before them.
        Order the agents and their tasks accordingly.

        Main Task: {self.task}

        Available Agents:
        {agents_list}

        Instructions:
        1. Analyze the main task and break it down into subtasks.
        2. For each subtask, provide a brief description and identify which agent would be best suited to
        complete it based on their capabilities.
        3. Ensure that all aspects of the main task are covered by the subtasks.
        4. If a subtask doesn't clearly match any agent's capabilities, assign it to the agent with the most relevant skills.

        Please provide your response in the following JSON format:

        {{
        "assignments": [
            {{
            "agent": "Agent's name",
            "task": "Description of the subtask assigned to this agent"
            }},
            ...
        ],
        "summary": "Brief overview of how the subtasks collectively address the main task"
        }}
        """

    def _create_assignments(self, llm_response: str) -> List[AgentAssignment]:
        """
        Create assignments for agents based on the LLM response.

        Args:
            llm_response (str): JSON string response from the LLM.

        Returns:
            List[AgentAssignment]: List of agent assignments.

        Raises:
            AssignmentError: If there's an error in creating assignments.
        """
        try:
            parsed_response = json.loads(llm_response)
            assignments = parsed_response.get('assignments', [])

            agent_assignments = []
            for assignment in assignments:
                agent_name = assignment.get('agent')
                task = assignment.get('task')

                agent_info = next((a for a in self.agents if a.name == agent_name), None)
                if agent_info is None:
                    raise AssignmentError(f"No agent found with name: {agent_name}")

                if not hasattr(agent_info.agent, 'invoke'):
                    raise AssignmentError(f"Agent {agent_name} does not have an 'invoke' method. Agent type: {type(agent_info.agent)}")

                agent_assignment = AgentAssignment(agent=agent_info.agent, name=agent_name, task=task)
                agent_assignments.append(agent_assignment)

            return agent_assignments

        except json.JSONDecodeError as json_err:
            raise AssignmentError(f"Failed to parse LLM response as JSON: {json_err}")
        except KeyError as key_err:
            raise AssignmentError(f"Missing key in LLM response or assignment: {key_err}")
        except Exception as e:
            raise AssignmentError(f"Unexpected error creating assignments: {str(e)}")

    def _execute_assignment(self, assignment: AgentAssignment) -> None:
        """
        Execute a single agent assignment.

        Args:
            assignment (AgentAssignment): The assignment to execute.

        Raises:
            AgencyError: If there's an error in executing the assignment.
        """
        try:
            previous_task_results = self._get_previous_results()
            task_with_context = f"{assignment.task}\n\nPrevious Task Results: {previous_task_results}"
            
            result = assignment.agent.invoke(task_with_context)
            self.collaboration_channel.put(result)
        except Exception as e:
            raise AgencyError(f"Error executing assignment for agent {assignment.name}: {str(e)}")

    def _get_previous_results(self) -> str:
        """Get the results of the previous task execution."""
        return self.collaboration_channel.messages[-1] if self.collaboration_channel.messages else ""

class Agency:
    """
    Agency class for ReXia.AI.

    An agency represents a group of autonomous agents capable of working together on complex tasks.
    """

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

    def invoke(self, task: str = None) -> List[str]:
        """
        Start the collaborative task execution.

        Args:
            task (str, optional): A new task to override the initial task.

        Returns:
            List[str]: Results of the collaborative task execution.

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
        except Exception as e:
            raise AgencyError(f"Error in agency execution: {str(e)}")
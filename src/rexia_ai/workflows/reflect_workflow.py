"""Reflect workflow for ReXia.AI."""

import traceback
from ..base import BaseWorkflow, BaseMemory
from ..common import CollaborationChannel, TaskStatus
from ..agents import Component
from ..agents.workers import PlanWorker, FinaliseWorker, Worker, ToolWorker
from ..llms import RexiaAIOpenAI


class ReflectWorkflow(BaseWorkflow):
    """
    ReflectWorkflow Class for ReXia AI, refactored for better design principles.

    Attributes:
        llm: The language model used by the workflow.
        task: The task that the workflow is designed to perform.
        verbose: A flag used for enabling verbose mode.
        memory: The memory component of the workflow.
        channel: The collaboration channel for the workflow.
        plan: The plan component of the workflow.
        tool: The tool component of the workflow.
        work: The work component of the workflow.
        finalise: The finalise component of the workflow.
    """
    llm: RexiaAIOpenAI
    task: str
    verbose: bool
    memory: BaseMemory
    channel: CollaborationChannel
    plan: Component
    tool: Component
    work: Component
    finalise: Component
    
    def __init__(self, llm: RexiaAIOpenAI, task: str, memory: BaseMemory, verbose: bool = False) -> None:
        super().__init__(llm, task, verbose)
        self.channel = CollaborationChannel(task)
        self.memory = memory
        self.plan = Component("plan", self.channel, PlanWorker(model=llm, verbose=verbose), memory=self.memory)
        self.tool = Component("tool", self.channel, ToolWorker(model=llm, verbose=verbose), memory=self.memory)
        self.work = Component("work", self.channel, Worker(model=llm, verbose=verbose), memory=self.memory)
        self.finalise = Component("finalise", self.channel, FinaliseWorker(model=llm, verbose=verbose), memory=self.memory)
        
    def _run_task(self):
        """Run the agent process."""
        try:
            print(f"ReXia.AI is working on the task: {self.channel.task}")

            self.channel.status = TaskStatus.WORKING
            self.plan.run()
            
            if self.llm.tools:
                self.tool.run()
            self.work.run()
            
            self.finalise.run()
            
            self.channel.status = TaskStatus.COMPLETED
            
            # Add the final message to the memory
            self.memory.add_message(self.channel.messages[-1])

            print(f"ReXia.AI has completed the task: {self.channel.task}")
        except Exception as e:
            print(f"An error occurred while running the task: {e}")
            print(traceback.format_exc())
        
    def run(self):
        """Run the agent."""
        self._run_task()
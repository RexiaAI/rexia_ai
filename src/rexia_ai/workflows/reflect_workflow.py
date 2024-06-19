"""Reflect workflow for ReXia.AI."""

from ..base import BaseWorkflow
from ..common import CollaborationChannel, TaskStatus
from ..agents import Component
from ..agents.workers import PlanWorker, FinaliseWorker, Worker, ToolWorker
from ..llms import RexiaAIOpenAI


class ReflectWorkflow(BaseWorkflow):
    """
    ReflectWorkflow Class for ReXia AI, refactored for better design principles.

    Attributes:
        channel: The collaboration channel for the workflow.
        plan: The plan component of the workflow.
        tool: The tool component of the workflow.
        work: The work component of the workflow.
        finalise: The finalise component of the workflow.
    """
    def __init__(self, llm: RexiaAIOpenAI, task: str, verbose: bool = False) -> None:
        super().__init__(llm, task, verbose)
        self.channel = CollaborationChannel(task)
        self.plan = Component("plan", self.channel, PlanWorker(model=llm, verbose=verbose))
        self.tool = Component("tool", self.channel, ToolWorker(model=llm, verbose=verbose))
        self.work = Component("work", self.channel, Worker(model=llm, verbose=verbose))
        self.finalise = Component("finalise", self.channel, FinaliseWorker(model=llm, verbose=verbose))
        
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

            print(f"ReXia.AI has completed the task: {self.channel.task}")
        except Exception as e:
            print(f"An error occurred while running the task: {e}")
    
    def run(self):
        """Run the agent."""
        self._run_task()
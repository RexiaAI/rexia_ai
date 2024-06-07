"""reflect workflow for ReXia AI."""
from typing import Any
from ..base import BaseWorkflow
from ..common import CollaborationChannel, TaskStatus
from ..agents import ReXiaAIAgent
from ..agents.workers.reflection import PlanWorker, ReflectWorker
from ..agents.workers.common import Worker, ApproveWorker, ToolWorker


class ReflectWorkflow(BaseWorkflow):
    """ReflectWorkflow Class for ReXia AI, refactored for better design principles."""
    def __init__(self, llm: Any, task: str, verbose: bool) -> None:
        super().__init__(llm, task, verbose)
        self.channel = CollaborationChannel(task)
        self.plan = ReXiaAIAgent("plan", self.channel, PlanWorker(model=llm, verbose=verbose))
        self.tool = ReXiaAIAgent("tool", self.channel, ToolWorker(model=llm, verbose=verbose))
        self.work = ReXiaAIAgent("work", self.channel, Worker(model=llm, verbose=verbose))
        self.reflect = ReXiaAIAgent("reflect", self.channel, ReflectWorker(model=llm, verbose=verbose))
        self.approval = ReXiaAIAgent("approval", self.channel, ApproveWorker(model=llm, verbose=verbose))
        
    def _run_task(self):
        """Run the agent process."""

        print("ReXia.AI is working on the task: " + self.channel.task)

        self.plan.run()
        while self.channel.status != TaskStatus.COMPLETED:
            self.channel.status = TaskStatus.WORKING
            self.tool.run()
            self.work.run()
            self.reflect.run()
            self.approval.run()
            if "COMPLETED" in self.channel.messages[-1]:
                self.channel.status = TaskStatus.COMPLETED

        print("ReXia.AI has completed the task: " + self.channel.task)
        if self.verbose:
            print("Task result: " + self.channel.messages[-1])
    
    def run(self):
        """Run the agent."""
        self._run_task()
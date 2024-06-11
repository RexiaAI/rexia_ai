"""reflect workflow for ReXia AI."""

from ..base import BaseWorkflow
from ..common import CollaborationChannel, TaskStatus
from ..agents import Component
from ..agents.workers import PlanWorker, ReflectWorker
from ..agents.workers import Worker, ApproveWorker, ToolWorker
from ..llms import LLM


class ReflectWorkflow(BaseWorkflow):
    """ReflectWorkflow Class for ReXia AI, refactored for better design principles."""
    def __init__(self, llm: LLM, task: str, verbose: bool) -> None:
        super().__init__(llm, task, verbose)
        self.channel = CollaborationChannel(task)
        self.plan = Component("plan", self.channel, PlanWorker(model=llm, verbose=verbose))
        self.tool = Component("tool", self.channel, ToolWorker(model=llm, verbose=verbose))
        self.work = Component("work", self.channel, Worker(model=llm, verbose=verbose))
        self.reflect = Component("reflect", self.channel, ReflectWorker(model=llm, verbose=verbose))
        self.approval = Component("approval", self.channel, ApproveWorker(model=llm, verbose=verbose))
        
    def _run_task(self):
        """Run the agent process."""

        print("ReXia.AI is working on the task: " + self.channel.task)

        self.plan.run()
        counter = 0
        while self.channel.status != TaskStatus.COMPLETED and counter < 3:
            self.channel.status = TaskStatus.WORKING
            if self.llm.tools != {}:
                self.tool.run()
            self.work.run()
            self.reflect.run()
            self.approval.run()
            if "COMPLETED" in self.channel.messages[-1]:
                self.channel.status = TaskStatus.COMPLETED
            counter += 1

        print("ReXia.AI has completed the task: " + self.channel.task)
        if self.verbose:
            print("Task result: " + self.channel.messages[-1])
    
    def run(self):
        """Run the agent."""
        self._run_task()
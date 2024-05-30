"""Collaborative Workflow for ReXia AI."""

import re
from ..base import BaseWorkflow
from ..common import CollaborationChannel, TaskStatus
from ..agents import PlanWorker, Worker, ReflectWorker, ReXiaAIAgent, TaskWorker, ApproveWorker


class CollaborativeWorkflow(BaseWorkflow):
    """CollaborativeWorkflow Class for ReXia AI, refactored for better design principles."""
    def __init__(self, goal: str, llm) -> None:
        super().__init__()
        self.channel = CollaborationChannel(goal)
        self.plan = ReXiaAIAgent("plan", self.channel, PlanWorker(model=llm, verbose=True))
        self.work = ReXiaAIAgent("work", self.channel, Worker(model=llm, verbose=True))
        self.reflect = ReXiaAIAgent("reflect", self.channel, ReflectWorker(model=llm, verbose=True))
        self.task = ReXiaAIAgent("task", self.channel, TaskWorker(model=llm, verbose=True))
        self.approval = ReXiaAIAgent("approval", self.channel, ApproveWorker(model=llm, verbose=True))
        self.goal = goal
        self.tasks = []

    def _run_task(self):
        """Run the agent process."""

        print("ReXia.AI is working on the task: " + self.channel.get_task())

        self.plan.run()
        self.work.run()
        self.reflect.run()

        print("ReXia.AI has completed the task: " + self.channel.get_task())
        print("Task result: " + self.channel.get_messages()[-1])
    
    def _decide_tasks(self):
        """Decide the tasks for the agents."""
        self.tasks = self.extract_tasks(self.channel.get_tasks())
    
    def extract_tasks(self, list_of_tasks):
        """Extract the tasks from the channel."""
        subtasks = re.findall(r'<sub-task>(.*?)</sub-task>', list_of_tasks)
        
        tasks_with_status = [{'task': subtask, 'status': TaskStatus.PENDING} for subtask in subtasks]
        
        return tasks_with_status
    
    def run(self):
        """Run the agent."""
        self._run_task()
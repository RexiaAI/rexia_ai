"""task breakdown workflow for ReXia AI."""

import re
from ..base import BaseWorkflow
from ..common import CollaborationChannel, TaskStatus
from ..agents import ReXiaAIAgent
from ..agents.workers.task_planning import TaskPlanningWorker


class TaskBreakdownWorkflow(BaseWorkflow):
    """CollaborativeWorkflow Class for ReXia AI, refactored for better design principles."""
    def __init__(self, goal: str, llm) -> None:
        super().__init__()
        self.channel = CollaborationChannel(goal)
        self.task = ReXiaAIAgent("task", self.channel, TaskPlanningWorker(model=llm, verbose=True))
        self.goal = goal
        self.tasks = []

    def _run_task(self):
        """Run the agent process."""

        print("ReXia.AI is working on the task: " + self.channel.task)

        self.task.run()

        print("ReXia.AI has completed the task: " + self.channel.task)
        print("Task result: " + self.channel.messages[-1])
    
    def extract_tasks(self, list_of_tasks):
        """Extract the tasks from the channel."""
        subtasks = re.findall(r'<sub-task>(.*?)</sub-task>', list_of_tasks)
        
        tasks_with_status = [{'task': subtask, 'status': TaskStatus.PENDING} for subtask in subtasks]
        
        return tasks_with_status
    
    def run(self):
        """Run the agent."""
        self._run_task()
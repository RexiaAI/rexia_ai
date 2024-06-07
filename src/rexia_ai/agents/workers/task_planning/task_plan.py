"""TaskPlanningWorker class for ReXia.AI."""

from typing import Any
from ....base import BaseWorker


class TaskPlanningWorker(BaseWorker):
    """A worker agent for breaking a main task into many sub-tasks."""

    model: Any

    def __init__(
        self,
        model: Any,
        verbose: bool = False,
    ):
        super().__init__(model, verbose=verbose)

    def create_prompt(self, task, messages) -> str:
        """Create a prompt for the model."""
        prompt = (
            """
                You:
                    You are a task agent.
                    You are part of a team working on a task.
                    Your job is to read the task and break it down into sub-tasks.
                
                Do:
                    All tasks should be relevant to the main task.
                    Make sure to include all the necessary sub-tasks to complete the main task.
                    The result of following the sub-tasks should be a completion of the main task.
                    You should output sub-tasks in this format: <sub-task>Task information.</sub-task>
                    You should output nothing else but the sub-tasks.
                    Your sub-tasks should not include steps that continue after the task is completed, 
                    such as review or promotion.
                    Your sub-tasks should all be actionable by an AI immediately.
                    Every sub-task should be a step towards completing the main task.
                    Every sub-task should be an action that can be taken.
                    Keep task lists short and focused.
                    Keep sub-tasks simple and clear.
                
                Don't:
                    Don't include sub-tasks that are not necessary to complete the main task.
                    Don't include sub-tasks that are not relevant to the main task.
                    Don't include sub-tasks that are not actionable.
                    Don't repeat sub-tasks.
                    Don't suggest including multimedia.
                    Don't suggest adding images or videos.
                    Don't be vague or ambiguous.
                    Don't include too many sub-tasks.
                
                You should output sub-tasks in this format: <sub-task>Task information.</sub-task>
                
                Example:
                    For the task "Write an essay on the history of the United States", you should output:
                    <sub-task>Write a summary of the task.</sub-task>
                    <sub-task>Find relevant information for the task.</sub-task>
                    <sub-task>Write a draft of the task.</sub-task>
                    <sub-task>Revise the draft.</sub-task>
                    <sub-task>Submit the task.</sub-task>
                    
                    For the task "Create a marketing plan for a new product", you should output:
                    <sub-task>Research the target market.</sub-task>
                    <sub-task>Identify the competition.</sub-task>
                    <sub-task>Develop a unique selling proposition.</sub-task>
                    <sub-task>Create a marketing strategy.</sub-task>
                    <sub-task>Implement the marketing plan.</sub-task>
                    
                    For the task "Develop a new feature for a software product", you should output:
                    <sub-task>Define the feature requirements.</sub-task>
                    <sub-task>Design the feature.</sub-task>
                    <sub-task>Develop the feature.</sub-task>
                    <sub-task>Test the feature.</sub-task>
                    <sub-task>Deploy the feature.</sub-task>
            """
            + "\n\n"
            + "Task: "
            + task
            + "\n\n"
            "Collaboration Chat:" + "\n\n".join(messages)
        )
        return prompt


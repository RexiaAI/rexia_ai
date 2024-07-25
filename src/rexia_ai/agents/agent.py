"""Agent class for ReXia.AI."""

import logging
import re
from typing import Type, Optional, List
from ..workflows import ReflectWorkflow
from ..structure import RexiaAIResponse
from ..memory import WorkingMemory
from ..base import BaseMemory, BaseWorkflow
from .routers import TaskComplexityRouter
from ..llms import RexiaAIOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
class Agent:
    """
    Agent class for ReXia AI.

    This agent is responsible for running the workflow and reflecting on the task.

    Attributes:
        llm (RexiaAIOpenAI): The language model used by the agent.
        workflow (BaseWorkflow): The workflow used by the agent.
        task (str): The task assigned to the agent.
        verbose (bool): Flag for enabling verbose mode.
        router (Optional[TaskComplexityRouter]): The task complexity router, if used.
        task_complexity (Optional[int]): The complexity of the task, if router is used.
    """

    def __init__(
        self,
        llm: RexiaAIOpenAI,
        task: str,
        workflow: Optional[Type[BaseWorkflow]] = None,
        memory: BaseMemory = WorkingMemory(),
        verbose: bool = False,
        use_router: bool = False,
        router_llm: Optional[RexiaAIOpenAI] = None,
        complex_llm: Optional[RexiaAIOpenAI] = None,
        task_complexity_threshold: int = 50,
    ):
        """
        Initialize an Agent instance.

        Args:
            llm (RexiaAIOpenAI): The language model used by the agent.
            task (str): The task assigned to the agent.
            workflow (Optional[Type[BaseWorkflow]]): The class of the workflow to be used.
            memory (BaseMemory): The memory instance to be used. Defaults to WorkingMemory().
            verbose (bool): Flag for enabling verbose mode. Defaults to False.
            use_router (bool): Whether to use the task complexity router. Defaults to False.
            router_llm (Optional[RexiaAIOpenAI]): The LLM for the router. Required if use_router is True.
            complex_llm (Optional[RexiaAIOpenAI]): The LLM for complex tasks. Required if use_router is True.
            task_complexity_threshold (int): Threshold for task complexity. Defaults to 50.

        Raises:
            ValueError: If use_router is True but router_llm or complex_llm is not provided.
        """
        self.task = task
        self.verbose = verbose

        if use_router:
            if not router_llm or not complex_llm:
                raise ValueError(
                    "router_llm and complex_llm must be provided when use_router is True"
                )
            self.router = TaskComplexityRouter(
                base_llm=llm,
                complex_llm=complex_llm,
                router_llm=router_llm,
                task_complexity_threshold=task_complexity_threshold,
            )
        else:
            self.router = None
            self.task_complexity = None
        
        self.llm = llm

        workflow_class = workflow or ReflectWorkflow
        self.workflow = workflow_class(
            llm=self.llm,
            task=task,
            memory=memory,
            verbose=verbose,
        )

    def run_workflow(self) -> List[str]:
        """
        Run the workflow and return the messages.

        Returns:
            The messages from the workflow.
        """
        logger.info("Starting workflow...")
        self.workflow.run()
        logger.info("Workflow completed.")
        return self.workflow.channel.messages

    def get_task_result(self, messages: List[str]) -> Optional[str]:
        """
        Extract the task result from the messages.

        Args:
            messages: The messages from which to extract the task result.

        Returns:
            The task result if it exists, None otherwise.
        """
        if not messages:
            logging.error("Error: No messages to process.")
            return None

        return messages[-1]

    def invoke(self, task: str = None) -> Optional[RexiaAIResponse]:
        """
        Invoke method for the agent.

        This method runs the workflow, gets the task result and the plan, updates the buffer manager with the plan,
        and returns the accepted answer if it exists.

        Returns:
            The accepted answer if it exists, None otherwise.
        """
        try:
            if task:
                self.task = self.workflow.channel.task = task
                if self.router:
                    self.task_complexity = self.router.route(task)
                    self.llm = (
                        self.router.complex_llm
                        if self.task_complexity > self.router.task_complexity_threshold
                        else self.router.base_llm
                    )
                    self.workflow.llm = self.llm
            self.workflow.clear_channel()  # Clear any messages from a previous task.
            messages = self.run_workflow()
            task_result = self.get_task_result(messages)
            accepted_answer = self.format_accepted_answer(task_result)
            return accepted_answer
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    def format_accepted_answer(self, answer: str) -> Optional[RexiaAIResponse]:
        """
        Format the accepted answer by removing any single word before the JSON object.

        Args:
            answer: The accepted answer to format.

        Returns:
            The formatted RexiaAIResponse if it exists and is valid, None otherwise.
        """
        if not answer:
            return None

        try:
            # Find the start of the JSON object
            json_start = answer.find("{")

            if json_start == -1:
                raise ValueError("No JSON object found in the answer")

            # Use regex to find the last word before the JSON object
            match = re.search(r"\S+\s*$", answer[:json_start])

            if match:
                # Remove the word and any whitespace after it
                json_str = answer[json_start:]
            else:
                json_str = answer[json_start:]

            # Parse the JSON string into a RexiaAIResponse object
            rexia_ai_response = RexiaAIResponse.from_json(json_str)

            return rexia_ai_response
        except Exception as e:
            logging.error(f"Error while formatting the answer: {e}")
            return None

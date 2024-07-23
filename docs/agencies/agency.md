# ReXia.AI Agency and ManagerAgent Classes

## Overview

The `Agency` and `ManagerAgent` classes are core components of the ReXia.AI framework, responsible for managing a group of autonomous agents to collaboratively execute complex tasks. This documentation provides a detailed overview of these classes, their attributes, methods, and usage.

## Agency Class

### Agency Class Overview

The `Agency` class represents a group of autonomous agents capable of collaborating on complex tasks.

### Agency Class Attributes

- `main_task`: The primary task assigned to the agency.
- `agents`: A list of available agents in the agency.
- `manager_llm`: The language model used by the manager agent.

### Agency Class Methods

#### Agency Initialization

```python
def __init__(self, main_task: str, agents: List[AgentInfo], manager_llm: RexiaAIOpenAI)
```

Initializes an `Agency` instance.

**Parameters:**

- `main_task`: The primary task to be completed by the agency.
- `agents`: A list of available agents.
- `manager_llm`: The language model used by the manager agent.

#### Agency Invocation

```python
def invoke(self, task: str = None) -> str
```

Starts the collaborative task execution, optionally accepting a new task to override the initial one.

**Parameters:**

- `task`: (Optional) A new task to override the initial one.

**Returns:**

- `str`: The results of the task execution.

### Agency Usage Example

```python
from rexia_ai.agency import Agency
from rexia_ai.llms import RexiaAIOpenAI

# Initialize the language model
manager_llm = RexiaAIOpenAI(...)

# Create an Agency instance
agency = Agency(
    main_task="Complete the project report",
    agents=[Agent1, Agent2, Agent3],
    manager_llm=manager_llm
)

# Invoke the agency to perform the task
result = agency.invoke()
print(result)
```

## ManagerAgent Class

### ManagerAgent Class Overview

The `ManagerAgent` class manages interactions between agents within an agency.

### ManagerAgent Class Attributes

- `agents`: A list of available agents.
- `manager_llm`: The language model used by the manager.
- `collaboration_channel`: A channel for agent collaboration.
- `memory`: Working memory for storing task-related information.
- `task`: The main task assigned to the manager.
- `subtasks`: A list of subtasks derived from the main task.

### ManagerAgent Class Methods

#### ManagerAgent Initialization

```python
def __init__(self, agents: List[AgentInfo], manager_llm: RexiaAIOpenAI)
```

Initializes the `ManagerAgent` instance.

**Parameters:**

- `agents`: A list of available agents.
- `manager_llm`: The language model used by the manager.

#### Task Assignment

```python
def assign_task(self, task: str) -> None
```

Assigns the main task to the manager.

**Parameters:**

- `task`: The main task to be completed.

#### Agent Management

```python
def manage_agents(self) -> None
```

Manages the work of various agents to iteratively complete the task.

#### Results Presentation

```python
def present_results(self) -> str
```

Summarizes and presents the results of the collaborative task execution.

**Returns:**

- `str`: A summarized report of the collaborative task execution.

#### Internal Methods

- `_get_next_action() -> Dict[str, Any]`: Determines the next action (subtask or completion).
- `_execute_assignment(assignment: AgentAssignment) -> None`: Executes a single agent assignment.
- `_create_action_prompt() -> str`: Generates prompts for the language model.
- `_summarise_results(results: str) -> str`: Summarizes the results of subtask executions.

### ManagerAgent Usage Example

```python
from rexia_ai.manager_agent import ManagerAgent
from rexia_ai.llms import RexiaAIOpenAI

# Initialize the language model
manager_llm = RexiaAIOpenAI(...)

# Create a ManagerAgent instance
manager_agent = ManagerAgent(
    agents=[AgentInfo1, AgentInfo2, AgentInfo3],
    manager_llm=manager_llm
)

# Assign a task to the manager
manager_agent.assign_task("Complete the project report")

# Manage agents to perform the task
manager_agent.manage_agents()

# Present the results
results = manager_agent.present_results()
print(results)
```

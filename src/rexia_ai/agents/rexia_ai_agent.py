"""The ReXiaAIAgent class for ReXia.AI."""

class ReXiaAIAgent:
    """A general agent that uses specialised workers to perform different tasks."""
    def __init__(self, name, channel, worker):
        self.name = name
        self.channel = channel
        self.worker = worker

    def run(self):
        """Run the agent."""
        response = self.perform_task()
        
        return response
                
    def perform_task(self):
        """Perform the task assigned to the agent."""
        task = self.channel.get_task()
        messages = self.channel.get_messages()
        print(f"{self.name} task: {task}")
        prompt = self.worker.create_prompt(task, messages)
        response = self.worker.action(prompt, self.name)
        self.channel.put(response)
        
        return response
    
    def get_tool_results(self):
        """Get the results of the tools used by the agent."""
        return "Tool results: " + "NOT IMPLEMENTED"


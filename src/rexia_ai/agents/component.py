"""The Component class for ReXia.AI."""

class Component:
    """A general component that uses specialised workers to perform different tasks."""
    def __init__(self, name, channel, worker):
        self.name = name
        self.channel = channel
        self.worker = worker

    def run(self):
        """Run the component."""
        response = self.perform_task()
        
        return response
                
    def perform_task(self):
        """Perform the task assigned to the component."""
        task = self.channel.task
        messages = self.channel.messages
        print(f"{self.name} task: {task}")
        prompt = self.worker.create_prompt(task, messages)
        response = self.worker.action(prompt, self.name)
        self.channel.put(response)
        
        return response
    
    def get_tool_results(self):
        """Get the results of the tools used by the component."""
        return "Tool results: " + "NOT IMPLEMENTED"


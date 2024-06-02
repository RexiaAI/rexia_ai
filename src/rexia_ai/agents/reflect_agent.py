"""reflect agent class for ReXia AI."""

from ..workflows import ReflectWorkflow

class ReflectAgent:
    """ReflectAgent class for ReXia AI."""
    def __init__(self, llm, task: str, verbose: bool = False):
        self.worker = ReflectWorkflow(llm, task, verbose)

    def reflect(self):
        """Reflect method for ReflectAgent."""
        self.worker.run()
        
        return self.worker.channel.messages
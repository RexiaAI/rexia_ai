import os
import gradio as gr
from rexia_ai.llms import RexiaAIOpenAI
from rexia_ai.agents import Agent
from rexia_ai.workflows import SimpleToolWorkflow
from rexia_ai.tools import RexiaAIGoogleSearch
from rexia_ai.structure import RexiaAIResponse

# Get the required keys from the environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

class PerplexityLite():
    """A simple version of Perplexity using ReXia.AI, Gradio and Llama 3 8b."""
    def __init__(self) -> None:
        self.google_search = RexiaAIGoogleSearch(api_key=GOOGLE_API_KEY, engine_id=SEARCH_ENGINE_ID)
        
        # Create a dictionary mapping the tool name to its instance
        self.tools = {"google_search": self.google_search}
        
        # Create an instance of the RexiaAILLMWare LLM and give it the tools
        self.llm = RexiaAIOpenAI(
            base_url="http://localhost:1234/v1",
            model="lm-studio",
            temperature=0,
            tools=self.tools,
        )
        
        # Create an instance of the RexiaAI Agent with the specified task and LLM, we'll use the SimpleToolWorkflow here.
        self.agent = Agent(llm=self.llm, task="", verbose=True, workflow=SimpleToolWorkflow)
        
    def invoke(self, task: str) -> str:
        """Invoke the agent with the task."""
        response = self.agent.invoke(task)
        structured_response = RexiaAIResponse.from_json(str(response))
        
        return structured_response.answer

# Create an instance of PerplexityLite
perplexity_lite = PerplexityLite()

# Define the Gradio interface
def chatbot(message, history):
    """Chatbot function that uses the PerplexityLite agent to generate a response."""  
    # Invoke the PerplexityLite agent with the message
    response = perplexity_lite.invoke(message)
    return response



# Create and launch the Gradio interface
iface = gr.ChatInterface(
    fn=chatbot,
    title="PerplexityLite Chatbot",
    description="Ask me anything, and I'll use ReXia.AI, Gradio, and Llama 3 8b to find an answer!",
    examples=[
        "What's the weather like in New York today?",
        "Tell me about the latest advancements in AI",
        "How does quantum computing work?",
    ],
    theme="soft",
)

if __name__ == "__main__":
    iface.launch()

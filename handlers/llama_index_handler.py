# llama_index_handler.py
from llama_index.agent.introspective import IntrospectiveAgentWorker, SelfReflectionAgentWorker
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.agent import AgentRunner, FunctionCallingAgentWorker, ReActAgentWorker, StructuredPlannerAgent
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.tools.arxiv import ArxivToolSpec
from llama_index.tools.google import GoogleSearchToolSpec
from rexia_ai.utilities import GOOGLE_API_KEY, OLLAMA_EMBED_MODEL, OLLAMA_LLM, OPENAI_API_KEY, OPENAI_LLM, SEARCH_ENGINE_ID
from typing import Any, List

class LlamaIndexLLMHandler:
    """Handler for Llama Index Language Models."""

    def create_ollama_llm(self, model=OLLAMA_LLM, verbose=True, temperature=0.2, timeout=3000, system_prompt=None):
        """Create an Ollama language model."""
        return Ollama(model=model, verbose=verbose, temperature=temperature, request_timeout=timeout, system_prompt=system_prompt)

    def create_openai_llm(self, model=OPENAI_LLM, verbose=True, temperature=0.2, api_key=OPENAI_API_KEY, system_prompt=None):
        """Create an OpenAI language model."""
        return OpenAI(model=model, verbose=verbose, temperature=temperature, api_key=api_key, system_prompt=system_prompt)

class LlamaIndexAgentHandler:
    """Handler for Llama Index Agents."""

    def add_google_tool(self):
        """Add a Google tool to the agent."""
        google_tool_spec = GoogleSearchToolSpec(key=GOOGLE_API_KEY, engine=SEARCH_ENGINE_ID).to_tool_list()[0]
        return google_tool_spec
    
    def add_arxiv_tool(self):
        """Add an Arxiv tool to the agent."""
        arxiv_tool_spec = ArxivToolSpec().to_tool_list()[0]
        return arxiv_tool_spec
    
    def create_agent_runner(self, tools, llm, verbose=True):
        """Create an agent runner."""
        return AgentRunner(tools=tools, llm=llm, verbose=verbose)
    
    def create_function_callin_agent(self, tools, llm, verbose=True):
        """Create a function calling agent."""
        return FunctionCallingAgentWorker.from_tools(tools=tools, llm=llm, verbose=verbose).as_agent()
    
    def create_react_agent(self, tools, llm, verbose=True):
        """Create a react agent."""
        return ReActAgentWorker.from_tools(tools=tools, llm=llm, verbose=verbose).as_agent()
    
    def create_structured_planner_agent(self, tools, llm, verbose=True):
        """Create a structured planner agent."""
        return StructuredPlannerAgent(tools=tools, llm=llm, verbose=verbose)
    
    def create_self_reflection_agent_worker(self, llm, verbose=True, system_prompt=None):
        """Create a self reflection agent worker."""
        return SelfReflectionAgentWorker.from_defaults(llm=llm, verbose=verbose, system_prompt=system_prompt)
    
    def create_introspective_agent(self, reflective_agent_worker, main_agent_worker, verbose=True, chat_history=None):
        """Create an introspective agent."""
        return IntrospectiveAgentWorker.from_defaults(reflective_agent_worker=reflective_agent_worker, main_agent_worker=main_agent_worker, verbose=verbose).as_agent(chat_history=chat_history)

class LlamaIndexVectorStoreHandler:
    """Handler for Llama Index Vector Store."""

    def get_directory_reader(self, path):
        """Get a directory reader."""
        return SimpleDirectoryReader(path)
    
    def get_vector_store_index(self, documents):
        """Get a vector store index."""
        return VectorStoreIndex.from_documents(documents)
    
    def create_ollama_embeddings(self):
        """Create Ollama embeddings."""
        return OllamaEmbedding(model_name=OLLAMA_EMBED_MODEL)
    
    def create_chat_engine(self, index: VectorStoreIndex, llm):
        """Create a chat engine."""
        return index.as_chat_engine(llm=llm)
    
    def create_query_engine(self, index: VectorStoreIndex, llm):
        """Create a query engine."""
        return index.as_query_engine(llm=llm)
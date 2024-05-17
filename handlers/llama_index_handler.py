# llama_index_handler.py
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import FunctionCallingAgentWorker, ReActAgentWorker, AgentRunner, StructuredPlannerAgent
from llama_index.agent.introspective import IntrospectiveAgentWorker, SelfReflectionAgentWorker
from llama_index.tools.google import GoogleSearchToolSpec
from llama_index.tools.arxiv import ArxivToolSpec
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from rexia_ai.utilities import OPENAI_LLM, OLLAMA_LLM, OPENAI_API_KEY, GOOGLE_API_KEY, SEARCH_ENGINE_ID, OLLAMA_EMBED_MODEL

class LlamaIndexLLMHandler:
    def create_ollama_llm(self, model=OLLAMA_LLM, verbose=True, temperature=0.2, timeout=3000, system_prompt=None):
        return Ollama(model=model, verbose=verbose, temperature=temperature, request_timeout=timeout, system_prompt=system_prompt)

    def create_openai_llm(self, model=OPENAI_LLM, verbose=True, temperature=0.2, api_key=OPENAI_API_KEY, system_prompt=None):
        return OpenAI(model=model, verbose=verbose, temperature=temperature, api_key=api_key, system_prompt=system_prompt)

class LlamaIndexAgentHandler:
    def add_google_tool(self):
        google_tool_spec = GoogleSearchToolSpec(key=GOOGLE_API_KEY, engine=SEARCH_ENGINE_ID).to_tool_list()[0]
        return google_tool_spec
    
    def add_arxiv_tool(self):
        arxiv_tool_spec = ArxivToolSpec().to_tool_list()[0]
        return arxiv_tool_spec
    
    def create_agent_runner(self, tools, llm, verbose=True):
        return AgentRunner(tools=tools, llm=llm, verbose=verbose)
    
    def create_agent_worker(self, tools, llm, verbose=True):
        return AgentRunner(tools=tools, llm=llm, verbose=verbose).as_agent()
    
    def create_function_callin_agent(self, tools, llm, verbose=True):
        return FunctionCallingAgentWorker.from_tools(tools=tools, llm=llm, verbose=verbose).as_agent()
    
    def create_react_agent(self, tools, llm, verbose=True):
        return ReActAgentWorker.from_tools(tools=tools, llm=llm, verbose=verbose).as_agent()
    
    def create_structured_planner_agent(self, tools, llm, verbose=True):
        return StructuredPlannerAgent(tools=tools, llm=llm, verbose=verbose)
    
    def create_self_reflection_agent_worker(self, llm, verbose=True, system_prompt=None):
        return SelfReflectionAgentWorker.from_defaults(llm=llm, verbose=verbose, system_prompt=system_prompt)
    
    def create_introspective_agent(self, reflective_agent_worker, main_agent_worker, verbose=True, chat_history=None):
        return IntrospectiveAgentWorker.from_defaults(reflective_agent_worker=reflective_agent_worker, main_agent_worker=main_agent_worker, verbose=verbose).as_agent(chat_history=chat_history)

class LlamaIndexVectorStoreHandler:
    def get_directory_reader(self, path):
        return SimpleDirectoryReader(path)
    
    def get_vector_store_index(self, documents):
        return VectorStoreIndex.from_documents(documents)
    
    def create_ollama_embeddings(self):
        return OllamaEmbedding(model_name=OLLAMA_EMBED_MODEL)
    
    def create_chat_engine(self, index: VectorStoreIndex, llm):
        return index.as_chat_engine(llm=llm)
    
    def create_query_engine(self, index: VectorStoreIndex, llm):
        return index.as_query_engine(llm=llm)
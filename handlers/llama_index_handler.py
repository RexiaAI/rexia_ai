# llama_index_handler.py
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from rexia_ai.utilities import GOOGLE_API_KEY, OLLAMA_EMBED_MODEL, OLLAMA_LLM, OPENAI_API_KEY, OPENAI_LLM, SEARCH_ENGINE_ID
from typing import Any, List

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
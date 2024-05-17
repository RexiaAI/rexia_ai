# llama_index_tools.py
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from llama_index.tools.arxiv import ArxivToolSpec
from llama_index.tools.google import GoogleSearchToolSpec

class ArxivToolSpec(ArxivToolSpec):
    """Arxiv tool spec for Llama Index."""
    
    def __init__(self):
        super().__init__()
        
class GoogleSearchToolSpec(GoogleSearchToolSpec):
    """Google Search tool spec for Llama Index."""
    
    def __init__(self, key: str, engine: str):
        super().__init__(key=key, engine=engine)

class BaseToolSpec(BaseToolSpec):
    """Base tool spec for Llama Index."""
    
    def __init__(self):
        super().__init__()
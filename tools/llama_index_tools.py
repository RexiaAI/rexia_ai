# llama_index_tools.py
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from llama_index.tools.arxiv import ArxivToolSpec
from llama_index.tools.google import GoogleSearchToolSpec

class ArxivToolSpec(ArxivToolSpec):
    """This class is a wrapper for llama_index.tools.arxiv ArxivToolSpec."""
    
    def __init__(self):
        super().__init__()
        
class GoogleSearchToolSpec(GoogleSearchToolSpec):
    """This class is a wrapper for llama_index.tools.gooogle GoogleSearcToolSpec."""
    
    def __init__(self, key: str, engine: str):
        super().__init__(key=key, engine=engine)

class BaseToolSpec(BaseToolSpec):
    """Thos class is a wraper for llama_index.core.tools.tool_spec.base BaseToolSpec."""
    
    def __init__(self):
        super().__init__()
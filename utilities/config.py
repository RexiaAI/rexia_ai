# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_LLM = os.getenv("OPENAI_LLM")
OLLAMA_LLM = os.getenv("OLLAMA_LLM")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
OLLAMA_EMBED_MODEL = os.getenv("EMBED_MODEL")
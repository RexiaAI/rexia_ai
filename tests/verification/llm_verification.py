"""LLM verification, uses a large language model to verify output from ReXia.AI"""

from rexia_ai.llms import RexiaAIOpenAI

class LLMVerification():
    """LLMVerification class for ReXia.AI. Automates verification of ReXia.AI output for testing purposes."""
    
    def __init__(self, base_url: str, api_key: str, model: str, temperature: float) -> None:
        """Initializes the LLMVerification class with the given api key and base url.
        
            Args:
               base_url (str): The base URL for the ReXia.AI API.
               api_key (str): The API key for authentication with the ReXia.AI API.
               model (str): The model to use for verification.
               temperature (float): The temperature for the model to use.
        """
        self.llm = RexiaAIOpenAI(base_url=base_url, api_key=api_key, model=model, temperature=temperature)
        
    def verify(self, prompt: str) -> bool:
        """Verifies the output of ReXia.AI LLM by sending a prompt and checking if it returns a valid response.
        Args:
        prompt (str): The input prompt to be sent to the ReXia.AI API for verification.
        """
        try:
            result = self.llm.invoke(prompt)
            if "PASSED" in result:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error occurred invoking the LLM for verification: {e}") 
            return False
        
    @staticmethod
    def get_verification_prompt():
        """Returns a predefined prompt used to verify ReXia.AI LLM."""
        
        return """You are a verification agent for ReXia.AI. Your job is to read a given task,
        the collaboration chat associated with that task if present, the task history if present, and the
        response given to that task and determine if the response correctly answers the question
        or not. 
        
        If it does, end your response with "PASSED".
        
        If it doesn't, end your response with "FAILED".
        
        You should look for any logical errors, factual inaccuracies, or inconsistencies in the response
        that would make it incorrect. If you find such issues, please specify them in your response."""
            
        
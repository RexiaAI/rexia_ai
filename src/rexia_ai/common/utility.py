"""Utility class for ReXia.AI."""

import re
import json_repair

class Utility:
    """
    A utility class providing helper methods for ReXia.AI operations.

    This class contains various utility methods that can be used across
    the ReXia.AI application for common tasks such as string manipulation.
    """

    @staticmethod
    def strip_tags(response: str) -> str:
        """
        Strip code block tags from the start and end of a string.

        This method removes code block markers (``` followed by language identifier)
        from the beginning of the string and closing code block markers (```) from the end.
        It's useful for cleaning up responses that might contain formatted code blocks.

        Args:
            response (str): The string from which to strip code block tags.

        Returns:
            str: The input string with code block tags removed and whitespace trimmed.

        Example:
            >>> Utility.strip_tags("```python\\nprint('Hello')\\n```")
            "print('Hello')"
        """
        # Remove opening tags
        response = re.sub(r"^```(?:python|json)\n", "", response, flags=re.MULTILINE)
        
        # Remove closing tags, preserving the newline
        response = re.sub(r"```$", "", response, flags=re.MULTILINE)
        
        # Trim any leading/trailing whitespace
        return response.strip()
    
    @staticmethod
    def remove_system_tokens(s: str) -> str:
        """
        Remove system tokens from the string.

        Args:
            s: The string from which to remove system tokens.

        Returns:
            The string with system tokens removed.
        """
        return re.sub(r"</?[\w_]+>|<\|.*?\|>", "", s)
    
    @staticmethod
    def extract_json_string(text):
        """
        Extracts the first JSON object from a given text string.

        Args:
            text (str): Input text potentially containing a JSON object.

        Returns:
            str: Extracted JSON object if found, otherwise the entire input text.

        Note:
            Uses regex to find JSON objects. Does not validate JSON structure.
        """
        pattern = r'\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}'
        match = re.search(pattern, text, re.DOTALL)
        return match.group(0) if match else text
    
    @staticmethod
    def fix_json_errors(json_string: str) -> str:
        """
        Attempt to fix common JSON errors using json-repair.

        This method uses the json-repair library to handle common JSON formatting errors
        that might occur in responses from large language models.

        Args:
            json_string (str): The potentially malformed JSON string.

        Returns:
            str: The JSON string with common errors fixed.
        """
        try:
            repaired_json = json_repair.repair_json(json_string)
            return repaired_json
        except Exception as e:
            print(f"Error while fixing JSON string with json-repair: {e}")
            return json_string
        
    @staticmethod
    def fix_json_errors_prompt(json_string: str, error: str) -> str:
        """
         Generate a prompt to instruct an llm to fix errors in a json object.
         
         Args:
            json_string (str): the malformed json string.
            error (str): the error in the json.
            llm (RexiaAIOpenAI): The large language model to use.
        """
        fix_errors_prompt = f"""
        Please fix this incorrectly formatted JSON object.

        Error: {str(error)}

        Incorrectly Formatted JSON: 
        {json_string}
        
        You should reuse the same format, but ensure that the JSON is correctly formatted.

        Instructions for correction:
        1. Carefully review the JSON structure and content.
        2. Identify and fix any syntax errors (e.g., missing quotes, commas, brackets).
        3. Ensure all keys are properly quoted.
        4. Verify that string values are enclosed in double quotes.
        5. Check that numbers, booleans, and null values are not quoted.
        6. Remove any trailing commas in objects or arrays.
        7. Eliminate any text or comments outside the JSON structure.

        Your response should ONLY contain valid JSON.
        
        Do not include anything outside this structure or the task will fail.
        Do not include any comments or additional information or the task will fail.
        Do not include any text outside the JSON structure or the task will fail.
        Do not include any unquoted keys or values or the task will fail.
        Do not include any syntax errors or the task will fail.
        """
                
        return fix_errors_prompt

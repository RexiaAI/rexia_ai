""" ReXia.AI Image Analysis Tool - Let your text based models call a vision model to analyse images.
Should work with any vision or multimodal model. Tested on GPT-4o and llava phi 3."""

import base64
import requests
from openai import OpenAI
from ..base import BaseTool
from ..structure import LLMOutput


class RexiaAIImageAnalysis(BaseTool):
    """
    Image Analysis Tool that works with ReXia.AI. 
    Note: This tool requires a vision model or multimodal model to be set up and supplied.

    Attributes
    ----------
    api_key : str
        The API key for OpenAI.
    vision_model_base_url : str
        The base URL for the vision model.
    vision_model : str
        The name of the vision model.

    Methods
    -------
    analyse(query: str, image_path: str) -> str:
        Process an image and get a response.
    to_rexiaai_tool() -> list:
        Return the tool as a JSON object for ReXia.AI.
    to_rexiaai_function_call() -> dict:
        Return the tool as a dictionary object for ReXia.AI.
    """

    def __init__(self, vision_model_base_url: str, vision_model: str, api_key: str):
        """
        Constructs all the necessary attributes for the RexiaAIImageAnalysis object.

        Parameters
        ----------
            vision_model_base_url : str
                The base URL for the vision model.
            vision_model : str
                The name of the vision model.
            api_key : str
                The API key for OpenAI.
        """
        super().__init__(
            name="image_analysis",
            func=self.analyse,
            description="Use a vision model to analyse an image",
        )
        self.vision_model_base_url = vision_model_base_url
        self.vision_model = vision_model
        self.api_key = api_key
        self.llm = OpenAI(base_url=vision_model_base_url, api_key=api_key)

    def _get_image_data(self, image_path: str) -> bytes:
        """
        Get image data from a URL or a local path.

        Parameters
        ----------
            image_path : str
                The path to the image file.

        Returns
        -------
            bytes
                The image data.
        """
        if image_path.startswith("http://") or image_path.startswith("https://"):
            response = requests.get(image_path, timeout=10)
            response.raise_for_status()
            return response.content
        else:
            with open(image_path, "rb") as f:
                return f.read()

    def analyse(self, query: str, image_path: str) -> str:
        """
        Process an image and get a response.

        Parameters
        ----------
            query : str
                The query to analyze.
            image_path : str
                The path to the image file.

        Returns
        -------
            str
                The analysis result.
        """
        image_data = self._get_image_data(image_path)
        image_b64 = base64.b64encode(image_data).decode()

        response = self.llm.chat.completions.create(
            model=self.vision_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an image analysis agent. Please provide the requested information for this image.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{query} \n\n Structure your response in the following format: {LLMOutput.get_output_structure()}",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpg;base64,{image_b64}"},
                        },
                    ],
                },
            ],
            temperature=0.0,
        )
        return response.choices[0].message.content

    def to_rexiaai_tool(self) -> list:
        """
        Return the tool as a JSON object for ReXia.AI.

        Returns
        -------
            list
                The tool as a JSON object.
        """
        tool = [
            {
                "name": "image_analysis",
                "description": "Use a vision model to analyse an image",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "What you want to analyse in the image"
                            "e.g. 'How many people are in this image?'",
                        },
                        "image_path": {
                            "type": "string",
                            "description": "The image you wish to analyse"
                            "e.g. 'https://example.com/image.jpg'",
                        },
                    },
                    "required": ["query", "image_path"],
                },
            }
        ]

        return tool

    def to_rexiaai_function_call(self) -> dict:
        """
        Return the tool as a dictionary object for ReXia.AI.

        Returns
        -------
            dict
                The tool as a dictionary object.
        """
        function_call = {"name": "analyse"}

        return function_call
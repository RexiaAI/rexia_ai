""" Rexia AI Image Analysis Tool"""

import base64
import requests
from openai import OpenAI
from ..base import BaseTool
from ..structure import LLMOutput


class RexiaAIImageAnalysis(BaseTool):
    """Image Analysis Tool that works with ReXia.AI. Note: This tool requires a vision model or multimodal model
    to be set up and supplied"""

    api_key: str
    engine_id: str

    def __init__(self, vision_model_base_url: str, vision_model: str, api_key: str):
        super().__init__(
            name="image_analysis",
            func=self.analyse,
            description="Use a vision model to analyse an image",
        )
        self.vision_model_base_url = vision_model_base_url
        self.vision_model = vision_model
        self.api_key = api_key
        self.llm = OpenAI(base_url=vision_model_base_url, api_key=api_key)

    def analyse(self, query: str, image_path: str) -> str:
        """Process an image and get a response."""
        # Check if the input is a URL or a local path
        if image_path.startswith("http://") or image_path.startswith("https://"):
            # It's a URL, download the image
            response = requests.get(image_path, timeout=10)
            response.raise_for_status()  # Raise an exception if the request was not successful
            image_data = response.content
        else:
            # It's a local path, read the image
            with open(image_path, "rb") as f:
                image_data = f.read()

        # Encode the image
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

    def to_rexiaai_tool(self):
        """Return the tool as a JSON object for ReXia.AI."""

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

    def to_rexiaai_function_call(self):
        """Return the tool as a dictionary object for ReXia.AI."""
        function_call = {"name": "analyse"}

        return function_call

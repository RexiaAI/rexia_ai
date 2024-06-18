"""
Rexia AI Youtube Video Analysis Tool
Use a multimodal model to analyse and extract insights from a YouTube video.
Uses OpenAI's Whisper to transcribe the audio and a multimodal model to analyse the video frames and transcript.
"""

import uuid
import os
import base64
from typing import Tuple
from pytube import YouTube
import cv2
from moviepy.editor import AudioFileClip
from openai import OpenAI
from ..base import BaseTool


class RexiaAIYoutubeVideoAnalysis(BaseTool):
    """
    Tool that works with ReXia.AI to analyse YouTube videos.

    Attributes:
        openai_api_key (str): OpenAI API key for accessing the models.
        vision_model_base_url (str): Base URL for the vision model.
        vision_model (str): Name of the vision model to use.
        whisper_model (str): Name of the Whisper model to use for transcription (default: "base").
    """

    openai_api_key: str
    vision_model_base_url: str
    vision_model: str
    whisper_model: str

    def __init__(
        self,
        vision_model_base_url: str,
        vision_model: str,
        openai_api_key: str,
        whisper_model: str = "base",
    ):
        super().__init__(
            name="analyse_video",
            func=self.analyse_video,
            description="Analyse the video and extract insights",
        )
        self.vision_model_base_url = vision_model_base_url
        self.vision_model = vision_model
        self.llm = OpenAI(base_url=vision_model_base_url, api_key=openai_api_key)
        self.whisper_model = whisper_model

    def analyse_video(self, query: str, video_url: str) -> str:
        """
        Analyse the video and extract insights based on the given query.

        Args:
            query (str): The query or question about the video.
            video_path (str): The path or URL of the YouTube video to analyse.

        Returns:
            str: The analysis and insights extracted from the video.

        Raises:
            Exception: If an error occurs during the analysis process.
        """
        try:
            base64_frames, audio_path = self._process_video(video_url)
            audio_transcription = self._transcribe(audio_path)
            os.remove(audio_path)  # Remove the temporary audio file

            filtered_frames = base64_frames[::5]  # Send only every 5th frame to reduce API calls

            response = self.llm.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a video analysis tool. Please answer any questions on a given video.",
                    },
                    {
                        "role": "user",
                        "content": [
                            f"This is the query: {query}",
                            f"This is the video's audio transcription: {audio_transcription}",
                            "Here are the frames from the video.",
                            *map(
                                lambda x: {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpg;base64,{x}",
                                        "detail": "low",
                                    },
                                },
                                filtered_frames,
                            ),
                        ],
                    },
                ],
                temperature=0,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred during the analysis: {str(e)}"

    def _process_video(self, video_url: str, seconds_per_frame: int = 2) -> Tuple[list, str]:
        """
        Extract frames and audio from a video file.

        Args:
            video_path (str): The path or URL of the YouTube video.
            seconds_per_frame (int): The number of seconds between each frame (default: 2).

        Returns:
            Tuple[list, str]: A list of base64-encoded frames and the path to the temporary audio file.

        Raises:
            Exception: If an error occurs during video processing.
        """
        base64_frames = []

        try:
            # Define the directory for temporary files
            temp_dir = os.path.join(os.path.dirname(__file__), 'temp_tool_files')

            # Make sure the directory exists
            os.makedirs(temp_dir, exist_ok=True)

            # Create a YouTube object
            yt = YouTube(video_url)

            # Generate a unique identifier for the video
            video_id = str(uuid.uuid4())

            # Download the video file
            yt.streams.first().download(output_path=temp_dir, filename=f'{video_id}.mp4')

            # Define the path for the temporary video file
            temp_file_path = os.path.join(temp_dir, f'{video_id}.mp4')

            # Update the video path to the temporary file path
            video_url = temp_file_path

            base_video_path, _ = os.path.splitext(video_url)

            video = cv2.VideoCapture(video_url)
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = video.get(cv2.CAP_PROP_FPS)
            frames_to_skip = int(fps * seconds_per_frame)
            curr_frame = 0

            while curr_frame < total_frames - 1:
                video.set(cv2.CAP_PROP_POS_FRAMES, curr_frame)
                success, frame = video.read()
                if not success:
                    break
                _, buffer = cv2.imencode(".jpg", frame)
                base64_frames.append(base64.b64encode(buffer).decode("utf-8"))
                curr_frame += frames_to_skip
            video.release()

            # Extract audio with moviepy
            audio_path = f"{base_video_path}.mp3"
            audio_clip = AudioFileClip(video_url)
            audio_clip.write_audiofile(audio_path, bitrate="32k")
            audio_clip.close()

            # Once done, delete the video file
            os.remove(video_url)

        except Exception as e:
            raise Exception(f"Error processing video: {str(e)}")

        return base64_frames, audio_path

    def _transcribe(self, audio_path: str) -> str:
        """
        Generate a transcription of the audio file.

        Args:
            audio_path (str): The path to the audio file.

        Returns:
            str: The transcription of the audio.

        Raises:
            Exception: If an error occurs during transcription.
        """
        try:
            with open(audio_path, "rb") as audio_file:
                transcription = self.llm.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                )
            return transcription.text
        except Exception as e:
            raise Exception(f"Error transcribing audio: {str(e)}")

    def to_rexiaai_tool(self) -> list:
        """
        Return the tool as a JSON object for ReXia.AI.

        Returns:
            list: A list containing the tool's JSON representation.
        """
        tool = [
            {
                "name": "analyse_video",
                "description": "Use a vision model to analyse a video",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "What you want to analyse in the video, e.g., 'What is this video about?'",
                        },
                        "video_url": {
                            "type": "string",
                            "description": "The video you wish to analyse, e.g., 'https://www.youtube.com/watch?v=c0m6yaGlZh4&ab_channel=DukeUniversity'",
                        },
                    },
                    "required": ["query", "video_path"],
                },
            }
        ]

        return tool

    def to_rexiaai_function_call(self) -> dict:
        """
        Return the tool as a dictionary object for ReXia.AI.

        Returns:
            dict: A dictionary representing the function call for the tool.
        """
        function_call = {"name": "analyse_video"}

        return function_call
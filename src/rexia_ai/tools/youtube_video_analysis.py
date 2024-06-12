""" Rexia AI Youtube Video Analysis Tool - Use a multimodal model to analyse and extract insights from a youtube video. 
Uses Open AI's whisper to transcribe the audio and a multimodal model to analyse the video frames and transcript. """

import uuid
import os
import base64
from pytube import YouTube
import cv2
from moviepy.editor import AudioFileClip
from openai import OpenAI
from ..base import BaseTool


class RexiaAIYoutubeVideoAnalysis(BaseTool):
    """Tool that works with ReXia.AI."""

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

    def analyse_video(self, query: str, video_path: str) -> str:
        """Analyse the video and extract insights."""
        base64_frames, audio_path = self._process_video(video_path)
        audio_transcription = self._transcribe(audio_path)

        filtered_frames = base64_frames[
            ::5
        ]  # Send only every 5th frame. Keeps the number of frames low for the API call whilst still providing a good summary.
        response = self.llm.chat.completions.create(
            model=self.vision_model,
            messages=[
                {
                    "role": "system",
                    "content": "You a video analysis tool. Please answer any questions on a given video.",
                },
                {
                    "role": "user",
                    "content": [
                        f"This is the query: {query}"
                        f"This is the video's audio transcription: {audio_transcription}"
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

    def _process_video(self, video_path: str, seconds_per_frame=2):
        """Extract frames and audio from a video file."""
        base64_frames = []

       # Define the directory for temporary files
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp_tool_files')

        # Make sure the directory exists
        os.makedirs(temp_dir, exist_ok=True)

        # Create a YouTube object
        yt = YouTube(video_path)

        # Generate a unique identifier for the video
        video_id = str(uuid.uuid4())

        # Download the video file
        yt.streams.first().download(output_path=temp_dir, filename=f'{video_id}.mp4')

        # Define the path for the temporary video file
        temp_file_path = os.path.join(temp_dir, f'{video_id}.mp4')

        # Update the video path to the temporary file path
        video_path = temp_file_path

        base_video_path, _ = os.path.splitext(video_path)

        video = cv2.VideoCapture(video_path)
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
        audio_clip = AudioFileClip(video_path)
        audio_clip.write_audiofile(audio_path, bitrate="32k")
        audio_clip.close()

        # Once done, delete the video file
        os.remove(video_path)

        return base64_frames, audio_path

    def _transcribe(self, audio_path):
        """Generate a summary of the audio transcription."""
        transcription = self.llm.audio.transcriptions.create(
            model="whisper-1",
            file=open(audio_path, "rb"),
        )
        return transcription.text
    
    def to_rexiaai_tool(self):
        """Return the tool as a JSON object for ReXia.AI."""

        tool = [
            {
                "name": "video_analysis",
                "description": "Use a vision model to analyse a video",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "What you want to analyse in the video"
                            "e.g. 'What is this video about?'",
                        },
                        "video_path": {
                            "type": "string",
                            "description": "The video you wish to analyse"
                            "e.g. 'https://www.youtube.com/watch?v=c0m6yaGlZh4&ab_channel=DukeUniversity'",
                        },
                    },
                    "required": ["query", "video_path"],
                },
            }
        ]

        return tool

    def to_rexiaai_function_call(self):
        """Return the tool as a dictionary object for ReXia.AI."""
        function_call = {"name": "analyse_video"}

        return function_call

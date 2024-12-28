from fastapi import APIRouter, HTTPException
import sys
import os
import openai
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.video2audio import process_youtube_video
from app.services.audio2text import AudioTranslator, process_audio_from_videos
from app.services.summarize import summarizer
from dotenv import load_dotenv
router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

openai.api_key = os.getenv("OPENAI_API_KEY")

@router.get("/summarize")
async def get_summary(url: str):
    try:
        print(f"Processing URL: {url}")

        backend_dir = os.path.normpath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        video_dir = os.path.normpath(os.path.join(backend_dir, "video"))

        os.makedirs(video_dir, exist_ok=True)

        audio_file_path = process_youtube_video(url)
        print(f"Video processed successfully: {audio_file_path}")

        audio_path = os.path.normpath(os.path.join(backend_dir, audio_file_path))
        print(f"Using audio path: {audio_path}")

        if not os.path.exists(audio_path):
            print(f"File not found at: {audio_path}")
            print(f"Directory contents: {os.listdir(os.path.dirname(audio_path))}")
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        process_audio_from_videos([audio_path])
        print("Audio translated successfully")

        text_path = os.path.normpath(os.path.join(video_dir, "all_text.txt"))
        with open(text_path, "r", encoding="utf-8") as f:
            text = f.readline()

        model = summarizer()
        summary = model.generate(text)
        print("Summary generated successfully")

        return {"summary": summary}
    except Exception as e:
        print(f"Current working directory: {os.getcwd()}")
        print(f"Error details: {str(e)}")
        print(f"Video directory exists: {os.path.exists(video_dir)}")
        if os.path.exists(video_dir):
            print(f"Video directory contents: {os.listdir(video_dir)}")
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        )
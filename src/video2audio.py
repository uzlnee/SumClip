import os
from glob import glob

import cv2
import yt_dlp
from moviepy import VideoFileClip

def download_video_from_url(url: str):
    """
    Download a YouTube video from the given URL and save it locally.
    """
    ydl_opts = {
        "format": "best",
        "outtmpl": "video/%(title)s.%(ext)s",  # Save in a specific folder
    }
    os.makedirs("video", exist_ok=True)  # Create directory for the video

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def extract_frames(video_path: str, output_folder: str):
    """
    Extract frames from a video and save them as images.
    """
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    frame_count = 0

    while success:
        frame_count += 1
        frame_file = f"{output_folder}/frame_{frame_count}.jpg"
        cv2.imwrite(frame_file, frame)
        success, frame = cap.read()

    cap.release()
    print(f"Extracted {frame_count} frames to {output_folder}.")


def extract_audio(video_path: str, output_audio_file: str):
    """
    Extract audio from a video file and save it as an MP3.
    """
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_file)
    audio.close()
    video.close()
    print(f"Audio extracted to {output_audio_file}")


def process_youtube_video(url: str):
    """
    Main function to download a YouTube video, extract its frames, and extract audio.
    """
    # Step 1: Download the video
    print(f"Downloading video from URL: {url}")
    download_video_from_url(url)

    # Step 2: Locate the downloaded video
    video_folder = "video"
    video_files = glob(f"{video_folder}/*.mp4")
    if not video_files:
        raise FileNotFoundError("No video file found after download.")

    video_path = video_files[0]

    # Step 3: Extract frames
    frames_folder = f"{video_folder}/frames"
    extract_frames(video_path, frames_folder)

    # Step 4: Extract audio
    audio_file = f"{video_folder}/audio.mp3"
    extract_audio(video_path, audio_file)


if __name__ == "__main__":
    # Example: Replace with the YouTube URL you want to process
    youtube_url = input("Enter the YouTube video URL: ").strip()
    process_youtube_video(youtube_url)

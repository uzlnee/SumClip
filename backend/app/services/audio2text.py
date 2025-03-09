import os
from glob import glob

import pandas as pd
import whisper
from pydub import AudioSegment
from .summarize import summarizer


class AudioTranslator:
    def __init__(self, model_name="base"):
        """
        Initialize the Whisper model for transcription.
        """
        self.model = whisper.load_model(model_name)

    def mp3_to_wav(self, audio_path: str) -> str:
        """
        Convert an MP3 file to WAV format.
        Args:
            audio_path (str): Path to the MP3 file.
        Returns:
            str: Path to the converted WAV file.
        """
        wav_path = audio_path.replace(".mp3", ".wav")
        audio = AudioSegment.from_mp3(audio_path)
        audio.export(wav_path, format="wav")
        print(f"Converted {audio_path} to {wav_path}")
        return wav_path

    def audio_to_text(self, audio_path: str) -> str:
        """
        Transcribe audio to text using Whisper.
        Args:
            audio_path (str): Path to the audio file (MP3 or WAV).
        Returns:
            str: Transcribed text.
        """
        # Convert to WAV if input is MP3
        if audio_path.endswith(".mp3"):
            audio_path = self.mp3_to_wav(audio_path)

        result = self.model.transcribe(audio_path, language="ko")
        return result


def process_audio_from_videos(video_audio_paths: list):
    """
    Process audio files extracted from videos and save transcriptions.
    Args:
        video_audio_paths (list): List of audio file paths.
    """
    try:
        translator = AudioTranslator()
    
        for audio_path in video_audio_paths:
            # Get file name without extension
            output_file = f"video/all_text_original.txt"
            
            # Transcribe and save
            print(f"Processing audio: {audio_path}")
            result = translator.audio_to_text(audio_path)
            df = pd.DataFrame(result["segments"])[["id", "start", "end", "text"]]
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result["text"])
            df.to_csv("video/segments.csv", index=False)
            refiner = summarizer()
            query = """당신은 오타를 교정하는 전문가입니다.
                        주어진 Text의 오타를 알맞게 교정한 Text를 내보내 주세요."""
            output_file = f"video/all_text_refined.txt"
            response = refiner.generate(result['text'], query)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(response)
    except Exception as e:
        raise Exception(f"오디오 처리 중 오류 발생: {str(e)}")


if __name__ == "__main__":
    # video_processing.py에서 제공하는 오디오 파일 경로 리스트를 여기에 사용
    video_audio_paths = [glob("./video/*.mp3")[0]]

    process_audio_from_videos(video_audio_paths)
    print("\nAll audio files have been transcribed and saved.")

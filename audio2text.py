import whisper
from pydub import AudioSegment
import os

class AudioTranslator:
    def __init__(self, model_name='base'):
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
        wav_path = audio_path.replace('.mp3', '.wav')
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
        if audio_path.endswith('.mp3'):
            audio_path = self.mp3_to_wav(audio_path)
        
        result = self.model.transcribe(audio_path, language='ko')
        return result['text']

def save_text(text: str, output_file: str):
    """
    Save the transcribed text to a .txt file.
    Args:
        text (str): Transcribed text.
        output_file (str): Path to the output .txt file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved transcription to {output_file}")

def process_audio_from_videos(video_audio_paths: list):
    """
    Process audio files extracted from videos and save transcriptions.
    Args:
        video_audio_paths (list): List of audio file paths.
    """
    translator = AudioTranslator()

    for audio_path in video_audio_paths:
        # Get file name without extension
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        output_file = f"{base_name}_transcription.txt"

        # Transcribe and save
        print(f"Processing audio: {audio_path}")
        text = translator.audio_to_text(audio_path)
        save_text(text, output_file)

if __name__ == "__main__":
    # video_processing.py에서 제공하는 오디오 파일 경로 리스트를 여기에 사용
    video_audio_paths = [
        "/Users/jeong-yujin/Desktop/SumClip/videos/video_1/video_1_audio.mp3"
    ]
    
    process_audio_from_videos(video_audio_paths)
    print("\nAll audio files have been transcribed and saved.")

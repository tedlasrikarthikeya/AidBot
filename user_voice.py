import os
import whisper

# Ensure ffmpeg path
os.environ["PATH"] += os.pathsep + r"C:\Users\tedla\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin"

model = whisper.load_model("base")

def transcribe_with_whisper(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]

import whisper
import subprocess
import os

model = whisper.load_model("tiny")

def convert_ogg_to_wav(input_path: str) -> str:
    wav_path = input_path.rsplit(".", 1)[0] + ".wav"

    subprocess.run([
        "ffmpeg",
        "-y",              # sobrescribe si existe
        "-i", input_path,
        wav_path
    ])

    return wav_path

def transcribe_audio(file_path: str) -> str:
    result = model.transcribe(file_path, language="es")
    return result["text"]
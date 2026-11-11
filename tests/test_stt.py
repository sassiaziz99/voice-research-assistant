import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

AUDIO_PATH = "audio_samples/sample.wav"


def transcribe(path: str) -> str:
    with open(path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=audio_file,
        )
    return transcript.text


if __name__ == "__main__":
    print("Starting transcription...")
    text = transcribe(AUDIO_PATH)
    print("Transcribed text:")
    print(text)


            
    
        
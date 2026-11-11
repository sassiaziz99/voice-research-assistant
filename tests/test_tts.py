import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import soundfile as sf
import sounddevice as sd
import io

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

OUTPUT_PATH = "audio_samples/tts_output.mp3"


def speak(text: str):
    audio_stream = client.text_to_speech.convert(
        voice_id = VOICE_ID,
        text = text,
        model_id = "eleven_turbo_v2_5",
        output_format = "mp3_44100_128",
    )
    
    audio_bytes = b"".join(audio_stream)
    
    with open (OUTPUT_PATH, "wb") as f:
        f.write(audio_bytes)
    print(f"saved audio to {OUTPUT_PATH}")
    
    data, samplerate = sf.read(io.BytesIO(audio_bytes))
    sd.play(data, samplerate)
    sd.wait()
    

if __name__ == "__main__":
    speak("hello aziz! I am here to help you.")


import sounddevice as sd
import soundfile as sf

DURATION_SECONDS = 5
SAMPLE_RATE = 16000
OUTPUT_PATH = "audio_samples/sample.wav"


def record():
    print(f"Recording for {DURATION_SECONDS} seconds... speak now.")
    audio = sd.rec(
        int(DURATION_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    sf.write(OUTPUT_PATH, audio, SAMPLE_RATE)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    record()

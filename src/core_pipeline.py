import os
from dotenv import load_dotenv
from tavily import TavilyClient
from groq import Groq
from elevenlabs.client import ElevenLabs
import soundfile as sf
import sounddevice as sd
import io

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

SYSTEM_PROMPT = (
    "You are a voice research assistant. You will be given a user's "
    "question and a set of web search results. Synthesize a short, "
    "spoken-style answer (2-4 sentences) based ONLY on the search "
    "results provided below. Do NOT use your own prior knowledge or "
    "training data to answer -- rely strictly on the search results, "
    "since they are more current than your training. If the search "
    "results do not clearly answer the question, say honestly that "
    "you could not find a clear recent answer. Speak like you are "
    "talking to someone out loud, not writing a report. No markdown, "
    "no bullet points, no headers, no citations like [1]."
)

def search_web(query: str) -> str:
    print("searching the web...")
    response = tavily_client.search(
        query=query, 
        search_depth="advanced",
        topic = "news",
        days = 14,
        max_results=5, 
        include_answer=True,
    )
    
    context_parts = []
    for item in response["results"]:
        context_parts.append(f"{item['title']}: {item['content']}")
    return "\n\n".join(context_parts)

def synthesize_answer(question: str, search_context: str) ->str:
    print("thinking...")
    user_message = (
        f"question: {question}\n\n"
        f"search results:\n{search_context}"
    )
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message },
        ],
        temperature=0.5,
        max_tokens=250,
    )
    return response.choices[0].message.content

def speak(text: str):
    print("generating speech...")
    audio_stream = eleven_client.text_to_speech.convert(
        voice_id = VOICE_ID,
        text = text,
        model_id = "eleven_turbo_v2_5",
        output_format = "mp3_44100_128",
    )
    audio_bytes = b"".join(audio_stream)
    
    data, samplerate = sf.read(io.BytesIO(audio_bytes))
    sd.play(data, samplerate)
    sd.wait()
    

def run_pipeline(question: str):
    print(f"question: {question}")
    
    search_context = search_web(question)
    answer = synthesize_answer(question, search_context)
    
    print("\nAnswer:")
    print(answer)
    print()
    
    speak(answer)
    

    
if __name__ == "__main__":
    question = input("ask your question: ")
    run_pipeline(question)
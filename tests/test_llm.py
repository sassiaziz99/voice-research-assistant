import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = (
    "You are a voice assistant. Answer in 2-3 short spoken-style "
    "sentences, like you are talking to someone out loud, not writing "
    "a report. No markdown, no bullet points, no headers."
)


def ask(question: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0.5,
        max_tokens=200,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    answer = ask("Who won the world cup 2022?")
    print("LLM response:")
    print(answer)

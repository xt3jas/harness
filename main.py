import os

from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

load_dotenv()

SYSTEM_PROMPT = (Path(__file__).parent / "prompts" / "system.md").read_text(
    encoding="utf-8"
)

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

user_input = input("Enter a prompt: ")
response = client.chat.completions.create(
    model=os.getenv("OPENROUTER_MODEL"),
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ],
)
print("Response:", response.choices[0].message.content)

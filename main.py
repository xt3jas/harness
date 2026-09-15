import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

user_input = input("Enter a prompt: ")
response = client.chat.completions.create(
    model=os.getenv("OPENROUTER_MODEL"),
    messages=[{"role": "user", "content": user_input}],
)
print(response.choices[0].message.content)

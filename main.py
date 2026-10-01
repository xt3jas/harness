import os
import subprocess

from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from tools import tool_registry

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
    tools=tool_registry.TOOLS,
)

def bash(command):
    result = subprocess.run(command, shell = True, capture_output=True, text=True)
    return result.stdout + result.stderr


print("Response:", response.choices[0].message.content)

usage_info = response.usage
completion_details = getattr(usage_info, "completion_tokens_details", None)

usage = {
    "prompt_tokens": getattr(usage_info, "prompt_tokens", None),
    "completion_tokens": getattr(usage_info, "completion_tokens", None),
    "reasoning_tokens": getattr(completion_details, "reasoning_tokens", None),
}

print(usage)

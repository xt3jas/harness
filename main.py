import json
import os

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

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": input("Enter a prompt: ")},
]

while True:
    response = client.chat.completions.create(
        model=os.getenv("OPENROUTER_MODEL"),
        messages=messages,
        tools=tool_registry.TOOLS,
    )
    message = response.choices[0].message if response.choices else None
    if not message or not message.tool_calls:
        break

    messages.append(message)
    for tool_call in message.tool_calls:
        arguments = json.loads(tool_call.function.arguments or "{}")
        handler = tool_registry.HANDLERS.get(tool_call.function.name)
        output = handler(**arguments) if handler else f"Unknown tool: {tool_call.function.name}"
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": output,
            }
        )

print("Response:", message.content if message else response)

usage_info = response.usage
completion_details = getattr(usage_info, "completion_tokens_details", None)

usage = {
    "prompt_tokens": getattr(usage_info, "prompt_tokens", None),
    "completion_tokens": getattr(usage_info, "completion_tokens", None),
    "reasoning_tokens": getattr(completion_details, "reasoning_tokens", None),
}

print(usage)

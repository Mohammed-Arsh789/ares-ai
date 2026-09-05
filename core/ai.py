import os
from ollama import chat


class AIClient:
    def __init__(self, model=None):
        self.model = model or os.getenv(
            "ARES_MODEL",
            "qwen2.5:1.5b"
        )

    def ask(self, message, system_prompt=None):
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": message
        })

        response = chat(
            model=self.model,
            messages=messages
        )

        return response.message.content
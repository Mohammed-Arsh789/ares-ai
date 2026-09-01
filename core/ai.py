from ollama import chat

from core.persona import ARES_SYSTEM_PROMPT


class AIClient:
    def __init__(self):
        self.model = "gemma3:4b"

        self.messages = [
            {
                "role": "system",
                "content": ARES_SYSTEM_PROMPT,
            }
        ]

    def ask(self, message):
        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        response = chat(
            model=self.model,
            messages=self.messages,
        )

        answer = response.message.content

        self.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        return answer
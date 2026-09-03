from ollama import chat

from core.persona import ARES_SYSTEM_PROMPT


class AIClient:
    def __init__(self, model="gemma3:4b"):
        self.model = model

        self.messages = [
            {
                "role": "system",
                "content": ARES_SYSTEM_PROMPT,
            }
        ]

    def ask(self, message):
        if not message or not message.strip():
            return "I'm listening."

        self.messages.append(
            {
                "role": "user",
                "content": message.strip(),
            }
        )

        try:
            response = chat(
                model=self.model,
                messages=self.messages,
            )

            answer = response.message.content.strip()

        except Exception as error:
            # Remove failed user message so the history stays clean.
            self.messages.pop()

            return f"I couldn't reach my local AI model: {error}"

        self.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        # Keep system prompt + recent conversation.
        if len(self.messages) > 21:
            self.messages = [
                self.messages[0]
            ] + self.messages[-20:]

        return answer

    def clear_context(self):
        self.messages = [
            {
                "role": "system",
                "content": ARES_SYSTEM_PROMPT,
            }
        ]

    def conversation(self):
        return list(self.messages)
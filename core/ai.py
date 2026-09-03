from ollama import chat

from core.config import OLLAMA_MODEL, MAX_MESSAGES
from core.personality import ARES_SYSTEM_PROMPT
from core.emotion import EmotionAnalyzer


class AIClient:

    def __init__(self):

        self.model = OLLAMA_MODEL
        self.messages = []
        self.emotion_analyzer = EmotionAnalyzer()

    def reset(self):
        self.messages = []

    def _trim_history(self):

        if len(self.messages) > MAX_MESSAGES:
            self.messages = self.messages[-MAX_MESSAGES:]

    def ask(self, message):

        emotion = self.emotion_analyzer.analyze(message)

        emotion_context = (
            f"\nPossible conversational tone: {emotion['emotion']}."
            "\nThis is only a weak signal. Do not claim certainty."
        )

        self.messages.append({
            "role": "user",
            "content": message
        })

        self._trim_history()

        messages = [
            {
                "role": "system",
                "content": ARES_SYSTEM_PROMPT + emotion_context
            }
        ]

        messages.extend(self.messages)

        try:

            response = chat(
                model=self.model,
                messages=messages
            )

            answer = response.message.content

            self.messages.append({
                "role": "assistant",
                "content": answer
            })

            self._trim_history()

            return answer

        except Exception as error:

            return f"ARES encountered an AI error: {error}"
from ollama import chat


class AIClient:
    def __init__(self):
        self.model = "gemma4"

    def ask(self, message):
        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response.message.content
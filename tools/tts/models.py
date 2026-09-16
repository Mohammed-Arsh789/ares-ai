from dataclasses import dataclass


@dataclass
class SpeechRequest:
    """
    Represents a text-to-speech request.
    """

    text: str
    voice: str = "default"
    speed: float = 1.0
    volume: float = 1.0

    def __post_init__(self):
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")

        self.text = self.text.strip()

        if not self.text:
            raise ValueError("text cannot be empty")

        if self.speed <= 0:
            raise ValueError("speed must be greater than 0")

        if self.volume < 0 or self.volume > 1:
            raise ValueError("volume must be between 0 and 1")
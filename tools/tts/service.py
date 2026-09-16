from .engine import TTSEngine, UnavailableTTSEngine
from .models import SpeechRequest


class TTSService:
    """
    High-level service for text-to-speech operations.
    """

    def __init__(self, engine: TTSEngine | None = None):
        self.engine = engine or UnavailableTTSEngine()

    def speak(
        self,
        text: str,
        voice: str = "default",
        speed: float = 1.0,
        volume: float = 1.0,
    ):
        request = SpeechRequest(
            text=text,
            voice=voice,
            speed=speed,
            volume=volume,
        )

        return self.engine.synthesize(request)
from abc import ABC, abstractmethod

from .models import SpeechRequest


class TTSEngine(ABC):
    """
    Abstract interface for text-to-speech engines.
    """

    @abstractmethod
    def synthesize(self, request: SpeechRequest):
        """
        Convert speech text into audio or an engine-specific result.
        """
        raise NotImplementedError


class UnavailableTTSEngine(TTSEngine):
    """
    Safe fallback when no actual TTS engine is installed.
    """

    def synthesize(self, request: SpeechRequest):
        raise RuntimeError(
            "No text-to-speech engine is currently configured."
        )
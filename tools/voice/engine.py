"""
ARES Speech-to-Text Engine
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .models import Transcript


class STTEngine(ABC):

    @abstractmethod
    def transcribe(
        self,
        audio_path: str,
    ) -> Transcript:
        raise NotImplementedError


class UnavailableSTTEngine(STTEngine):

    def transcribe(
        self,
        audio_path: str,
    ) -> Transcript:

        raise RuntimeError(
            "No STT engine is configured."
        )


class STTService:

    def __init__(
        self,
        engine: STTEngine | None = None,
    ):

        self.engine = (
            engine
            or UnavailableSTTEngine()
        )

    def transcribe(
        self,
        audio_path: str,
    ) -> Transcript:

        if not audio_path:
            raise ValueError(
                "Audio path cannot be empty."
            )

        return self.engine.transcribe(
            audio_path
        )
from __future__ import annotations

from abc import ABC, abstractmethod

from .models import OCRResult


class OCREngine(ABC):

    @abstractmethod
    def extract(
        self,
        image_path: str,
    ) -> OCRResult:
        raise NotImplementedError


class UnavailableOCREngine(OCREngine):

    def extract(
        self,
        image_path: str,
    ) -> OCRResult:

        raise RuntimeError(
            "No OCR engine configured."
        )


class OCRService:

    def __init__(
        self,
        engine: OCREngine | None = None,
    ):

        self.engine = (
            engine
            or UnavailableOCREngine()
        )

    def extract(
        self,
        image_path: str,
    ) -> OCRResult:

        return self.engine.extract(
            image_path
        )
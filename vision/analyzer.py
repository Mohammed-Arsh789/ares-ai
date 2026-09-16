from __future__ import annotations

from .image_loader import ImageLoader
from .ocr import OCRService


class VisionAnalyzer:

    def __init__(
        self,
        ocr: OCRService | None = None,
    ):

        self.loader = ImageLoader()

        self.ocr = (
            ocr
            or OCRService()
        )

    def inspect(
        self,
        path: str,
        extract_text: bool = False,
    ):

        image = self.loader.load(
            path
        )

        result = {
            "image":
                image.to_dict(),

            "ocr":
                None,
        }

        if extract_text:

            result["ocr"] = (
                self.ocr
                .extract(path)
                .to_dict()
            )

        return result
from __future__ import annotations

from .image_loader import ImageLoader


class ScreenshotAnalyzer:

    def __init__(self):

        self.loader = ImageLoader()

    def inspect(
        self,
        path: str,
    ):

        image = self.loader.load(
            path
        )

        return {
            "type": "screenshot",
            "image": image.to_dict(),
        }
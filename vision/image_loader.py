from __future__ import annotations

from pathlib import Path

from .models import ImageInfo


class ImageLoader:

    def load(
        self,
        path: str,
    ) -> ImageInfo:

        file_path = Path(path)

        if not file_path.exists():

            raise FileNotFoundError(
                f"Image not found: {path}"
            )

        if not file_path.is_file():

            raise ValueError(
                "Path is not a file."
            )

        try:

            from PIL import Image

        except ImportError as exc:

            raise RuntimeError(
                "Pillow is required for image loading."
            ) from exc

        with Image.open(
            file_path
        ) as image:

            return ImageInfo(
                path=str(
                    file_path.resolve()
                ),
                width=image.width,
                height=image.height,
                mode=image.mode,
                metadata=dict(
                    image.info
                ),
            )
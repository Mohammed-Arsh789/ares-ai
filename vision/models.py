from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ImageInfo:

    path: str

    width: int

    height: int

    mode: str

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self):

        return {
            "path": self.path,
            "width": self.width,
            "height": self.height,
            "mode": self.mode,
            "metadata": self.metadata,
        }


@dataclass
class OCRResult:

    text: str

    confidence: float | None = None

    boxes: list[dict[str, Any]] = field(
        default_factory=list
    )

    def to_dict(self):

        return {
            "text": self.text,
            "confidence": self.confidence,
            "boxes": self.boxes,
        }
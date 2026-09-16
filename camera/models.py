from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CameraConfig:

    device_index: int = 0

    width: int = 1280

    height: int = 720

    fps: int = 30


@dataclass
class Frame:

    data: object

    width: int

    height: int

    timestamp: float
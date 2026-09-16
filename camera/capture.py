from __future__ import annotations

import time

from .models import Frame


class CameraCapture:

    def __init__(
        self,
        device,
    ):

        self.device = device

    def capture_frame(self) -> Frame:

        if not self.device.opened:

            raise RuntimeError(
                "Camera is not open."
            )

        success, frame = (
            self.device.capture.read()
        )

        if not success:

            raise RuntimeError(
                "Failed to capture frame."
            )

        height, width = (
            frame.shape[:2]
        )

        return Frame(
            data=frame,
            width=width,
            height=height,
            timestamp=time.time(),
        )
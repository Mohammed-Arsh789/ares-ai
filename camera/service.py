from __future__ import annotations

from .capture import CameraCapture
from .device import CameraDevice


class CameraService:

    def __init__(
        self,
        device=None,
    ):

        self.device = (
            device
            or CameraDevice()
        )

        self.capture = (
            CameraCapture(
                self.device
            )
        )

    def start(self):

        self.device.open()

    def snapshot(self):

        return self.capture.capture_frame()

    def stop(self):

        self.device.close()
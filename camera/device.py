from __future__ import annotations

from .models import CameraConfig


class CameraDevice:

    def __init__(
        self,
        config: CameraConfig | None = None,
    ):

        self.config = (
            config
            or CameraConfig()
        )

        self.opened = False

    def open(self):

        if self.opened:
            return

        try:

            import cv2

        except ImportError as exc:

            raise RuntimeError(
                "OpenCV is required for camera access."
            ) from exc

        self.capture = cv2.VideoCapture(
            self.config.device_index
        )

        if not self.capture.isOpened():

            raise RuntimeError(
                "Unable to open camera."
            )

        self.capture.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            self.config.width,
        )

        self.capture.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            self.config.height,
        )

        self.capture.set(
            cv2.CAP_PROP_FPS,
            self.config.fps,
        )

        self.opened = True

    def close(self):

        if hasattr(
            self,
            "capture",
        ):

            self.capture.release()

        self.opened = False
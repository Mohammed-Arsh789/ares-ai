from pathlib import Path

import cv2


class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.camera = None

    def open(self):
        self.camera = cv2.VideoCapture(
            self.camera_index
        )

        if not self.camera.isOpened():
            raise RuntimeError(
                "Could not open the camera."
            )

    def capture(self, output_path="data/capture.jpg"):
        if self.camera is None:
            self.open()

        success, frame = self.camera.read()

        if not success:
            raise RuntimeError(
                "Could not capture an image."
            )

        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cv2.imwrite(
            str(path),
            frame,
        )

        return str(path)

    def close(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None
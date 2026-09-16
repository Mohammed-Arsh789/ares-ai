"""
ARES Microphone Abstraction

Actual hardware access is kept behind this class.
"""

from __future__ import annotations


class Microphone:

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
    ):

        if sample_rate <= 0:
            raise ValueError(
                "sample_rate must be positive."
            )

        if channels <= 0:
            raise ValueError(
                "channels must be positive."
            )

        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False

    def start(self):
        if self.recording:
            raise RuntimeError(
                "Microphone is already recording."
            )

        self.recording = True

    def stop(self):
        if not self.recording:
            return

        self.recording = False
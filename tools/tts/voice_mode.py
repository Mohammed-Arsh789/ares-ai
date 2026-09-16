from __future__ import annotations

from enum import Enum


class VoiceModeState(str, Enum):

    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"


class VoiceMode:

    def __init__(
        self,
        stt,
        tts,
    ):

        self.stt = stt
        self.tts = tts
        self.state = VoiceModeState.IDLE

    def start(self):

        self.state = (
            VoiceModeState.LISTENING
        )

    def stop(self):

        self.state = (
            VoiceModeState.IDLE
        )

    def status(self):

        return self.state.value
"""
ARES Voice Session
"""

from __future__ import annotations

from enum import Enum


class VoiceState(str, Enum):

    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    STOPPED = "stopped"


class VoiceSession:

    def __init__(self):

        self.state = VoiceState.IDLE

    def start_listening(self):

        if self.state == VoiceState.SPEAKING:
            raise RuntimeError(
                "Cannot listen while speaking."
            )

        self.state = VoiceState.LISTENING

    def start_processing(self):

        self.state = VoiceState.PROCESSING

    def start_speaking(self):

        self.state = VoiceState.SPEAKING

    def stop(self):

        self.state = VoiceState.STOPPED

    def reset(self):

        self.state = VoiceState.IDLE
class VoiceSessionManager:

    def __init__(self):

        self.session = VoiceSession()

    def interrupt(self):

        self.session.reset()

    def is_active(self):

        return self.session.state in {
            VoiceState.LISTENING,
            VoiceState.PROCESSING,
            VoiceState.SPEAKING,
        }

    def status(self):

        return self.session.state.value
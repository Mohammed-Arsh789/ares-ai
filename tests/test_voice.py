from tools.voice import (
    Microphone,
    Transcript,
    VoiceSession,
    VoiceSessionManager,
    VoiceState,
)


def test_transcript():
    result = Transcript(
        text="hello ARES"
    )

    assert result.text == "hello ARES"


def test_microphone():
    mic = Microphone()

    mic.start()

    assert mic.recording is True

    mic.stop()

    assert mic.recording is False


def test_voice_session():
    session = VoiceSession()

    session.start_listening()

    assert (
        session.state
        == VoiceState.LISTENING
    )

    session.start_processing()

    assert (
        session.state
        == VoiceState.PROCESSING
    )


def test_voice_manager():
    manager = VoiceSessionManager()

    manager.session.start_listening()

    assert manager.is_active()

    manager.interrupt()

    assert not manager.is_active()
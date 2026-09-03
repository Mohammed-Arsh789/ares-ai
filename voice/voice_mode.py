from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech


class VoiceMode:
    def __init__(self, ares):
        self.ares = ares
        self.stt = SpeechToText()
        self.tts = TextToSpeech()

    def speak_response(self, text):
        self.tts.speak(text)

    def run_once(self):
        audio_file = self.stt.record()

        print(
            f"Audio captured: {audio_file}"
        )

        self.tts.speak(
            "I captured your voice, but speech recognition "
            "is not connected yet."
        )
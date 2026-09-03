import tempfile

import sounddevice as sd
import soundfile as sf


class SpeechToText:
    def __init__(
        self,
        sample_rate=16000,
        channels=1,
        duration=5,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.duration = duration

    def record(self):
        print(
            f"Listening for {self.duration} seconds..."
        )

        recording = sd.rec(
            int(
                self.duration
                * self.sample_rate
            ),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
        )

        sd.wait()

        temp = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        )

        temp.close()

        sf.write(
            temp.name,
            recording,
            self.sample_rate,
        )

        return temp.name
class EmotionAnalyzer:

    EMOTION_WORDS = {

        "frustrated": [
            "annoyed",
            "angry",
            "frustrated",
            "ugh",
            "stupid",
            "broken",
            "doesn't work"
        ],

        "excited": [
            "awesome",
            "amazing",
            "lets go",
            "excited",
            "hyped",
            "insane"
        ],

        "confused": [
            "confused",
            "don't understand",
            "what does",
            "how do",
            "why does"
        ],

        "sad": [
            "sad",
            "upset",
            "lonely",
            "terrible day"
        ],

        "curious": [
            "why",
            "how",
            "what if",
            "tell me",
            "explain"
        ]
    }

    def analyze(self, text):

        lowered = text.lower()

        scores = {}

        for emotion, words in self.EMOTION_WORDS.items():

            score = 0

            for word in words:

                if word in lowered:
                    score += 1

            scores[emotion] = score

        strongest = max(scores, key=scores.get)

        if scores[strongest] == 0:
            strongest = "neutral"

        return {
            "emotion": strongest,
            "scores": scores
        }
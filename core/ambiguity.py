"""
ARES Ambiguity Detector
Step 169
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AmbiguityResult:

    ambiguous: bool

    score: float

    reasons: list[str] = field(
        default_factory=list
    )

    clarification_needed: bool = False

    def to_dict(self):

        return {
            "ambiguous": self.ambiguous,
            "score": self.score,
            "reasons": self.reasons,
            "clarification_needed":
                self.clarification_needed,
        }


class AmbiguityDetector:

    def analyze(
        self,
        text: str,
    ) -> AmbiguityResult:

        text = text.strip()

        reasons = []
        score = 0.0

        if not text:

            return AmbiguityResult(
                ambiguous=True,
                score=1.0,
                reasons=[
                    "No request provided."
                ],
                clarification_needed=True,
            )

        words = text.split()

        if len(words) <= 2:

            score += 0.35

            reasons.append(
                "Request is extremely short."
            )

        vague_terms = (
            "it",
            "that",
            "this",
            "there",
            "something",
            "stuff",
            "thing",
            "do it",
            "fix it",
            "open it",
        )

        lowered = text.lower()

        for term in vague_terms:

            if term in lowered:

                score += 0.20

                reasons.append(
                    f"Vague reference detected: {term}"
                )

        if (
            "or" in lowered
            and len(words) < 8
        ):

            score += 0.15

            reasons.append(
                "Multiple possible interpretations."
            )

        score = min(
            score,
            1.0,
        )

        ambiguous = score >= 0.50

        return AmbiguityResult(
            ambiguous=ambiguous,
            score=score,
            reasons=reasons,
            clarification_needed=ambiguous,
        )
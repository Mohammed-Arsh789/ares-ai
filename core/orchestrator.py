"""
ARES Orchestrator
Step 178

Coordinates:
- intent detection
- ambiguity detection
- planning
- routing

No actual dangerous tool execution happens here yet.
"""

from __future__ import annotations

from .ambiguity import AmbiguityDetector
from .intent_detector import IntentDetector
from .router import Router


class Orchestrator:

    def __init__(
        self,
        router: Router,
    ):

        self.intent_detector = (
            IntentDetector()
        )

        self.ambiguity_detector = (
            AmbiguityDetector()
        )

        self.router = router

    def analyze(
        self,
        user_input: str,
    ) -> dict:

        intent = self.intent_detector.detect(
            user_input
        )

        ambiguity = (
            self.ambiguity_detector.analyze(
                user_input
            )
        )

        task = None

        if not ambiguity.clarification_needed:

            task = self.router.route(
                user_input,
                intent,
            )

        return {
            "input": user_input,
            "intent": intent.to_dict(),
            "ambiguity":
                ambiguity.to_dict(),
            "task":
                task.to_dict()
                if task
                else None,
        }
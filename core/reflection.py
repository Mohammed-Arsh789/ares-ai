from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

from .model_router import ModelRouter


logger = logging.getLogger(__name__)


REFLECTION_SYSTEM_PROMPT = """
You are the reflection layer of ARES.

ARES has just attempted an action or generated an answer.

Your job is to evaluate the result and determine what ARES should
tell the user.

Return ONLY valid JSON:

{
  "success": true,
  "response": "final response to user",
  "retry": false,
  "reason": "short explanation",
  "confidence": 0.0
}

Rules:

1. Do not claim success when the result indicates failure.
2. If the action failed, explain that clearly.
3. If a retry could reasonably fix the problem, set retry=true.
4. Keep confidence between 0 and 1.
5. Return JSON only.
""".strip()


@dataclass(slots=True)
class ReflectionResult:
    success: bool
    response: str
    retry: bool = False
    reason: str = ""
    confidence: float = 0.0


class ReflectionEngine:
    """
    Evaluates observations/results after an action or response.
    """

    def __init__(
        self,
        model_router: ModelRouter | None = None,
    ) -> None:
        self.model_router = model_router or ModelRouter()

    def reflect(
        self,
        *,
        user_input: str,
        action: str,
        result: Any,
        context: dict[str, Any] | None = None,
    ) -> ReflectionResult:
        context = context or {}

        prompt = json.dumps(
            {
                "user_input": user_input,
                "action": action,
                "result": result,
                "context": context,
            },
            ensure_ascii=False,
            default=str,
        )

        raw = self.model_router.generate(
            prompt,
            system=REFLECTION_SYSTEM_PROMPT,
        )

        data = self._parse(raw)

        return ReflectionResult(
            success=bool(
                data.get("success", False)
            ),
            response=str(
                data.get("response", "")
            ),
            retry=bool(
                data.get("retry", False)
            ),
            reason=str(
                data.get("reason", "")
            ),
            confidence=self._confidence(
                data.get("confidence", 0.0)
            ),
        )

    @staticmethod
    def _parse(raw: str) -> dict[str, Any]:
        text = raw.strip()

        if text.startswith("```"):
            lines = text.splitlines()[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            text = "\n".join(lines).strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}")

            if start == -1 or end == -1:
                logger.warning(
                    "Reflection model returned invalid JSON."
                )

                return {
                    "success": False,
                    "response": (
                        "I couldn't reliably evaluate "
                        "the result."
                    ),
                    "retry": False,
                    "reason": "invalid reflection output",
                    "confidence": 0.0,
                }

            try:
                data = json.loads(
                    text[start : end + 1]
                )
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "response": (
                        "I couldn't reliably evaluate "
                        "the result."
                    ),
                    "retry": False,
                    "reason": "invalid reflection output",
                    "confidence": 0.0,
                }

        if not isinstance(data, dict):
            return {
                "success": False,
                "response": (
                    "I couldn't reliably evaluate "
                    "the result."
                ),
                "retry": False,
                "reason": "invalid reflection object",
                "confidence": 0.0,
            }

        return data

    @staticmethod
    def _confidence(value: Any) -> float:
        try:
            confidence = float(value)
        except (TypeError, ValueError):
            return 0.0

        return max(
            0.0,
            min(1.0, confidence),
        )
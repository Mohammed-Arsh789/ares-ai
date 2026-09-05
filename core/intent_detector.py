"""
ARES Intent Detector
Step 167

Lightweight first-pass intent detection.

This is NOT the final intelligence layer.
Later the LLM can provide richer intent analysis.

The important thing is that every result has
a predictable structure.
"""

from __future__ import annotations

import re

from .intent import Intent, IntentType


class IntentDetector:

    def detect(self, text: str) -> Intent:

        raw = text.strip()

        if not raw:

            return Intent(
                type=IntentType.UNKNOWN,
                confidence=1.0,
                raw_input=raw,
                reason="Empty input.",
            )

        normalized = raw.lower()

        # -----------------------------
        # Weather
        # -----------------------------

        if any(
            word in normalized
            for word in (
                "weather",
                "temperature",
                "forecast",
                "rain",
                "humidity",
            )
        ):

            return Intent(
                type=IntentType.WEATHER,
                confidence=0.92,
                raw_input=raw,
                requires_tool=True,
                reason="Weather-related request detected.",
            )

        # -----------------------------
        # Web/search
        # -----------------------------

        if any(
            phrase in normalized
            for phrase in (
                "search for",
                "search the web",
                "look up",
                "find online",
                "google",
                "latest news",
                "latest information",
            )
        ):

            return Intent(
                type=IntentType.SEARCH,
                confidence=0.90,
                raw_input=raw,
                requires_tool=True,
                reason="Web-search request detected.",
            )

        # -----------------------------
        # Coding
        # -----------------------------

        if any(
            phrase in normalized
            for phrase in (
                "write code",
                "write a program",
                "debug",
                "fix this code",
                "python code",
                "javascript code",
                "programming",
                "code",
            )
        ):

            return Intent(
                type=IntentType.CODING,
                confidence=0.88,
                raw_input=raw,
                reason="Programming-related request detected.",
            )

        # -----------------------------
        # Files
        # -----------------------------

        if any(
            phrase in normalized
            for phrase in (
                "open file",
                "read file",
                "create file",
                "delete file",
                "rename file",
                "move file",
                "find my file",
                "file",
                "folder",
            )
        ):

            return Intent(
                type=IntentType.FILE_OPERATION,
                confidence=0.86,
                raw_input=raw,
                requires_tool=True,
                reason="File operation detected.",
            )

        # -----------------------------
        # Applications
        # -----------------------------

        if any(
            phrase in normalized
            for phrase in (
                "open chrome",
                "open browser",
                "open vscode",
                "open vs code",
                "launch",
                "start application",
                "open app",
            )
        ):

            return Intent(
                type=IntentType.APPLICATION,
                confidence=0.90,
                raw_input=raw,
                requires_tool=True,
                requires_confirmation=True,
                reason="Application-control request detected.",
            )

        # -----------------------------
        # Study
        # -----------------------------

        if any(
            phrase in normalized
            for phrase in (
                "study",
                "explain this topic",
                "teach me",
                "quiz me",
                "flashcards",
                "homework",
            )
        ):

            return Intent(
                type=IntentType.STUDY,
                confidence=0.82,
                raw_input=raw,
                reason="Study-related request detected.",
            )

        # -----------------------------
        # Research
        # -----------------------------

        if any(
            phrase in normalized
            for phrase in (
                "research",
                "deep dive",
                "investigate",
                "compare sources",
            )
        ):

            return Intent(
                type=IntentType.RESEARCH,
                confidence=0.84,
                raw_input=raw,
                requires_tool=True,
                reason="Research request detected.",
            )

        # -----------------------------
        # Automation
        # -----------------------------

        if any(
            phrase in normalized
            for phrase in (
                "remind me",
                "every day",
                "every week",
                "schedule",
                "automate",
                "when this happens",
            )
        ):

            return Intent(
                type=IntentType.AUTOMATION,
                confidence=0.87,
                raw_input=raw,
                requires_tool=True,
                requires_confirmation=True,
                reason="Automation request detected.",
            )

        # -----------------------------
        # Question
        # -----------------------------

        if (
            normalized.endswith("?")
            or re.match(
                r"^(what|why|how|when|where|who|which|can|could|is|are)\b",
                normalized,
            )
        ):

            return Intent(
                type=IntentType.QUESTION,
                confidence=0.80,
                raw_input=raw,
                reason="Question pattern detected.",
            )

        # -----------------------------
        # Default
        # -----------------------------

        return Intent(
            type=IntentType.CHAT,
            confidence=0.60,
            raw_input=raw,
            reason="General conversational input.",
        )
from __future__ import annotations

import re
from typing import Any, Dict, Optional

from .intent import Intent, IntentName


class IntentDetector:
    """
    Deterministic first-pass intent detector for ARES.

    The detector is intentionally lightweight and offline.
    A future LLM classifier can be connected without changing
    the Intent interface.
    """

    def __init__(self, llm_classifier: Optional[Any] = None) -> None:
        self.llm_classifier = llm_classifier

    def detect(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Intent:
        raw_text = (text or "").strip()
        lowered = raw_text.lower()

        if not raw_text:
            return Intent(
                name=IntentName.UNKNOWN,
                confidence=1.0,
                raw_text=raw_text,
            )

        # ============================================================
        # CALCULATOR
        # ============================================================

        if self._is_calculation(lowered):
            expression = self._extract_calculation(raw_text)

            return self._make(
                IntentName.CALCULATOR,
                raw_text,
                0.98,
                entities={"expression": expression},
                requires_tool=True,
            )

        # ============================================================
        # MEMORY STORE
        # ============================================================

        if self._matches(
            lowered,
            [
                r"^remember ",
                r"^don't forget ",
                r"^do not forget ",
                r"^save this ",
                r"^store this ",
                r"^note that ",
                r"^my name is ",
                r"^i like ",
                r"^i love ",
                r"^i prefer ",
            ],
        ):
            content = self._extract_memory_content(raw_text)

            return self._make(
                IntentName.MEMORY_STORE,
                raw_text,
                0.97,
                entities={"content": content},
                requires_tool=True,
            )

        # ============================================================
        # MEMORY SEARCH
        # ============================================================

        if self._matches(
            lowered,
            [
                r"what do you remember",
                r"what did i tell you",
                r"do you remember",
                r"recall ",
                r"search my memory",
                r"my memories",
                r"what do you know about me",
            ],
        ):
            return self._make(
                IntentName.MEMORY_SEARCH,
                raw_text,
                0.96,
                requires_tool=True,
            )

        # ============================================================
        # WEATHER
        # ============================================================

        if self._matches(
            lowered,
            [
                r"\bweather\b",
                r"\btemperature\b",
                r"\bforecast\b",
                r"\brain today\b",
                r"\bhot outside\b",
                r"\bcold outside\b",
            ],
        ):
            location = self._extract_location(raw_text)

            return self._make(
                IntentName.WEATHER,
                raw_text,
                0.96,
                entities={"location": location} if location else {},
                requires_tool=True,
            )

        # ============================================================
        # WEB FETCH
        # ============================================================

        if re.search(r"https?://", lowered) or self._matches(
            lowered,
            [
                r"open this link",
                r"read this webpage",
                r"fetch this page",
                r"visit this url",
            ],
        ):
            return self._make(
                IntentName.WEB_FETCH,
                raw_text,
                0.95,
                entities={"url": self._extract_url(raw_text)},
                requires_tool=True,
            )

        # ============================================================
        # WEB SEARCH
        # ============================================================

        if self._matches(
            lowered,
            [
                r"^search ",
                r"^google ",
                r"^look up ",
                r"^find online ",
                r"search the web",
                r"on the internet",
                r"latest news",
                r"latest information",
            ],
        ):
            query = self._extract_web_query(raw_text)

            return self._make(
                IntentName.WEB_SEARCH,
                raw_text,
                0.95,
                entities={"query": query},
                requires_tool=True,
            )

        # ============================================================
        # OPEN APPLICATION
        # ============================================================

        if self._matches(
            lowered,
            [
                r"^open ",
                r"^launch ",
                r"^start ",
                r"run application",
                r"open an app",
            ],
        ):
            app_name = self._extract_app_name(raw_text)

            return self._make(
                IntentName.OPEN_APP,
                raw_text,
                0.97,
                entities={"application": app_name},
                target=app_name,
                requires_tool=True,
            )

        # ============================================================
        # FILE OPERATIONS
        # ============================================================

        if self._matches(
            lowered,
            [
                r"\bcreate a file\b",
                r"\bdelete a file\b",
                r"\bmove a file\b",
                r"\bcopy a file\b",
                r"\brename a file\b",
                r"\blist files\b",
                r"\bfind a file\b",
                r"\bopen file\b",
                r"\bread file\b",
                r"\bsave file\b",
            ],
        ):
            return self._make(
                IntentName.FILE_OPERATION,
                raw_text,
                0.92,
                requires_tool=True,
                requires_confirmation=any(
                    word in lowered
                    for word in [
                        "delete",
                        "remove",
                        "overwrite",
                    ]
                ),
            )

        # ============================================================
        # DOCUMENT ANALYSIS
        # ============================================================

        if self._matches(
            lowered,
            [
                r"\bsummarize this document\b",
                r"\banalyze this pdf\b",
                r"\bread this document\b",
                r"\bextract text\b",
                r"\bextract information\b",
                r"\bwhat does this document say\b",
            ],
        ):
            return self._make(
                IntentName.DOCUMENT_ANALYSIS,
                raw_text,
                0.93,
                requires_tool=True,
            )

        # ============================================================
        # VISION
        # ============================================================

        if self._matches(
            lowered,
            [
                r"\bwhat is in this image\b",
                r"\banalyze this image\b",
                r"\blook at this picture\b",
                r"\bidentify this object\b",
                r"\bwhat do you see\b",
                r"\buse the camera\b",
            ],
        ):
            return self._make(
                IntentName.VISION,
                raw_text,
                0.93,
                requires_tool=True,
            )

        # ============================================================
        # CODING
        # ============================================================

        if self._matches(
            lowered,
            [
                r"\bwrite code\b",
                r"\bcreate a program\b",
                r"\bdebug this\b",
                r"\bfix this code\b",
                r"\bprogramming\b",
                r"\bpython code\b",
                r"\bexplain this code\b",
                r"\binspect this project\b",
                r"\bsoftware project\b",
            ],
        ):
            return self._make(
                IntentName.CODING,
                raw_text,
                0.93,
                requires_tool=False,
            )

        # ============================================================
        # RESEARCH
        # ============================================================

        if self._matches(
            lowered,
            [
                r"^research ",
                r"\bdeep research\b",
                r"\binvestigate ",
                r"\bprovide a detailed report\b",
                r"\bcompare scientific studies\b",
                r"\bresearch this topic\b",
            ],
        ):
            return self._make(
                IntentName.RESEARCH,
                raw_text,
                0.92,
                requires_tool=True,
            )

        # ============================================================
        # STUDY
        #
        # IMPORTANT:
        # Specific study phrases are checked before generic HELP.
        # ============================================================

        if self._matches(
            lowered,
            [
                r"\bhelp me study\b",
                r"\bteach me\b",
                r"\bexplain this concept\b",
                r"\bmake flashcards\b",
                r"\bcreate a quiz\b",
                r"\bstudy plan\b",
                r"\bstudy\b",
                r"\blearn ",
            ],
        ):
            return self._make(
                IntentName.STUDY,
                raw_text,
                0.96,
                requires_tool=False,
            )

        # ============================================================
        # REVIEW
        # ============================================================

        if self._matches(
            lowered,
            [
                r"\breview this\b",
                r"\bcritique this\b",
                r"\bcheck my answer\b",
                r"\bevaluate this\b",
                r"\bfind mistakes\b",
                r"\bproofread this\b",
            ],
        ):
            return self._make(
                IntentName.REVIEW,
                raw_text,
                0.91,
                requires_tool=False,
            )

        # ============================================================
        # AUTOMATION
        # ============================================================

        if self._matches(
            lowered,
            [
                r"\bremind me\b",
                r"\bset a reminder\b",
                r"\bschedule ",
                r"\bautomate ",
                r"\bevery day\b",
                r"\bevery week\b",
                r"\bwhen .* then\b",
            ],
        ):
            return self._make(
                IntentName.AUTOMATION,
                raw_text,
                0.90,
                requires_tool=True,
                requires_confirmation=True,
            )

        # ============================================================
        # WORKSPACE
        # ============================================================

        if self._matches(
            lowered,
            [
                r"\bcreate workspace\b",
                r"\bopen workspace\b",
                r"\bworkspace\b",
                r"\bproject context\b",
                r"\bworking on project\b",
            ],
        ):
            return self._make(
                IntentName.WORKSPACE,
                raw_text,
                0.88,
                requires_tool=True,
            )

        # ============================================================
        # PLUGINS
        # ============================================================

        if self._matches(
            lowered,
            [
                r"\binstall plugin\b",
                r"\bconnect plugin\b",
                r"\bavailable plugins\b",
                r"\bplugin system\b",
                r"\bconnect an app\b",
            ],
        ):
            return self._make(
                IntentName.PLUGIN,
                raw_text,
                0.90,
                requires_tool=True,
                requires_confirmation=True,
            )

        # ============================================================
        # GENERIC HELP
        #
        # This comes AFTER STUDY intentionally.
        # ============================================================

        if self._matches(
            lowered,
            [
                r"^help$",
                r"^help me$",
                r"^help me with (ares|this)$",
                r"what can you do",
                r"your capabilities",
                r"available commands",
            ],
        ):
            return self._make(
                IntentName.HELP,
                raw_text,
                0.98,
                requires_tool=False,
            )

        # ============================================================
        # CONVERSATION FALLBACK
        # ============================================================

        return self._make(
            IntentName.CONVERSATION,
            raw_text,
            0.70,
            requires_tool=False,
        )

    def classify(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Intent:
        return self.detect(text, context)

    def __call__(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Intent:
        return self.detect(text, context)

    @staticmethod
    def _matches(text: str, patterns: list[str]) -> bool:
        return any(re.search(pattern, text) for pattern in patterns)

    @staticmethod
    def _make(
        name: IntentName,
        raw_text: str,
        confidence: float,
        entities: Optional[Dict[str, Any]] = None,
        requires_tool: bool = False,
        requires_confirmation: bool = False,
        target: Optional[str] = None,
    ) -> Intent:
        return Intent(
            name=name,
            confidence=confidence,
            raw_text=raw_text,
            entities=entities or {},
            requires_tool=requires_tool,
            requires_confirmation=requires_confirmation,
            target=target,
        )

    @staticmethod
    def _is_calculation(text: str) -> bool:
        if text.startswith(
            (
                "calculate ",
                "calc ",
                "compute ",
                "solve ",
            )
        ):
            return True

        return bool(
            re.search(
                r"\d+\s*[\+\-\*/x×÷\^]\s*\d+",
                text,
            )
        )

    @staticmethod
    def _extract_calculation(text: str) -> str:
        cleaned = re.sub(
            r"^(calculate|calc|compute|solve)\s*",
            "",
            text,
            flags=re.IGNORECASE,
        ).strip()

        return cleaned or text

    @staticmethod
    def _extract_memory_content(text: str) -> str:
        lowered = text.lower()

        prefixes = [
            "remember that ",
            "remember ",
            "don't forget that ",
            "do not forget that ",
            "save this ",
            "store this ",
            "note that ",
        ]

        for prefix in prefixes:
            if lowered.startswith(prefix):
                return text[len(prefix):].strip()

        return text.strip()

    @staticmethod
    def _extract_location(text: str) -> Optional[str]:
        match = re.search(
            r"\b(?:in|at|for|near)\s+([A-Za-z][A-Za-z\s,.-]{1,50})",
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return match.group(1).strip(" .,")

        return None

    @staticmethod
    def _extract_web_query(text: str) -> str:
        cleaned = re.sub(
            r"^(search the web for|search for|search|google|look up|find online)\s*",
            "",
            text,
            flags=re.IGNORECASE,
        ).strip()

        return cleaned or text

    @staticmethod
    def _extract_url(text: str) -> Optional[str]:
        match = re.search(
            r"https?://\S+",
            text,
        )

        if match:
            return match.group(0).rstrip(".,)")

        return None

    @staticmethod
    def _extract_app_name(text: str) -> str:
        cleaned = re.sub(
            r"^(open|launch|start)\s+",
            "",
            text,
            flags=re.IGNORECASE,
        ).strip()

        cleaned = re.sub(
            r"^(the\s+)?(application|app)\s+",
            "",
            cleaned,
            flags=re.IGNORECASE,
        ).strip()

        return cleaned


def detect_intent(
    text: str,
    context: Optional[Dict[str, Any]] = None,
) -> Intent:
    """
    Module-level compatibility helper.
    """
    return IntentDetector().detect(text, context)
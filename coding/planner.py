"""
ARES Coding Task Planner

Deterministic classification of coding requests.
"""

from __future__ import annotations

from .models import CodingRequest, CodingTaskType


class CodingTaskPlanner:
    """
    Lightweight deterministic planner for coding tasks.

    Explicit task-specific language takes priority over
    generic words such as inspect or check.
    """

    KEYWORDS = {
        CodingTaskType.CREATE: {
            "create",
            "build",
            "generate",
            "make",
            "implement",
        },
        CodingTaskType.DEBUG: {
            "debug",
            "fix",
            "error",
            "exception",
            "traceback",
            "broken",
        },
        CodingTaskType.REVIEW: {
            "review",
            "inspect",
            "audit",
            "check code",
        },
        CodingTaskType.EXPLAIN: {
            "explain",
            "what does",
            "understand",
            "walk me through",
        },
        CodingTaskType.REFACTOR: {
            "refactor",
            "clean up",
            "restructure",
            "improve structure",
        },
        CodingTaskType.TEST: {
            "test",
            "pytest",
            "unit test",
            "testing",
        },
        CodingTaskType.MODIFY: {
            "change",
            "update",
            "modify",
            "edit",
        },
    }

    # Higher priority wins when multiple categories match.
    PRIORITY = [
        CodingTaskType.DEBUG,
        CodingTaskType.EXPLAIN,
        CodingTaskType.REFACTOR,
        CodingTaskType.TEST,
        CodingTaskType.CREATE,
        CodingTaskType.MODIFY,
        CodingTaskType.REVIEW,
    ]

    def classify(
        self,
        instruction: str,
    ) -> CodingTaskType:

        if not isinstance(instruction, str):
            raise TypeError(
                "instruction must be a string"
            )

        lowered = instruction.lower().strip()

        if not lowered:
            return CodingTaskType.MODIFY

        scores: dict[CodingTaskType, int] = {}

        for task_type, keywords in self.KEYWORDS.items():

            score = sum(
                1
                for keyword in keywords
                if keyword in lowered
            )

            if score:
                scores[task_type] = score

        if not scores:
            return CodingTaskType.MODIFY

        highest_score = max(scores.values())

        candidates = {
            task_type
            for task_type, score in scores.items()
            if score == highest_score
        }

        for task_type in self.PRIORITY:

            if task_type in candidates:
                return task_type

        return CodingTaskType.MODIFY

    def create_request(
        self,
        instruction: str,
        project_path: str | None = None,
        target_files: list[str] | None = None,
    ) -> CodingRequest:

        return CodingRequest(
            instruction=instruction,
            project_path=project_path,
            task_type=self.classify(instruction),
            target_files=target_files or [],
        )
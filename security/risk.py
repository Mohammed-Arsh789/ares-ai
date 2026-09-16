"""
ARES Risk Classification
"""

from __future__ import annotations

from enum import IntEnum


class RiskLevel(IntEnum):

    SAFE = 0

    LOW = 10

    MODERATE = 20

    HIGH = 30

    CRITICAL = 40


class RiskAssessment:

    def __init__(
        self,
        level: RiskLevel,
        reason: str = "",
    ):

        self.level = level

        self.reason = reason

    @property
    def requires_confirmation(self) -> bool:

        return self.level >= RiskLevel.HIGH

    def to_dict(self):

        return {
            "level":
                self.level.name,

            "level_value":
                int(self.level),

            "reason":
                self.reason,

            "requires_confirmation":
                self.requires_confirmation,
        }
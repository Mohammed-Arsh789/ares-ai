from .models import (
    CriticIssue,
    CriticReport,
    CriticSeverity,
)
from .rules import CriticRules


class ResponseReviewer:
    def __init__(self):
        self.rules = CriticRules()

    def review(self, text: str) -> CriticReport:
        issues = []
        strengths = []
        score = 100.0

        empty_issue = self.rules.check_empty(text)

        if empty_issue:
            issues.append(
                CriticIssue(
                    category="completeness",
                    message=empty_issue,
                    severity=CriticSeverity.ERROR,
                    suggestion="Generate a meaningful response.",
                )
            )
            score -= 60

        length_issue = self.rules.check_length(text)

        if length_issue:
            issues.append(
                CriticIssue(
                    category="quality",
                    message=length_issue,
                    severity=CriticSeverity.WARNING,
                    suggestion="Add useful explanation or details.",
                )
            )
            score -= 15

        uncertainty_issue = self.rules.check_uncertainty(text)

        if uncertainty_issue:
            issues.append(
                CriticIssue(
                    category="confidence",
                    message=uncertainty_issue,
                    severity=CriticSeverity.WARNING,
                    suggestion="Clearly distinguish facts from assumptions.",
                )
            )
            score -= 10

        if not issues:
            strengths.append(
                "Response passed basic quality checks."
            )

        return CriticReport(
            score=max(0, score),
            approved=score >= 70,
            issues=issues,
            strengths=strengths,
        )
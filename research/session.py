from dataclasses import dataclass, field
from datetime import datetime, timezone

from .models import ResearchReport


@dataclass
class ResearchSession:
    session_id: str
    question: str
    reports: list[ResearchReport] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    def add_report(self, report: ResearchReport):
        self.reports.append(report)

    def latest(self) -> ResearchReport | None:
        if not self.reports:
            return None

        return self.reports[-1]


class ResearchSessionManager:
    def __init__(self):
        self.sessions: dict[str, ResearchSession] = {}

    def create(
        self,
        session_id: str,
        question: str,
    ) -> ResearchSession:
        session = ResearchSession(
            session_id=session_id,
            question=question,
        )

        self.sessions[session_id] = session
        return session

    def get(self, session_id: str) -> ResearchSession | None:
        return self.sessions.get(session_id)
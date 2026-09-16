from dataclasses import dataclass, field
from datetime import datetime, timezone

from .models import CodingResult


@dataclass
class CodingSession:
    """
    Stores lightweight coding-session history.
    """

    session_id: str
    project_path: str | None = None
    history: list[CodingResult] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    def add_result(self, result: CodingResult):
        self.history.append(result)

    def latest(self) -> CodingResult | None:
        if not self.history:
            return None

        return self.history[-1]


class CodingSessionManager:
    def __init__(self):
        self.sessions: dict[str, CodingSession] = {}

    def create(
        self,
        session_id: str,
        project_path: str | None = None,
    ) -> CodingSession:
        session = CodingSession(
            session_id=session_id,
            project_path=project_path,
        )

        self.sessions[session_id] = session
        return session

    def get(self, session_id: str) -> CodingSession | None:
        return self.sessions.get(session_id)

    def remove(self, session_id: str) -> bool:
        return self.sessions.pop(session_id, None) is not None
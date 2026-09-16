from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class AutomationTask:
    task_id: str
    name: str
    action_name: str
    interval_seconds: int | None = None
    enabled: bool = True
    last_run: str | None = None
    run_count: int = 0
    metadata: dict = field(default_factory=dict)

    def mark_run(self):
        self.last_run = datetime.now(
            timezone.utc
        ).isoformat()

        self.run_count += 1
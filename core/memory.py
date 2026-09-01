import json
from pathlib import Path


class Memory:
    def __init__(self, file_path="memory.json"):
        self.file_path = Path(file_path)
        self.data = self._load()

    def _load(self):
        if not self.file_path.exists():
            return []

        try:
            return json.loads(
                self.file_path.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            return []

    def save(self):
        self.file_path.write_text(
            json.dumps(self.data, indent=2),
            encoding="utf-8",
        )

    def add(self, content):
        self.data.append(content)
        self.save()

    def get_all(self):
        return self.data
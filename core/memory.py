import json
from pathlib import Path
from datetime import datetime


class Memory:
    def __init__(self, file_path="data/memory.json"):
        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file_path.exists():
            self._save([])

        self.memories = self._load()

    def _load(self):
        try:
            with self.file_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

        except (
            json.JSONDecodeError,
            OSError,
        ):
            pass

        return []

    def _save(self, memories=None):
        if memories is None:
            memories = self.memories

        with self.file_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                memories,
                file,
                indent=2,
                ensure_ascii=False,
            )

    def remember(
        self,
        content,
        category="general",
        importance=1,
    ):
        content = content.strip()

        if not content:
            return False

        for memory in self.memories:
            if memory["content"].lower() == content.lower():
                return False

        record = {
            "content": content,
            "category": category,
            "importance": importance,
            "created_at": datetime.now().isoformat(),
        }

        self.memories.append(record)
        self._save()

        return True

    def forget(self, content):
        content = content.strip().lower()

        old_count = len(self.memories)

        self.memories = [
            memory
            for memory in self.memories
            if memory["content"].lower() != content
        ]

        changed = len(self.memories) != old_count

        if changed:
            self._save()

        return changed

    def all(self):
        return list(self.memories)

    def search(self, query, limit=5):
        query_words = set(
            query.lower().split()
        )

        scored = []

        for memory in self.memories:
            words = set(
                memory["content"].lower().split()
            )

            score = len(query_words & words)

            if score > 0:
                scored.append(
                    (
                        score,
                        memory,
                    )
                )

        scored.sort(
            key=lambda item: (
                item[0],
                item[1].get("importance", 1),
            ),
            reverse=True,
        )

        return [
            memory
            for _, memory in scored[:limit]
        ]
from pathlib import Path
from tempfile import TemporaryDirectory

from core.memory_store import MemoryStore


def main():

    with TemporaryDirectory() as temp_dir:

        memory_file = Path(temp_dir) / "memory.json"

        memory_file.write_text(
            '["ARES memory test"]',
            encoding="utf-8",
        )

        store = MemoryStore(memory_file)

        memories = store.all()

        print("Migrated memories:")
        print(memories)

        assert len(memories) == 1
        assert memories[0]["content"] == "ARES memory test"

        print()
        print("MIGRATION TEST PASSED")


if __name__ == "__main__":
    main()
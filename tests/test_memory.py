from pathlib import Path
from tempfile import TemporaryDirectory

from core.memory_manager import MemoryManager


def main():

    with TemporaryDirectory() as temp_dir:

        memory_file = Path(temp_dir) / "memory.json"

        memory = MemoryManager(memory_file)

        created = memory.remember(
            "ARES memory system is working.",
            memory_type="system",
            importance=0.9,
            source="test",
        )

        print("Created:")
        print(created)

        print()

        print("All memories:")
        print(memory.all())

        print()

        print("Stats:")
        print(memory.stats())

        print()

        memory.update(
            created["id"],
            importance=1.0,
        )

        print("Updated:")
        print(memory.get(created["id"]))

        print()

        memory.forget(created["id"])

        print("After deletion:")
        print(memory.all())


if __name__ == "__main__":
    main()
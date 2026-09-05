from pathlib import Path
from tempfile import TemporaryDirectory

from core.memory_manager import MemoryManager
from core.memory_search import MemorySearch


def main():

    with TemporaryDirectory() as temp_dir:

        memory_file = Path(temp_dir) / "memory.json"

        manager = MemoryManager(memory_file)

        manager.remember(
            "ARES uses Python for its backend.",
            memory_type="project",
            importance=0.9,
        )

        manager.remember(
            "ARES will eventually support computer vision.",
            memory_type="project",
            importance=0.8,
        )

        manager.remember(
            "The weather is unrelated to this test.",
            memory_type="general",
            importance=0.1,
        )

        search = MemorySearch(
            manager.store
        )

        results = search.search(
            "Python ARES"
        )

        print("Search results:")

        for result in results:

            print(
                result["score"],
                "->",
                result["memory"]["content"],
            )

        assert results

        print()
        print("MEMORY SEARCH PASSED")


if __name__ == "__main__":
    main()
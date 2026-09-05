from pathlib import Path
from tempfile import TemporaryDirectory

from core.memory_links import MemoryLinks
from core.memory_manager import MemoryManager


def main():

    with TemporaryDirectory() as temp_dir:

        memory = MemoryManager(
            Path(temp_dir) / "memory.json"
        )

        project = memory.remember(
            "ARES project",
            memory_type="project",
            importance=1.0,
        )

        python_memory = memory.remember(
            "ARES uses Python",
            memory_type="knowledge",
            importance=0.8,
        )

        links = MemoryLinks(
            memory.store
        )

        success = links.link(
            project["id"],
            python_memory["id"],
            relation="uses",
            strength=0.9,
        )

        print(
            "Link created:",
            success,
        )

        print()

        print(
            "Relationships:"
        )

        print(
            links.related(
                project["id"]
            )
        )

        assert success

        assert links.related(
            project["id"]
        )

        print()
        print("MEMORY LINKS PASSED")


if __name__ == "__main__":
    main()
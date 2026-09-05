from pathlib import Path
from tempfile import TemporaryDirectory

from core.context_engine import ContextEngine
from core.memory_manager import MemoryManager


def main():

    with TemporaryDirectory() as temp_dir:

        memory_file = Path(temp_dir) / "memory.json"

        memory = MemoryManager(
            memory_file
        )

        memory.remember(
            "ARES is a Python AI assistant project.",
            memory_type="project",
            importance=1.0,
        )

        engine = ContextEngine(memory)

        engine.add_user_message(
            "Tell me about ARES."
        )

        engine.add_assistant_message(
            "ARES is being developed incrementally."
        )

        result = engine.build(
            "ARES Python"
        )

        print("RECENT CONTEXT:")
        print(
            result["recent_messages"]
        )

        print()

        print("RELEVANT MEMORIES:")

        for item in result[
            "relevant_memories"
        ]:

            print(
                item["score"],
                item["memory"]["content"],
            )

        assert result[
            "recent_messages"
        ]

        assert result[
            "relevant_memories"
        ]

        print()
        print("CONTEXT ENGINE PASSED")


if __name__ == "__main__":
    main()
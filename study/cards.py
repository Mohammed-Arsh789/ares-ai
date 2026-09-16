from .models import Difficulty, Flashcard


class FlashcardGenerator:
    def generate(
        self,
        topic: str,
        concepts: list[str],
        difficulty: Difficulty = Difficulty.INTERMEDIATE,
    ) -> list[Flashcard]:
        cards = []

        for concept in concepts:
            concept = concept.strip()

            if not concept:
                continue

            cards.append(
                Flashcard(
                    question=f"What is {concept}?",
                    answer=f"{concept} is an important concept in {topic}.",
                    topic=topic,
                    difficulty=difficulty,
                )
            )

        return cards
from .models import EvidenceItem, ResearchSource


class EvidenceExtractor:
    """
    Converts source snippets into traceable evidence items.
    """

    def extract_from_source(
        self,
        source: ResearchSource,
        claim: str | None = None,
    ) -> EvidenceItem:
        extracted_claim = claim or source.snippet or source.title

        confidence_map = {
            "high": 0.9,
            "medium": 0.65,
            "low": 0.35,
            "unknown": 0.5,
        }

        confidence = confidence_map[
            source.quality.value
        ]

        return EvidenceItem(
            claim=extracted_claim,
            source_url=source.url,
            supporting_text=source.snippet,
            confidence=confidence,
        )

    def extract_many(
        self,
        sources: list[ResearchSource],
    ) -> list[EvidenceItem]:
        return [
            self.extract_from_source(source)
            for source in sources
        ]
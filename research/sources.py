from .models import EvidenceQuality, ResearchSource


class SourceManager:
    """
    Normalizes and ranks research sources.
    """

    TRUSTED_DOMAINS = {
        "gov",
        "edu",
        "who.int",
        "nature.com",
        "sciencedirect.com",
        "arxiv.org",
        "wikipedia.org",
    }

    def normalize_url(self, url: str) -> str:
        return url.strip().rstrip("/")

    def classify_quality(self, url: str) -> EvidenceQuality:
        lowered = url.lower()

        if any(domain in lowered for domain in self.TRUSTED_DOMAINS):
            return EvidenceQuality.HIGH

        if lowered.startswith("https://"):
            return EvidenceQuality.MEDIUM

        return EvidenceQuality.LOW

    def create_source(
        self,
        title: str,
        url: str,
        snippet: str = "",
        source_type: str = "web",
    ) -> ResearchSource:
        normalized = self.normalize_url(url)

        return ResearchSource(
            title=title.strip() or "Untitled source",
            url=normalized,
            snippet=snippet,
            source_type=source_type,
            quality=self.classify_quality(normalized),
        )

    def deduplicate(
        self,
        sources: list[ResearchSource],
    ) -> list[ResearchSource]:
        seen = set()
        unique = []

        for source in sources:
            if source.url in seen:
                continue

            seen.add(source.url)
            unique.append(source)

        return unique

    def rank(
        self,
        sources: list[ResearchSource],
    ) -> list[ResearchSource]:
        ranking = {
            EvidenceQuality.HIGH: 3,
            EvidenceQuality.MEDIUM: 2,
            EvidenceQuality.LOW: 1,
            EvidenceQuality.UNKNOWN: 0,
        }

        return sorted(
            sources,
            key=lambda source: ranking[source.quality],
            reverse=True,
        )
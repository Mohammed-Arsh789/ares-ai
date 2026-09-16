from .models import ResearchReport, ResearchSource, EvidenceItem


class ResearchSynthesizer:
    """
    Produces a structured report from collected evidence.
    """

    def synthesize(
        self,
        question: str,
        sources: list[ResearchSource],
        evidence: list[EvidenceItem],
    ) -> ResearchReport:
        if not sources:
            return ResearchReport(
                question=question,
                summary=(
                    "No sources were collected. "
                    "The research result is incomplete."
                ),
                sources=[],
                evidence=[],
                limitations=["No usable sources were found."],
            )

        summary_lines = [
            f"Research question: {question}",
            f"Collected {len(sources)} source(s).",
        ]

        for index, evidence_item in enumerate(
            evidence[:5],
            start=1,
        ):
            summary_lines.append(
                f"{index}. {evidence_item.claim}"
            )

        limitations = []

        if len(sources) < 3:
            limitations.append(
                "The source sample is small."
            )

        if not evidence:
            limitations.append(
                "No evidence items were extracted."
            )

        return ResearchReport(
            question=question,
            summary="\n".join(summary_lines),
            sources=sources,
            evidence=evidence,
            limitations=limitations,
            metadata={
                "source_count": len(sources),
                "evidence_count": len(evidence),
            },
        )
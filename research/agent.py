from .collector import ResearchCollector
from .evidence import EvidenceExtractor
from .models import ResearchReport
from .planner import ResearchPlanner
from .sources import SourceManager
from .synthesizer import ResearchSynthesizer


class ResearchAgent:
    """
    Structured research agent.

    It performs source collection and evidence organization.
    LLM-based synthesis can be connected later.
    """

    def __init__(
        self,
        search_function=None,
    ):
        self.planner = ResearchPlanner()
        self.source_manager = SourceManager()
        self.collector = ResearchCollector(
            search_function=search_function,
            source_manager=self.source_manager,
        )
        self.extractor = EvidenceExtractor()
        self.synthesizer = ResearchSynthesizer()

    def research(
        self,
        question: str,
        depth: str = "standard",
        max_sources: int = 10,
    ) -> ResearchReport:
        request = self.planner.create_request(
            question=question,
            depth=depth,
            max_sources=max_sources,
        )

        subtasks = self.planner.decompose(request)

        all_sources = []

        per_task_limit = max(
            1,
            request.max_sources // max(1, len(subtasks)),
        )

        for subtask in subtasks:
            sources = self.collector.collect(
                query=subtask.query,
                max_results=per_task_limit,
            )

            all_sources.extend(sources)

        all_sources = self.source_manager.deduplicate(
            all_sources
        )

        all_sources = self.source_manager.rank(
            all_sources
        )[:request.max_sources]

        evidence = self.extractor.extract_many(
            all_sources
        )

        return self.synthesizer.synthesize(
            question=request.question,
            sources=all_sources,
            evidence=evidence,
        )
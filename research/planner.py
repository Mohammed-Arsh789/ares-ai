from .models import ResearchRequest, ResearchSubtask


class ResearchPlanner:
    """
    Breaks a research question into manageable subtasks.
    """

    def create_request(
        self,
        question: str,
        depth: str = "standard",
        max_sources: int = 10,
    ) -> ResearchRequest:
        from .models import ResearchDepth

        try:
            research_depth = ResearchDepth(depth.lower())
        except ValueError:
            research_depth = ResearchDepth.STANDARD

        return ResearchRequest(
            question=question,
            depth=research_depth,
            max_sources=max_sources,
        )

    def decompose(
        self,
        request: ResearchRequest,
    ) -> list[ResearchSubtask]:
        question = request.question

        subtasks = [
            ResearchSubtask(
                title="Core definition",
                query=f"What is {question}?",
                priority=1,
            ),
            ResearchSubtask(
                title="Current evidence",
                query=f"Latest reliable evidence about {question}",
                priority=2,
            ),
            ResearchSubtask(
                title="Advantages and limitations",
                query=f"Benefits limitations criticisms of {question}",
                priority=3,
            ),
        ]

        if request.depth.value == "deep":
            subtasks.extend(
                [
                    ResearchSubtask(
                        title="Historical context",
                        query=f"History and development of {question}",
                        priority=4,
                    ),
                    ResearchSubtask(
                        title="Expert perspectives",
                        query=f"Expert analysis and opposing views on {question}",
                        priority=5,
                    ),
                ]
            )

        return subtasks
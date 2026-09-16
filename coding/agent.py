from pathlib import Path

from .context import CodeContextBuilder
from .models import CodingResult, CodingTaskType
from .planner import CodingTaskPlanner
from .project import ProjectInspector


class CodingAgent:
    """
    Initial safe coding agent.

    Current capabilities:
    - classify coding requests
    - inspect projects
    - read code context
    - return structured coding information

    It does not autonomously overwrite files yet.
    """

    def __init__(
        self,
        inspector: ProjectInspector | None = None,
        context_builder: CodeContextBuilder | None = None,
        planner: CodingTaskPlanner | None = None,
    ):
        self.inspector = inspector or ProjectInspector()
        self.context_builder = (
            context_builder
            or CodeContextBuilder(self.inspector)
        )
        self.planner = planner or CodingTaskPlanner()

    def inspect_project(
        self,
        project_path: str,
    ) -> CodingResult:
        try:
            summary = self.inspector.project_summary(project_path)

            return CodingResult(
                success=True,
                message=(
                    f"Inspected project containing "
                    f"{summary['file_count']} supported files."
                ),
                metadata=summary,
            )

        except Exception as error:
            return CodingResult(
                success=False,
                message="Project inspection failed.",
                errors=[str(error)],
            )

    def analyze_request(
        self,
        instruction: str,
        project_path: str | None = None,
        target_files: list[str] | None = None,
    ) -> CodingResult:
        try:
            request = self.planner.create_request(
                instruction=instruction,
                project_path=project_path,
                target_files=target_files,
            )

            files_inspected: list[str] = []
            metadata = {
                "task_type": request.task_type.value,
                "instruction": request.instruction,
            }

            if project_path:
                contexts = self.context_builder.build_context(
                    project_path,
                    target_files=request.target_files,
                )

                files_inspected = [
                    context.path
                    for context in contexts
                ]

                metadata["context_count"] = len(contexts)
                metadata["languages"] = sorted(
                    {
                        context.language
                        for context in contexts
                    }
                )

            return CodingResult(
                success=True,
                message=(
                    f"Coding request classified as "
                    f"'{request.task_type.value}'."
                ),
                task_type=request.task_type,
                files_inspected=files_inspected,
                metadata=metadata,
            )

        except Exception as error:
            return CodingResult(
                success=False,
                message="Coding request analysis failed.",
                errors=[str(error)],
            )
from pathlib import Path

from .models import FileContext
from .project import ProjectInspector


class CodeContextBuilder:
    """
    Reads safe code context from project files.
    """

    LANGUAGE_MAP = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript-react",
        ".jsx": "javascript-react",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".h": "c-header",
        ".cs": "csharp",
        ".go": "go",
        ".rs": "rust",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
        ".md": "markdown",
        ".txt": "text",
    }

    def __init__(self, inspector: ProjectInspector | None = None):
        self.inspector = inspector or ProjectInspector()

    def detect_language(self, path: str | Path) -> str:
        return self.LANGUAGE_MAP.get(
            Path(path).suffix.lower(),
            "unknown",
        )

    def read_file(
        self,
        file_path: str | Path,
        project_root: str | Path | None = None,
        max_bytes: int = 200_000,
    ) -> FileContext:
        path = Path(file_path).expanduser().resolve()

        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")

        if not path.is_file():
            raise IsADirectoryError(f"Not a file: {path}")

        if project_root is not None:
            root = Path(project_root).expanduser().resolve()

            try:
                path.relative_to(root)
            except ValueError as error:
                raise PermissionError(
                    "File is outside the selected project root."
                ) from error

        size_bytes = path.stat().st_size

        if size_bytes > max_bytes:
            raise ValueError(
                f"File is too large to inspect safely: {path}"
            )

        content = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        return FileContext(
            path=str(path),
            content=content,
            language=self.detect_language(path),
            size_bytes=size_bytes,
        )

    def build_context(
        self,
        project_path: str | Path,
        target_files: list[str] | None = None,
    ) -> list[FileContext]:
        root = self.inspector.validate_project_path(project_path)

        if target_files:
            paths = [
                (root / relative_path).resolve()
                for relative_path in target_files
            ]
        else:
            paths = self.inspector.list_files(root)

        contexts = []

        for path in paths:
            try:
                context = self.read_file(
                    path,
                    project_root=root,
                )
                contexts.append(context)
            except (OSError, ValueError, PermissionError):
                continue

        return contexts
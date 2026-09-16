from pathlib import Path


class ProjectInspector:
    """
    Safely inspects a project directory.

    This class only reads metadata and file contents.
    It does not execute project code.
    """

    DEFAULT_IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        ".idea",
        ".vscode",
        "dist",
        "build",
    }

    DEFAULT_ALLOWED_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".cs",
        ".go",
        ".rs",
        ".html",
        ".css",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".md",
        ".txt",
    }

    def __init__(
        self,
        ignored_directories: set[str] | None = None,
        allowed_extensions: set[str] | None = None,
    ):
        self.ignored_directories = (
            ignored_directories
            if ignored_directories is not None
            else self.DEFAULT_IGNORED_DIRECTORIES
        )

        self.allowed_extensions = (
            allowed_extensions
            if allowed_extensions is not None
            else self.DEFAULT_ALLOWED_EXTENSIONS
        )

    def validate_project_path(self, project_path: str | Path) -> Path:
        path = Path(project_path).expanduser().resolve()

        if not path.exists():
            raise FileNotFoundError(f"Project path does not exist: {path}")

        if not path.is_dir():
            raise NotADirectoryError(f"Project path is not a directory: {path}")

        return path

    def list_files(
        self,
        project_path: str | Path,
        recursive: bool = True,
    ) -> list[Path]:
        root = self.validate_project_path(project_path)

        iterator = root.rglob("*") if recursive else root.glob("*")

        files = []

        for path in iterator:
            if not path.is_file():
                continue

            if any(
                ignored in path.parts
                for ignored in self.ignored_directories
            ):
                continue

            if path.suffix.lower() not in self.allowed_extensions:
                continue

            files.append(path)

        return sorted(files)

    def project_summary(self, project_path: str | Path) -> dict:
        root = self.validate_project_path(project_path)
        files = self.list_files(root)

        extensions: dict[str, int] = {}

        for file_path in files:
            extension = file_path.suffix.lower() or "[no extension]"
            extensions[extension] = extensions.get(extension, 0) + 1

        return {
            "root": str(root),
            "file_count": len(files),
            "extensions": extensions,
            "files": [str(path.relative_to(root)) for path in files],
        }
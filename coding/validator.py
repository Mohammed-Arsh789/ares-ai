import ast
from pathlib import Path


class CodeValidator:
    """
    Performs safe static validation.
    """

    def validate_python_syntax(
        self,
        source: str,
        filename: str = "<unknown>",
    ) -> dict:
        try:
            ast.parse(source, filename=filename)

            return {
                "valid": True,
                "language": "python",
                "filename": filename,
                "error": None,
            }

        except SyntaxError as error:
            return {
                "valid": False,
                "language": "python",
                "filename": filename,
                "error": str(error),
                "line": error.lineno,
                "column": error.offset,
            }

    def validate_file(
        self,
        file_path: str | Path,
        source: str | None = None,
    ) -> dict:
        path = Path(file_path)

        if source is None:
            source = path.read_text(
                encoding="utf-8",
                errors="replace",
            )

        if path.suffix.lower() == ".py":
            return self.validate_python_syntax(
                source,
                filename=str(path),
            )

        return {
            "valid": True,
            "language": path.suffix.lower().lstrip(".") or "unknown",
            "filename": str(path),
            "error": None,
            "note": "Only Python syntax validation is currently implemented.",
        }
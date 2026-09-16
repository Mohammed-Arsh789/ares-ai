"""
ARES Text Document Reader
"""

from __future__ import annotations

from pathlib import Path


def read_text(
    path: str,
) -> str:

    file_path = Path(path)

    if not file_path.exists():

        raise FileNotFoundError(
            f"File not found: {path}"
        )

    if not file_path.is_file():

        raise ValueError(
            f"Path is not a file: {path}"
        )

    return file_path.read_text(
        encoding="utf-8",
        errors="replace",
    )
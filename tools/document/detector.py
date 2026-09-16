"""
ARES Document Format Detector

Determines whether a file is supported by the
ARES document-intelligence subsystem.
"""

from __future__ import annotations

from pathlib import Path


SUPPORTED_EXTENSIONS = frozenset(
    {
        ".txt",
        ".md",
        ".json",
        ".csv",
        ".pdf",
        ".docx",
    }
)


def detect_format(path: str) -> str:
    """
    Detect the extension of a supported document.

    Raises:
        FileNotFoundError:
            If the file does not exist.

        ValueError:
            If the file format is unsupported.
    """

    if not isinstance(path, str):
        raise TypeError(
            "path must be a string."
        )

    if not path.strip():
        raise ValueError(
            "Document path cannot be empty."
        )

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"Path is not a file: {path}"
        )

    extension = (
        file_path.suffix
        .lower()
    )

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported document format: "
            f"{extension or '[none]'}"
        )

    return extension


def is_supported(path: str) -> bool:
    """
    Return True when a file uses a supported format.
    """

    try:
        extension = (
            Path(path)
            .suffix
            .lower()
        )

        return (
            extension
            in SUPPORTED_EXTENSIONS
        )

    except (TypeError, ValueError):
        return False
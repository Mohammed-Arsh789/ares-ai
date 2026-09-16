"""
ARES DOCX Reader
"""

from __future__ import annotations

from pathlib import Path


def read_docx(
    path: str,
) -> str:

    from docx import Document as DocxDocument

    file_path = Path(path)

    if not file_path.exists():

        raise FileNotFoundError(
            f"File not found: {path}"
        )

    document = DocxDocument(
        str(file_path)
    )

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:

            paragraphs.append(text)

    return "\n\n".join(
        paragraphs
    )
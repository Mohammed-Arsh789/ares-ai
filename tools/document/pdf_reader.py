"""
ARES PDF Reader
"""

from __future__ import annotations

from pathlib import Path


def read_pdf(
    path: str,
) -> tuple[str, int]:

    from pypdf import PdfReader

    file_path = Path(path)

    if not file_path.exists():

        raise FileNotFoundError(
            f"File not found: {path}"
        )

    reader = PdfReader(
        str(file_path)
    )

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:

            pages.append(text)

    return (
        "\n\n".join(pages),
        len(reader.pages),
    )
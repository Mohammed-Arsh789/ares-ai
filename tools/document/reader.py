"""
ARES Unified Document Reader
"""

from __future__ import annotations

from pathlib import Path

from .csv_reader import read_csv
from .detector import detect_format
from .docx_reader import read_docx
from .json_reader import read_json
from .model import Document
from .pdf_reader import read_pdf
from .text_reader import read_text


class DocumentReader:

    def read(
        self,
        path: str,
    ) -> Document:

        file_path = Path(path)

        extension = detect_format(
            path
        )

        pages = None

        if extension in {
            ".txt",
            ".md",
        }:

            content = read_text(
                path
            )

        elif extension == ".json":

            content = read_json(
                path
            )

        elif extension == ".csv":

            content = read_csv(
                path
            )

        elif extension == ".pdf":

            content, pages = read_pdf(
                path
            )

        elif extension == ".docx":

            content = read_docx(
                path
            )

        else:

            raise ValueError(
                f"Unsupported format: "
                f"{extension}"
            )

        return Document(
            name=file_path.name,
            path=str(
                file_path.resolve()
            ),
            extension=extension,
            content=content,
            pages=pages,
            metadata={
                "size_bytes":
                    file_path.stat().st_size,
            },
        )
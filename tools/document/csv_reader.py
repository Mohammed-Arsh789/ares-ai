"""
ARES CSV Document Reader
"""

from __future__ import annotations

import csv
from pathlib import Path


def read_csv(
    path: str,
) -> str:

    file_path = Path(path)

    if not file_path.exists():

        raise FileNotFoundError(
            f"File not found: {path}"
        )

    rows = []

    with file_path.open(
        "r",
        encoding="utf-8",
        errors="replace",
        newline="",
    ) as file:

        reader = csv.reader(file)

        for row in reader:

            rows.append(
                " | ".join(row)
            )

    return "\n".join(rows)
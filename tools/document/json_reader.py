"""
ARES JSON Document Reader
"""

from __future__ import annotations

import json
from pathlib import Path


def read_json(
    path: str,
) -> str:

    file_path = Path(path)

    if not file_path.exists():

        raise FileNotFoundError(
            f"File not found: {path}"
        )

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False,
    )
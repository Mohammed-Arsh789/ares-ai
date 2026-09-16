"""
ARES Web Retry Utility
"""

from __future__ import annotations

import time
from typing import Callable, TypeVar


T = TypeVar("T")


def retry(
    function: Callable[[], T],
    attempts: int = 3,
    delay: float = 0.5,
) -> T:

    attempts = max(
        1,
        min(
            int(attempts),
            3,
        ),
    )

    last_error: Exception | None = None

    for attempt in range(attempts):

        try:

            return function()

        except Exception as error:

            last_error = error

            if attempt == attempts - 1:

                break

            time.sleep(
                delay * (attempt + 1)
            )

    if last_error is not None:

        raise last_error

    raise RuntimeError(
        "Retry failed without an exception."
    )
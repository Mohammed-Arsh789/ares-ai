from __future__ import annotations

from abc import ABC, abstractmethod


class Filter(ABC):

    name: str = "unnamed"

    @abstractmethod
    def apply(self, frame):
        raise NotImplementedError
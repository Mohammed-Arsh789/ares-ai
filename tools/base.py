from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """
    Base class for every ARES tool.
    """

    name = "unnamed"
    description = "No description provided."

    @abstractmethod
    def run(self, **kwargs) -> Any:
        """
        Execute the tool.
        """
        raise NotImplementedError
from abc import ABC, abstractmethod
from typing import Any


class BaseAdapter(ABC):
    """Stable adapter boundary between an application and the benchmark runner."""

    @abstractmethod
    def predict(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

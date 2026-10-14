from typing import Any
from adapters.base_adapter import BaseAdapter


class LLMAdapterTemplate(BaseAdapter):
    def predict(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Override this method to return an answer and optional context."""
        raise NotImplementedError("Implement the LLM adapter for your application")

from typing import Any
from adapters.base_adapter import BaseAdapter


class CVAdapterTemplate(BaseAdapter):
    def predict(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Override this method to return predictions for one image."""
        raise NotImplementedError("Implement the CV adapter for your application")

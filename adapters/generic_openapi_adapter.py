from typing import Any
import urllib.request
import json
from adapters.base_adapter import BaseAdapter


class GenericOpenAPIAdapter(BaseAdapter):
    """Small standard-library adapter for an OpenAPI-compatible JSON endpoint."""

    def __init__(self, endpoint: str, timeout: float = 30) -> None:
        self.endpoint, self.timeout = endpoint, timeout

    def predict(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(self.endpoint, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            decoded = json.loads(response.read().decode("utf-8"))
        if not isinstance(decoded, dict):
            raise ValueError("Adapter endpoint must return a JSON object")
        return decoded

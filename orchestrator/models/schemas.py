from typing import Any, Literal
from pydantic import BaseModel, Field


class AppRegistration(BaseModel):
    app_id: str = Field(min_length=1, max_length=100)
    name: str
    app_type: Literal["cv", "llm"]
    endpoint: str | None = None
    latency_budget_ms: float = Field(default=2000, gt=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvaluationRequest(BaseModel):
    app_id: str
    app_type: Literal["cv", "llm"]
    records: list[dict[str, Any]] = Field(min_length=1)
    dataset_version: str = "sample-v1"
    security_records: list[dict[str, Any]] = Field(default_factory=list)
    git_commit: str | None = None


class RunResponse(BaseModel):
    run_id: str
    app_id: str
    app_type: str
    composite_score: float
    gates: dict[str, Any]
    metrics: dict[str, Any]
    security: dict[str, Any]
    created_at: str

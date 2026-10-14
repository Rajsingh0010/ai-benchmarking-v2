from datetime import datetime, timezone
from uuid import uuid4
from typing import Any
from orchestrator.config import Settings
from orchestrator.models.schemas import EvaluationRequest
from orchestrator.storage import RunStore
from metrics_engine.cv_metrics.detection import evaluate_detection_records
from metrics_engine.llm_metrics.generation import evaluate_llm_records
from security_suite.scorers import evaluate_security
from gates.gate_checker import check_gates


def evaluate(request: EvaluationRequest, store: RunStore, settings: Settings) -> dict[str, Any]:
    metrics = (evaluate_detection_records(request.records) if request.app_type == "cv"
               else evaluate_llm_records(request.records))
    security = evaluate_security(request.security_records)
    composite = _composite(request.app_type, metrics)
    gates = check_gates(request.app_type, metrics, security)
    run = {
        "run_id": str(uuid4()), "app_id": request.app_id, "app_type": request.app_type,
        "dataset_version": request.dataset_version, "git_commit": request.git_commit or settings.git_commit,
        "hardware_profile": settings.hardware_profile,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "composite_score": round(composite, 4), "metrics": metrics, "security": security, "gates": gates,
    }
    store.save(run)
    return run


def _composite(app_type: str, metrics: dict[str, Any]) -> float:
    if app_type == "cv":
        weights = {"map50": .35, "map5095": .25, "f1": .2, "mean_iou": .1, "robustness": .1}
    else:
        weights = {"exact_match": .25, "token_f1": .25, "faithfulness": .2, "answer_relevance": .2, "latency_score": .1}
    return sum(metrics.get(key, 0) * weight for key, weight in weights.items())

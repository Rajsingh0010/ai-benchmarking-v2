from fastapi import FastAPI, HTTPException
from orchestrator.config import settings
from orchestrator.models.schemas import AppRegistration, EvaluationRequest
from orchestrator.routes.evaluation import evaluate
from orchestrator.storage import RunStore

app = FastAPI(title="AI Benchmarking Suite", version="1.0.0")
store = RunStore(settings.db_path)
registered: dict[str, AppRegistration] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": app.version}


@app.post("/register_app")
def register_app(registration: AppRegistration) -> dict[str, str]:
    registered[registration.app_id] = registration
    return {"status": "registered", "app_id": registration.app_id}


@app.post("/run_eval")
def run_eval(request: EvaluationRequest) -> dict:
    registration = registered.get(request.app_id)
    if registration is None:
        raise HTTPException(status_code=404, detail=f"App is not registered: {request.app_id}")
    if registration.app_type != request.app_type:
        raise HTTPException(status_code=422, detail="app_type does not match registration")
    return evaluate(request, store, settings)


@app.get("/results/{run_id}")
def get_result(run_id: str) -> dict:
    result = store.get(run_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return result


@app.get("/results")
def list_results(limit: int = 50) -> list[dict]:
    return store.list(max(1, min(limit, 200)))

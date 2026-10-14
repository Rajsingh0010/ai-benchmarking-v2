# AI Benchmarking Suite v1

An offline-first benchmark harness for computer-vision, LLM/RAG, and AI safety evaluation.

## v1 capabilities

- FastAPI orchestration API: register apps, run benchmark payloads, retrieve immutable results.
- Model-agnostic CV metrics: IoU matching, precision/recall/F1, mAP at IoU 0.5 and 0.5:0.95, and slice breakdowns.
- LLM metrics: exact/normalized match, token F1, faithfulness and abstention heuristics, latency percentiles, and category slices.
- Security gate scoring: jailbreak ASR, toxicity, data-leak detection, agentic-risk and severity-weighted pass rate.
- Weighted composite scoring with explicit acceptance gates.
- SQLite persistence and a Streamlit dashboard.
- Contract schemas and adapter interfaces for plugging in real applications.

## Quickstart

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn orchestrator.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API, or run:

```powershell
streamlit run results_store\dashboard\app.py
```

Run the deterministic sample benchmark:

```powershell
py scripts\run_benchmark.py
```

The API accepts evaluation records directly, so v1 can be used with local mock apps or a real adapter without downloading model weights.

## API

- `POST /register_app` — register an app against the CV or LLM contract.
- `POST /run_eval` — evaluate a payload and persist a run.
- `GET /results/{run_id}` — return a stored immutable run.
- `GET /results` — list recent runs.
- `GET /health` — health check.

See `docs/eval-contracts.md` and `docs/how_to_register_an_app.md`.

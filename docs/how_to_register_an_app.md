# Register an app

Start the API with `uvicorn orchestrator.main:app --reload`, then register:

```json
{"app_id":"demo-llm","name":"Demo LLM","app_type":"llm","latency_budget_ms":1000}
```

Send it to `POST /register_app`, then send records to `POST /run_eval`. The returned `run_id` can be retrieved permanently from `GET /results/{run_id}`.

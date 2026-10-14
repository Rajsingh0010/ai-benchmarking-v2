# AI Benchmarking Suite v2

Offline-first benchmarking for computer-vision, LLM/RAG, and AI safety systems.

The complete v2 source tree is packaged in [`ai-benchmarking-v2.zip`](./ai-benchmarking-v2.zip). Extract it locally, install `requirements.txt`, and run:

```powershell
uvicorn orchestrator.main:app --reload
```

The suite includes app registration, CV and LLM metrics, security gates, immutable SQLite results, adapters, contracts, tests, and a Streamlit dashboard.

Local verification: **5 tests passed**.

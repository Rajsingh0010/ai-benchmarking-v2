# v1.0 Release Notes

## Included

- API registration, evaluation, immutable SQLite results, and health endpoints.
- Deterministic CV and LLM metric engines with scenario slices.
- Standalone security gate and severity-weighted pass rate.
- Contract schemas, adapter extension points, sample datasets, tests, and dashboard.

## Known v1 boundaries

- The seeded datasets are schema examples, not the 1000-image/1000-question production corpus.
- Advanced model-backed metrics (BERTScore, RAGAS, Detoxify, Presidio) are extension points for an air-gapped deployment.
- API and dashboard dependencies are installed from `requirements.txt`; metric calculations and sample runner are dependency-light.

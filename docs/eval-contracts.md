# v1 Evaluation Contracts

CV records contain `predictions` and `truth`, each a list of `{box: [x1, y1, x2, y2], label, score}` (score is optional for truth). Add `slices` such as `["low_light", "occluded"]`.

LLM records contain `question`, `answer`, `ground_truth`, optional `context`, `category`, `latency_ms`, `faithfulness`, `answer_relevance`, and `out_of_scope`.

Composite scores are normalized to `[0, 1]`. Security is a separate hard gate and is never blended into the accuracy composite:

- CV: mAP50 35%, mAP50:95 25%, F1 20%, IoU 10%, robustness 10%.
- LLM: exact match 25%, token F1 25%, faithfulness 20%, relevance 20%, latency 10%.

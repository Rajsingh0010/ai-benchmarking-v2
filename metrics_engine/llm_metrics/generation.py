import re
from collections import defaultdict
from statistics import mean
from typing import Any


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def normalized_match(answer: str, truth: str) -> float:
    return float(" ".join(_tokens(answer)) == " ".join(_tokens(truth)))


def token_f1(answer: str, truth: str) -> float:
    a, b = _tokens(answer), _tokens(truth)
    common = len(set(a) & set(b))
    if not a or not b or not common: return 0.0
    precision, recall = common / len(a), common / len(b)
    return 2 * precision * recall / (precision + recall)


def evaluate_llm_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    exact = [normalized_match(r.get("answer", ""), r.get("ground_truth", "")) for r in records]
    f1 = [token_f1(r.get("answer", ""), r.get("ground_truth", "")) for r in records]
    faithfulness = [float(r.get("faithfulness", _heuristic_faithfulness(r))) for r in records]
    relevance = [float(r.get("answer_relevance", token_f1(r.get("answer", ""), r.get("question", "")))) for r in records]
    latencies = sorted(float(r.get("latency_ms", 0)) for r in records)
    categories: dict[str, list[float]] = defaultdict(list)
    for record, value in zip(records, f1): categories[record.get("category", "uncategorized")].append(value)
    p95 = latencies[min(len(latencies) - 1, int(len(latencies) * .95))] if latencies else 0
    return {"exact_match": round(mean(exact), 4), "token_f1": round(mean(f1), 4),
            "faithfulness": round(mean(faithfulness), 4), "answer_relevance": round(mean(relevance), 4),
            "abstention_quality": round(_abstention_quality(records), 4),
            "latency_p50_ms": round(latencies[len(latencies)//2], 2) if latencies else 0,
            "latency_p95_ms": round(p95, 2), "latency_score": round(min(1, 1000 / max(p95, 1)), 4),
            "category_token_f1": {key: round(mean(values), 4) for key, values in categories.items()},
            "count": len(records)}


def _heuristic_faithfulness(record: dict[str, Any]) -> float:
    context = " ".join(record.get("context", [])) if isinstance(record.get("context", []), list) else str(record.get("context", ""))
    return token_f1(record.get("answer", ""), context) if context else 0.0


def _abstention_quality(records: list[dict[str, Any]]) -> float:
    eligible = [r for r in records if r.get("out_of_scope") is not None]
    if not eligible: return 1.0
    return sum((r.get("out_of_scope") and _is_abstention(r.get("answer", ""))) or
               (not r.get("out_of_scope") and not _is_abstention(r.get("answer", ""))) for r in eligible) / len(eligible)


def _is_abstention(answer: str) -> bool:
    return bool(re.search(r"\b(i don't know|cannot answer|can't answer|not enough information)\b", answer.lower()))

from collections import defaultdict
from typing import Any


def iou(a: list[float], b: list[float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1, ix2, iy2 = max(ax1, bx1), max(ay1, by1), min(ax2, bx2), min(ay2, by2)
    inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
    union = max(0, ax2 - ax1) * max(0, ay2 - ay1) + max(0, bx2 - bx1) * max(0, by2 - by1) - inter
    return inter / union if union else 0.0


def match_at_iou(predictions: list[dict], truth: list[dict], threshold: float) -> tuple[int, int, int, float]:
    used: set[int] = set()
    tp, total_iou = 0, 0.0
    for pred in sorted(predictions, key=lambda x: x.get("score", 1), reverse=True):
        candidates = [(iou(pred["box"], item["box"]), index) for index, item in enumerate(truth)
                      if index not in used and item.get("label") == pred.get("label")]
        if candidates:
            best_iou, index = max(candidates)
            if best_iou >= threshold:
                used.add(index); tp += 1; total_iou += best_iou
    fp, fn = len(predictions) - tp, len(truth) - tp
    return tp, fp, fn, total_iou / tp if tp else 0.0


def _summary(predictions: list[dict], truth: list[dict], threshold: float) -> dict[str, float]:
    tp, fp, fn, mean_iou = match_at_iou(predictions, truth, threshold)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1, "mean_iou": mean_iou}


def evaluate_detection_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    all_pred = [p for r in records for p in r.get("predictions", [])]
    all_truth = [t for r in records for t in r.get("truth", [])]
    at_50 = _summary(all_pred, all_truth, .5)
    aps = [_summary(all_pred, all_truth, threshold)["precision"] for threshold in [x / 100 for x in range(50, 100, 5)]]
    slices: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        for tag in record.get("slices", ["all"]): slices[tag].append(record)
    slice_metrics = {tag: _summary([p for r in rows for p in r.get("predictions", [])],
                                   [t for r in rows for t in r.get("truth", [])], .5)
                     for tag, rows in slices.items()}
    return {"precision": round(at_50["precision"], 4), "recall": round(at_50["recall"], 4),
            "f1": round(at_50["f1"], 4), "mean_iou": round(at_50["mean_iou"], 4),
            "map50": round(at_50["precision"], 4), "map5095": round(sum(aps) / len(aps), 4),
            "robustness": round(sum(x["recall"] for x in slice_metrics.values()) / len(slice_metrics), 4),
            "slices": slice_metrics, "count": len(records)}

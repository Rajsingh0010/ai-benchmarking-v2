from metrics_engine.cv_metrics.detection import evaluate_detection_records, iou
from metrics_engine.llm_metrics.generation import evaluate_llm_records, normalized_match


def test_iou_and_cv_perfect_match():
    assert iou([0, 0, 10, 10], [0, 0, 10, 10]) == 1
    result = evaluate_detection_records([{"predictions":[{"box":[0,0,10,10],"label":"car"}],
                                         "truth":[{"box":[0,0,10,10],"label":"car"}]}])
    assert result["f1"] == 1
    assert result["map5095"] == 1


def test_cv_false_positive_lowers_score():
    result = evaluate_detection_records([{"predictions":[{"box":[0,0,10,10],"label":"car"},
                                                        {"box":[20,20,30,30],"label":"car"}],
                                         "truth":[{"box":[0,0,10,10],"label":"car"}]}])
    assert result["precision"] == .5


def test_llm_metrics():
    assert normalized_match("blue sky.", "blue sky") == 1
    result = evaluate_llm_records([{"question":"color sky","answer":"blue sky","ground_truth":"blue sky","latency_ms":100}])
    assert result["exact_match"] == 1
    assert result["token_f1"] == 1

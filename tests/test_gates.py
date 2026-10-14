from gates.gate_checker import check_gates


def test_security_gates_reject_leaks_even_with_good_accuracy():
    result = check_gates(
        "llm",
        {"faithfulness": 1, "answer_relevance": 1, "token_f1": 1},
        {"status": "fail", "severity_weighted_pass_rate": 1, "asr": 0, "data_leak_rate": .01},
    )
    assert result["passed"] is False
    assert result["checks"]["data_leak_rate"]["passed"] is False


def test_security_gates_accept_clean_run():
    result = check_gates(
        "cv",
        {"map50": 1, "f1": 1, "robustness": 1},
        {"status": "pass", "severity_weighted_pass_rate": 1, "asr": 0, "data_leak_rate": 0},
    )
    assert result["passed"] is True

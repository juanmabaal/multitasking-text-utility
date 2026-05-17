from src.feedback import should_refine_response


def test_should_refine_true_when_any_score_is_below_threshold():
    scores = {
        "category": 1.0,
        "priority": 0.9,
        "answer": 0.7,
        "actions": 0.9,
        "status": 1.0,
    }

    assert should_refine_response(scores) is True


def test_should_refine_false_when_all_scores_are_equal_or_above_threshold():
    scores = {
        "category": 1.0,
        "priority": 0.9,
        "answer": 0.8,
        "actions": 0.8,
        "status": 1.0,
    }

    assert should_refine_response(scores) is False
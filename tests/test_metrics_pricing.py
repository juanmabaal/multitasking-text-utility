from src.model_pricing import MODEL_PRICING


def test_gpt_4o_mini_pricing_exists():
    pricing = MODEL_PRICING["gpt-4o-mini"]

    assert pricing["input_per_1m"] > 0
    assert pricing["output_per_1m"] > 0


def test_model_pricing_has_required_keys():
    for model, pricing in MODEL_PRICING.items():
        assert "input_per_1m" in pricing
        assert "output_per_1m" in pricing
        assert pricing["input_per_1m"] >= 0
        assert pricing["output_per_1m"] >= 0
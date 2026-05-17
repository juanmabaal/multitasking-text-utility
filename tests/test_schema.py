from src.schema import SupportResponse


def test_support_response_schema_accepts_valid_payload():
    payload = {
        "support_output": {
            "category": "payment",
            "priority": "high",
            "answer": "We can help you review your payment issue.",
            "actions": [
                "Verify your card information.",
                "Check if your bank blocked the transaction.",
                "Try another payment method.",
            ],
            "status": "needs_human_review",
        }
    }

    result = SupportResponse.model_validate(payload)

    assert result.support_output.category == "payment"
    assert result.support_output.priority == "high"
    assert result.support_output.status == "needs_human_review"
    assert len(result.support_output.actions) == 3
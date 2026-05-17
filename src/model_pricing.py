MODEL_PRICING = {
    # GPT-4o family
    "gpt-4o": {
        "input_per_1m": 2.50,
        "output_per_1m": 10.00,
    },
    "gpt-4o-mini": {
        "input_per_1m": 0.15,
        "output_per_1m": 0.60,
    },

    # GPT-4.1 family
    "gpt-4.1": {
        "input_per_1m": 2.00,
        "output_per_1m": 8.00,
    },
    "gpt-4.1-mini": {
        "input_per_1m": 0.40,
        "output_per_1m": 1.60,
    },
    "gpt-4.1-nano": {
        "input_per_1m": 0.10,
        "output_per_1m": 0.40,
    },

    # GPT-5 family
    "gpt-5.5": {
        "input_per_1m": 5.00,
        "output_per_1m": 30.00,
    },
    "gpt-5.4": {
        "input_per_1m": 2.50,
        "output_per_1m": 15.00,
    },
    "gpt-5.4-mini": {
        "input_per_1m": 0.75,
        "output_per_1m": 4.50,
    },
    "gpt-5-mini": {
        "input_per_1m": 0.25,
        "output_per_1m": 2.00,
    },
    "gpt-5-nano": {
        "input_per_1m": 0.05,
        "output_per_1m": 0.40,
    },

    # Legacy / compatibility
    "gpt-3.5-turbo": {
        "input_per_1m": 0.50,
        "output_per_1m": 1.50,
    },

    # Realtime / audio examples
    "gpt-realtime": {
        "input_per_1m": 4.00,
        "output_per_1m": 16.00,
    },
    "gpt-realtime-mini": {
        "input_per_1m": 0.60,
        "output_per_1m": 2.40,
    },
}
# Utilities for logging execution metrics such as latency, token usage, and cost

import tiktoken,  os, json
from typing import Any

def get_token_usage_from_response(response: Any) -> dict:
    usage = getattr(response, "usage", None)

    if usage is None:
        return {
            "tokens_prompt": 0,
            "tokens_completion": 0,
            "total_tokens": 0,
        }
    
    return {
        "tokens_prompt": getattr(usage, "prompt_tokens", 0) or 0,
        "tokens_completion": getattr(usage, "completion_tokens", 0) or 0,
        "total_tokens": getattr(usage, "total_tokens", 0) or 0,
    }

def estimate_tokens_with_tiktoken(prompt: str, output: dict) -> dict:
    model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

    try:
        enc = tiktoken.encoding_for_model(model)
    except:
        enc = tiktoken.get_encoding('cl100k_base')

    output_as_text = json.dumps(output, ensure_ascii=False)


    tokens_prompt = len(enc.encode(prompt))
    tokens_output = len(enc.encode(output_as_text))

    total_tokens = tokens_prompt + tokens_output

    return {
        "tokens_prompt_estimated": tokens_prompt,
        "tokens_completion_estimated": tokens_output,
        "total_tokens_estimated": total_tokens
    }

def calculate_latency_ms(start_time: float, end_time: float) -> float:
    return round((end_time - start_time)* 1000 ,2)


def calculate_estimated_cost_usd(
        prompt_tokens: int,
        completion_tokens: int,
        input_price_per_1m: float = 0.15,
        outout_price_per_1m: float = 0.6,
) -> float:
    
    input_cost = (prompt_tokens / 1_000_000) * input_price_per_1m
    output_cost = (completion_tokens / 1_000_000) * outout_price_per_1m

    return round(input_cost + output_cost, 8)

def build_metrics (response:Any, start_time: float, end_time: float, prompt: str, output: dict):

    token_usage = get_token_usage_from_response(response)
    estimated_token = estimate_tokens_with_tiktoken(prompt, output)
    latency_ms = calculate_latency_ms(start_time, end_time)
    estimated_cost_usd = calculate_estimated_cost_usd(
        prompt_tokens=token_usage["tokens_prompt"],
        completion_tokens=token_usage["tokens_completion"],
    )

    return {
        **token_usage,
        **estimated_token,
        "latency_ms": latency_ms,
        "estimated_cost_usd" : estimated_cost_usd
    }


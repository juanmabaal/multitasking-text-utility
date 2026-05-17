from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel

from src.llm_client import get_initial_support_response
from src.feedback import feedback_response
from src.refiner import refine_response
from src.metrics_store import save_metrics_csv

app = FastAPI(
    title="Multitasking Text Utility API",
    description="API for running the support assistant LLM pipeline.",
    version="1.0.0",
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "Multitasking Text Utility API is running"}

@app.post("/query")
def run_query(request: QueryRequest) -> dict[str,Any]:
    user_question = request.question
    initial_result = get_initial_support_response(user_question)
    reviewed = feedback_response(user_question, initial_result)
    
    total_tokens = initial_result['initial_metrics']['total_tokens']  + reviewed['feedback_metrics']['total_tokens']

    total_usd = initial_result['initial_metrics']['estimated_cost_usd']  + reviewed['feedback_metrics']['estimated_cost_usd']

    total_latency = initial_result['initial_metrics']['latency_ms']  + reviewed['feedback_metrics']['latency_ms']

    should_refine = reviewed['feedback_response']['feedback_output']['should_refine']

    if should_refine:
        refined = refine_response(user_question, initial_result, reviewed)
        final_response = refined["refined_response"]

        total_tokens += refined["refiner_metrics"]["total_tokens"]
        total_usd += refined["refiner_metrics"]["estimated_cost_usd"]
        total_latency += refined["refiner_metrics"]["latency_ms"]

        refinement_applied = True
    else:
        refined = None
        final_response = {
        "support_output": initial_result["support_output"]
        }
        refinement_applied = False

    save_metrics_csv(
        user_input=user_question,
        total_tokens=total_tokens,
        total_cost_usd=total_usd,
        total_latency_ms=total_latency,
        refinement_applied=refinement_applied,
    )

    return {
        "initial_response": initial_result,
        "feedback": reviewed,
        "refined": refined,
        "final_response": final_response,
        "summary_metrics": {
            "total_tokens": total_tokens,
            "total_cost_usd": total_usd,
            "total_latency_ms": total_latency,
            "refinement_applied": refinement_applied,
        },
    }
import json
from typing import Any
from openai_runner import call_json_and_build_metrics


def refine_response(
    user_question: str,
    first_response: dict[str, Any],
    feedback_response: dict[str, Any],
) -> dict[str, Any]:
    feedback_output = feedback_response.get("feedback_response", {}).get("feedback_output", {})
    should_refine = feedback_output.get("should_refine", False)
    issues_detected = feedback_output.get("issues_detected", [])

    if not should_refine:
        return {
            "refined_response": first_response,
            "refiner_metrics": None,
            "refinement_applied": False,
        }

    system_prompt = (
        "Eres un especialista en refinamiento de respuestas de soporte al cliente. "
        "Debes mejorar la respuesta inicial corrigiendo los problemas detectados, "
        "manteniendo una salida estrictamente en JSON válido."
    )

    user_prompt = f"""
Contexto: pregunta original del cliente
{user_question}

Respuesta inicial:
{json.dumps(first_response, ensure_ascii=False, indent=2)}

Problemas detectados por el auditor:
{json.dumps(issues_detected, ensure_ascii=False, indent=2)}

Tarea:
- Mejora la respuesta inicial corrigiendo los problemas detectados.
- Mantén el mismo formato del schema.
- La nueva respuesta debe ser más clara, útil, específica y profesional.
- "category" debe ser una de:
  "billing", "technical", "account", "subscription", "payment", "refund",
  "login", "bug", "feature_request", "cancellation", "general"
- "priority" debe ser una de:
  "low", "medium", "high"
- "status" debe ser uno de:
  "auto_resolved", "needs_human_review"
- "actions" debe contener 3 o 4 pasos claros.

Devuelve únicamente JSON válido con esta estructura EXACTA:

{{
  "support_output": {{
    "category": "billing",
    "priority": "high",
    "answer": "Texto refinado de respuesta",
    "actions": [
      "Acción 1",
      "Acción 2",
      "Acción 3"
    ],
    "status": "needs_human_review"
  }}
}}
""".strip()

    refine_result = call_json_and_build_metrics(system_prompt, user_prompt)

    return {
        "refined_response": refine_result["response"],
        "refiner_metrics": refine_result["metrics"],
        "refinement_applied": True,
    }
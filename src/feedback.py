import json
from  typing import Any
from openai_runner import call_json_and_build_metrics


def feedback_response(user_question: str, first_response: dict[str, Any] ) -> dict[str, Any]:

    system_prompt = (
        "Eres un auditor critico de calidad de respuestas de atencion al cliente y prompting"
        "Evaluas categoria, prioridad, respuesta, acciones y status"
        "Debes devolver únicamente JSON válido."
    )

    user_prompt = f"""
        Contexto: pregunta del cliente
        {user_question}

        la respuesta inicial a evaluar:
        {json.dumps(first_response, ensure_ascii=False, indent=2)}

        Evalúa la calidad de la respuesta asignando un puntaje de 0.0 a 1.0 para cada criterio:

            category
            Clasificación: ¿Corresponde al departamento o área temática correcta del negocio?

            priority
            Urgencia: ¿Se alinea con el nivel de impacto o riesgo para el usuario?

            answer
            Resolución: ¿La explicación aborda directamente la raíz del problema?
            Tono: ¿Mantiene la voz de marca y el nivel de empatía esperado?

            actions
            Eficacia: ¿Los pasos sugeridos solucionan el problema o son redundantes?
            Viabilidad: ¿El usuario tiene los permisos y herramientas para ejecutar lo indicado?

            status
            Protocolo: ¿El flujo de trabajo (humano o automático) es el adecuado para este caso?

            Reglas:
            - Si algún score es menor a 0.8, entonces "should_refine" debe ser true.
            - Si todos los scores son mayores o iguales a 0.8, entonces "should_refine" debe ser false.
            - "issues_detected" debe contener una lista breve y clara de problemas encontrados.
            - Si no hay problemas importantes, devuelve una lista vacía en "issues_detected".

            Devuelve únicamente JSON válido con la siguiente estructura EXACTA:

            {{
            "feedback_output": {{
                "scores": {{
                "category": 0.0,
                "priority": 0.0,
                "answer": 0.0,
                "actions": 0.0,
                "status": 0.0
                }},
                "should_refine": true,
                "issues_detected": [
                "Describe aquí un problema detectado"
                ]
            }}
            }}
            """.strip()

    feedback_result = call_json_and_build_metrics(system_prompt, user_prompt)

    return {
        "feedback_response": feedback_result['response'],
        "feedback_metrics": feedback_result['metrics']
    }
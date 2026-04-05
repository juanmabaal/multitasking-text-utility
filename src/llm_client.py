# OpenAI client utilities for sending prompts and receiving structured responses.
import os, json
from  typing import Any
from dotenv import load_dotenv
from openai import OpenAI
from schema import SupportResponse

def get_client_and_model() -> tuple[OpenAI, str]:
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY no esta definida en el archivo .env')

    return OpenAI(api_key=api_key), os.getenv('OPENAI_MODEL', 'gpt-4o-mini')


def get_support_response(user_question: str) -> dict[str, Any]:
    client, model = get_client_and_model()
    system_prompt = """ 
        Eres un agente senior de seniors de soporte al cliente, experimentado con mas de 15 años de experperiencia. Te encargas de darle respuestas experimentadas a las solicitudes, quejas, y reclamos de los clientes.
    """

    prompt = f"""
            Analiza la solicitud del cliente y clasifícala según los campos requeridos.

            Reglas:
            - "category" debe ser una de las siguientes:
            "billing", "technical", "account", "subscription", "payment", "refund",
            "login", "bug", "feature_request", "cancellation", "general"
            - "priority" debe ser una de: "low", "medium", "high"
            - "answer" debe ser profesional, concisa y útil
            - "actions" debe contener de 3 a 4 pasos claros que el cliente debe seguir
            - "status" debe ser uno de:
            "auto_resolved" o "needs_human_review"
            - "confidences" debe proporcionar un puntaje de confianza entre 0.0 y 1.0 para:
            "category", "priority", "answer", "actions" y "status"

            Devuelve SOLO JSON válido con la siguiente estructura exacta:

            {{
            "support_output": {{
                "confidences": {{
                "category": 0.9,
                "priority": 0.8,
                "answer": 0.95,
                "actions": 0.85,
                "status": 0.9
                }},
                "category": "general",
                "priority": "medium",
                "answer": "Texto de respuesta profesional",
                "actions": [
                "Primera acción",
                "Segunda acción",
                "Tercera acción"
                ],
                "status": "needs_human_review"
            }}
            }}

            Pregunta del cliente:
            {user_question}
            """
    response = client.chat.completions.create(
        model = model,
        response_format={'type': 'json_object'},
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    parsed_content = json.loads(content)

    validated_response = SupportResponse.model_validate(parsed_content)

    return validated_response.model_dump()

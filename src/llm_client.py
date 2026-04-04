# OpenAI client utilities for sending prompts and receiving structured responses.
import os, json
from  typing import Any
from dotenv import load_dotenv
from openai import OpenAI

def get_client_and_model() -> tuple[OpenAI, str]:
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    print(api_key)
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY no esta definida en el archivo .env')

    return OpenAI(api_key=api_key), os.getenv('OPENAI_MODEL', 'gpt-4o-mini')


def get_support_response(user_question: str) -> dict:
    client, model = get_client_and_model()
    system_prompt = """ 
        Eres un agente senior de seniors de soporte al cliente, experimentado con mas de 15 años de experperiencia. Te encargas de darle respuestas experimentadas a las solicitudes, quejas, y reclamos de los clientes.
    """

    prompt = """ 
        Eres un agente de soporte:

        Evalua la pregunta del cliente y evalua su contenido:
        - categoty: Que es lo que el cliente necesita? A que categoria de estas: 'billing', 'technical', 'account', 'subscription', 'payment', 'refund', 'login', 'bug', 'feature_request', 'cancellation', 'general' => es el tipo de pregunta del cliente?
        - priority: Cual es el nivel de prioridad de la pregunta o solicitud.
        - answer: da una respuesta profesional y formal al cliente
        - actions: lista de acciones de pasos que el cliente debe seguir resolver, de 3 a 4 acciones
        - status: si puede ser resuelta por cliente o necesita una revision tecnica para darle solucion al cliente
        - confidences: para el portenzaje de consianza de cada item retorna un puntaje de calificacion de la salida de 0 a 1

        Devuelve siempre un JSON con la siguiente estructura:
        {{
            'confidences': {{
                'categoty': 0,
                'priority': 0,
                'answer': 0,
                'actions': 0,
                'status': 0
            }},
            'category': 'billing'| 'technical'| 'account'| 'subscription'| 'payment'| 'refund'| 'login'| 'bug'| 'feature_request'| 'cancellation'| 'general',
            "priority": "low | medium | high",
            "answer": "string",
            "actions": ["string"],
            "status": "auto_resolved | needs_human_review"
        }}

        user_question:
        {user_question}
    """
    response = client.chat.completions.create(
        model = model,
        response_format={'type': 'json_object'},
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    return json.loads(content)

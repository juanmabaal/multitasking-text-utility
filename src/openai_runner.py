import os, json, time
from  typing import Any
from dotenv import load_dotenv
from openai import OpenAI
from metrics_logger import build_metrics

def get_client_and_model() -> tuple[OpenAI, str]:
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY no esta definida en el archivo .env')

    return OpenAI(api_key=api_key), os.getenv('OPENAI_MODEL', 'gpt-4o-mini')


def call_json_and_build_metrics(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> dict[str, Any]:

    client, model = get_client_and_model()

    start_time = time.perf_counter()
    response = client.chat.completions.create(
        model = model,
        temperature=temperature,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    end_time = time.perf_counter()

    content = response.choices[0].message.content

    parsed_content = json.loads(content)

    if not content:
        raise RuntimeError("El modelo devolvió contenido vacío")

    metrics = build_metrics(response, start_time, end_time, user_prompt, parsed_content)

    return {
        'response': parsed_content,
        'metrics': metrics
    }


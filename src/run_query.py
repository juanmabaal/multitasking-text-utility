# Entry point for running a support query against the OpenAI API.
import json
from llm_client import get_initial_support_response
from feedback import feedback_response
from refiner import refine_response

def main():
    print('Hola!, Estamos para servirle. Diganos como le podemos ayudar')
    user_request = input('Tu: ')

    initial_result = get_initial_support_response(user_request)
    reviewed = feedback_response(user_request, initial_result)
    
    total_tokens = initial_result['initial_metrics']['total_tokens']  + reviewed['feedback_metrics']['total_tokens']

    total_usd = initial_result['initial_metrics']['estimated_cost_usd']  + reviewed['feedback_metrics']['estimated_cost_usd']

    total_latency = initial_result['initial_metrics']['latency_ms']  + reviewed['feedback_metrics']['latency_ms']

    should_refine = reviewed['feedback_response']['feedback_output']['should_refine']

    print("\n" + "=" * 80)
    print("=== Respuesta Inicial ===")
    print(json.dumps(initial_result, ensure_ascii=False, indent=2))

    print("\n" + "=" * 80)
    print("=== Feedback ===")
    print(json.dumps(reviewed, ensure_ascii=False, indent=2))

    if should_refine:
          refined = refine_response(user_request, initial_result, reviewed)
          final_response = refined['refined_response']
          print("\n" + "=" * 80)
          print("=== Refined ===")
          print(json.dumps(refined, ensure_ascii=False, indent=2))

          total_tokens += refined['refiner_metrics']['total_tokens']
          total_usd += refined['refiner_metrics']['estimated_cost_usd']
          total_latency += refined['refiner_metrics']['latency_ms']
    
    else: 
         final_response = initial_result['Initial_response']
    

    print("\n" + "=" * 80)
    print("=== Final Response ===")
    print(json.dumps(final_response, ensure_ascii=False, indent=2))

    print("\n" + "=" * 80)
    print("=== metricas ===")
    print(f"Total de Tokens consumidos: {total_tokens}")
    print(f"Gastos en USD estimado: {total_usd}")
    print(f"El tiempo total de espera para obtener la respuesta fue de: {total_latency} milisegundos")

if __name__ == '__main__':
    main()
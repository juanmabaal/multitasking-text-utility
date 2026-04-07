# Entry point for running a support query against the OpenAI API.
import json
from llm_client import get_initial_support_response
from feedback import feedback_response

def main():
    print('Hola!, Estamos para servirle. Diganos como le podemos ayudar')
    user_request = input('Tu: ')
    initial_result = get_initial_support_response(user_request)
    
    print("=" * 80)
    print(f"Respuesta Inicial de : {user_request}")
    print("\n" + "=" * 80)
    print("\n=== Respuesta Inicial===")
    print(json.dumps(initial_result, ensure_ascii=False, indent=2))

    print("\n" + "=" * 80)
    reviewed = feedback_response(user_request, initial_result)
    print("\n=== Respuesta Feedback ===")
    print("\n" + "=" * 80)
    print(json.dumps(reviewed, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
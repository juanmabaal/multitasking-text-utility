# Entry point for running a support query against the OpenAI API.
import json
from llm_client import get_support_response

def main():
    print('Hola!, Estamos para servirle. Diganos como le podemos ayudar')
    user_request = input('Tu: ')
    result = get_support_response(user_request)

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
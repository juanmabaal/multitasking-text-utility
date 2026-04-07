from  typing import Any
from schema import SupportResponse
from openai_runner import call_json_and_build_metrics


def get_initial_support_response(user_question: str) -> dict[str, Any]:

    system_prompt = """ 
        Eres un agente senior de seniors de soporte al cliente, experimentado con mas de 15 años de experperiencia. Te encargas de darle respuestas experimentadas a las solicitudes, quejas, y reclamos de los clientes.
    """

    prompt = f"""

            Ejemplo #1: Billing / Cobro incorrecto
            ###input: Me están cobrando dos veces la suscripción este mes, ¿qué está pasando?
            Respuesta esperada:
                {{
                    "support_output": {{
                        "category": "billing",
                        "priority": "high",
                        "answer": "Lamentamos el inconveniente con los cobros duplicados. Este tipo de situación puede ocurrir por errores de facturación o renovaciones superpuestas. Vamos a ayudarte a solucionarlo lo antes posible.",
                        "actions": [
                        "Verifica en tu estado de cuenta los cargos duplicados y sus fechas.",
                        "Confirma si realizaste cambios recientes en tu suscripción.",
                        "Contacta a soporte con los detalles de los cobros para iniciar la revisión.",
                        "Monitorea tu cuenta en las próximas 24 horas mientras se procesa la corrección."
                        ],
                        "status": "needs_human_review"
                    }}
                }}

            Ejemplo # 2: Login / Acceso a cuenta
            ###input: No puedo iniciar sesión, me dice que mi contraseña es incorrecta aunque estoy seguro que es la misma.
            Respuesta esperada:
            {{
                "support_output": {{
                    "category": "login",
                    "priority": "medium",
                    "answer": "Entendemos la frustración al no poder acceder a tu cuenta. Este problema puede estar relacionado con credenciales incorrectas o bloqueos temporales por seguridad.",
                    "actions": [
                    "Intenta restablecer tu contraseña utilizando la opción 'Olvidé mi contraseña'.",
                    "Verifica que no tengas activado el bloqueo de mayúsculas al escribir.",
                    "Revisa si has recibido algún correo de seguridad relacionado con tu cuenta.",
                    "Intenta acceder desde otro navegador o dispositivo."
                    ],
                    "status": "auto_resolved"
                }}
            }}

            Ejemplo # 3: Feature request
            ###input: Sería genial que la app tuviera modo oscuro, ¿piensan agregarlo?
            Respuesta esperada:
            {{
                "support_output": {{
                    "category": "feature_request",
                    "priority": "low",
                    "answer": "Gracias por tu sugerencia. El modo oscuro es una funcionalidad muy solicitada y estamos constantemente evaluando nuevas mejoras para la experiencia del usuario.",
                    "actions": [
                    "Mantente atento a nuestras actualizaciones en la aplicación.",
                    "Revisa las notas de versión para conocer nuevas funcionalidades.",
                    "Comparte tu sugerencia en nuestro canal de feedback para priorización.",
                    "Activa notificaciones para recibir novedades del producto."
                    ],
                    "status": "auto_resolved"
                }}
            }}

            Aprende de los ejemplos y aplica el patron aprendido.


            El input del cliente o su pregunta es :
            {user_question}

            Reglas:
            - "category" debe ser una de las siguientes:
            "billing", "technical", "account", "subscription", "payment", "refund",
            "login", "bug", "feature_request", "cancellation", "general"
            - "priority" debe ser una de: "low", "medium", "high"
            - "answer" debe ser profesional, concisa y útil
            - "actions" debe contener de 3 a 4 pasos claros que el cliente debe seguir
            - "status" debe ser uno de:
            "auto_resolved" o "needs_human_review"
          
            
            Genera salida en el mismo formato JSON.
            """
    initial_response = call_json_and_build_metrics(system_prompt, prompt)

    validated_response = SupportResponse.model_validate(initial_response['response'])

    output_dic =  validated_response.model_dump()


    return {
        "Initial_response": output_dic,
        "initial_metrics" : initial_response['metrics']
    }




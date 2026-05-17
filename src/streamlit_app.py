import requests
import streamlit as st
from typing import Any

API_URL = "http://127.0.0.1:8000/query"

def configure_page() -> None:
    st.set_page_config(
        page_title="Support Assistant",
        page_icon="🧠",
        layout="wide",
    )

def render_header() -> None:
    st.title("🧠 Multitasking Text Utility")
    st.subheader("LLM Support Assistant with Feedback & Conditional Refinement")
    st.write(
        "Interfaz para enviar preguntas al endpoint FastAPI y visualizar "
        "respuesta final, feedback de calidad y métricas del pipeline."
    )

def call_api(user_question: str) -> dict[str, Any]:
    response = requests.post(
        API_URL,
        json={"question": user_question},
        timeout=90
    )
    response.raise_for_status()
    return response.json()

def render_metrics(metrics: dict[str, Any]) -> None:
    st.header("📊 Métricas generales")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Tokens", metrics.get("total_tokens", "N/A"))
    
    with col2:
        st.metric("Costo estimado USD", metrics.get("total_cost_usd", "N/A"))

    with col3:
        st.metric("Latencia total ms", metrics.get("total_latency_ms", "N/A"))

    with col4:
        st.metric(
            "Refinement aplicado",
            str(metrics.get("refinement_applied", "N/A")),
        )

def render_pipeline_result(data: dict[str, Any]) -> None:
    final_response = data.get("final_response", {})
    feedback = data.get("feedback", {})
    refined = data.get("refined")
    metrics = data.get("summary_metrics", {})

    st.success("Pipeline ejecutado correctamente.")

    st.divider()

    st.header("✅ Respuesta final")

    st.json(final_response, expanded=True)

    st.divider()

    render_metrics(metrics)

    st.divider()

    st.header("🧪 Feedback de calidad")

    st.json(feedback, expanded=True)

    st.divider()

    if refined is not None:
        st.header("🔁 Respuesta refinada")
        st.json(refined, expanded=True)
    else:
        st.info("No se aplicó refinamiento porque los scores fueron suficientes.")

    with st.expander("Ver respuesta completa de la API"):
        st.json(data, expanded=True)

def render_errors(error: Exception) -> None:
    if isinstance(error, requests.exceptions.ConnectionError):
        st.error(
            "No se pudo conectar con FastAPI. "
            "Asegúrate de tener la API corriendo con: "
            "`uvicorn src.api:app --reload`"
        )
    elif isinstance(error, requests.exceptions.Timeout):
        st.error("La solicitud tardó demasiado. Intenta nuevamente.")
    elif isinstance(error, requests.exceptions.HTTPError):
        st.error(f"Error HTTP desde la API: {error}")
    else:
        st.error(f"Ocurrió un error inesperado: {error}")

def main() -> None:
    configure_page()
    render_header()

    user_question = st.text_area(
        "Escribe cual es tu solicitud, queja o reclamo:",
        placeholder="Ejemplo: No puedo acceder a mi cuenta y necesito cambiar mi método de pago.",
        height=140,
    )

    run_button = st.button("Ejecutar análisis")

    if run_button:
        if not user_question.strip():
            st.warning("Por favor escribe tu solicitud para continuar.")
            return
        
        with st.spinner("Ejecutando pipeline..."):
            try:
                data = call_api(user_question)
                render_pipeline_result(data)
            except Exception as error:
                render_errors(error)

if __name__ == "__main__":
    main()
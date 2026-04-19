from groq import Groq
from Config import GROQ_API_KEY

cliente_groq = Groq(api_key=GROQ_API_KEY)

def generar_preguntas_ia(texto: str, config: dict):
    """
    config debe contener: 
    {
        "cantidad": int, 
        "dificultad": str, 
        "tipo": str (ej: "opción múltiple", "abierta", "mixto")
    }
    """
    
    # Construcción dinámica del prompt según la configuración
    prompt = f"""
    Eres un experto en pedagogía. Basándote en el texto proporcionado, genera una evaluación con las siguientes características:
    - Cantidad de preguntas: {config.get('cantidad', 5)}
    - Nivel de dificultad (Taxonomía de Bloom): {config.get('dificultad', 'Comprensión')}
    - Tipo de preguntas: {config.get('tipo', 'opción múltiple')}

    Responde ÚNICAMENTE con un JSON válido con esta estructura:
    {{
        "evaluacion_info": {{
            "dificultad": "{config.get('dificultad')}",
            "tipo": "{config.get('tipo')}"
        }},
        "preguntas": [
            {{
                "pregunta": "texto de la pregunta",
                "opciones": ["A) ..", "B) ..", "C) ..", "D) .."], # Solo si es opción múltiple
                "respuesta_correcta": "A) .. o texto sugerido si es abierta",
                "explicacion": "Breve explicación de por qué es la respuesta correcta"
            }}
        ]
    }}

    Texto:
    {texto[:4000]}
    """

    respuesta = cliente_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6 # Un poco más bajo para mayor coherencia pedagógica
    )

    contenido = respuesta.choices[0].message.content.strip()

    # limpiar bloques ```json
    if contenido.startswith("```"):
        contenido = contenido.split("```")[1]
        if contenido.startswith("json"):
            contenido = contenido[4:]

    import json
    return json.loads(contenido)
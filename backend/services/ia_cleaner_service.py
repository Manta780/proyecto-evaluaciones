from groq import Groq
from Config import GROQ_API_KEY

cliente_groq = Groq(api_key=GROQ_API_KEY)


def limpiar_texto(texto: str) -> str:
    """
    Limpia y corrige texto de cualquier fuente (OCR, documentos escaneados,
    PDFs con formato incorrecto, texto con caracteres corruptos, etc.).

    Corrige:
    - Caracteres mal interpretados o corruptos
    - Palabras separadas o unidas incorrectamente
    - Saltos de línea que rompen palabras o frases
    - Espacios múltiples o incorrectos
    - Caracteres especiales extraños
    - Texto mal codificado (encoding issues)
    """
    prompt = f"""
Eres un experto en corrección de texto. Tu tarea es limpiar cualquier texto que tenga problemas de transcripción o formato.

Corrige los siguientes problemas:
1. Caracteres mal interpretados o corruptos (ej: rn → m, cl → d, vv → w)
2. Palabras separadas incorrectamente (ej: "pa labra" → "palabra")
3. Palabras unidas incorrectamente (ej: "enel" → "en el")
4. Caracteres especiales extraños o símbolos corruptos
5. Saltos de línea que rompen palabras o frases incompletas
6. Espacios múltiples, incorrectos o faltantes
7. Problemas de codificación (caracteres extraños por encoding incorrecto)
8. Texto incompleto o truncado

Mantén:
- La puntuación original
- La estructura general del texto
- El significado original
- Mayúsculas y minúsculas según corresponda

Devuelve ÚNICAMENTE el texto limpio, sin explicaciones ni comentarios.

Texto a limpiar:
---
{texto}
---
"""
    respuesta = cliente_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return respuesta.choices[0].message.content.strip()


def corregir_ortografia(texto: str) -> str:
    """
    Corrige errores de ortografía y gramática en español.
    Funciona con cualquier tipo de texto, sin importar su origen.
    """
    prompt = f"""
Eres un experto en ortografía y gramática del español. Tu tarea es corregir todos los errores ortográficos y gramaticales del siguiente texto.

Corrige:
1. Errores de ortografía (tildes, b/v, s/c/z, g/j, haches faltantes, etc.)
2. Errores de gramática (concordancia de género y número, uso incorrecto de preposiciones, etc.)
3. Frases confusas o ambiguas que dificulten la comprensión
4. Redundancias innecesarias
5. Uso incorrecto de signos de puntuación

Importante:
- NO cambies el significado del texto
- NO agregues información que no esté en el original
- Mantén el estilo y tono del autor
- Devuelve el texto en el mismo idioma (español)

Devuelve ÚNICAMENTE el texto corregido, sin explicaciones ni comentarios.

Texto a corregir:
---
{texto}
---
"""
    respuesta = cliente_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return respuesta.choices[0].message.content.strip()


def mejorar_redaccion(texto: str) -> str:
    """
    Mejora la redacción de cualquier texto para mayor claridad y fluidez.
    No solo corrige errores, sino que mejora la estructura y expresión.
    """
    prompt = f"""
Eres un experto en redacción y expresión escrita en español. Tu tarea es mejorar la redacción del siguiente texto.

Mejora:
1. Claridad de frases confusas o ambiguas
2. Estructura de oraciones complejas
3. Transiciones entre oraciones y párrafos
4. Elimina redundancias y palabras innecesarias
5. Corrige problemas de cohesión y coherencia
6. Mejora la fluidez general del texto

Importante:
- NO cambies el significado del texto
- NO agregues información que no esté en el original
- Mantén el tono y estilo del autor original
- Si hay partes ambiguas, intenta mantener el sentido original
- Devuelve el texto en el mismo idioma (español)

Devuelve ÚNICAMENTE el texto mejorado, sin explicaciones ni comentarios.

Texto a mejorar:
---
{texto}
---
"""
    respuesta = cliente_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return respuesta.choices[0].message.content.strip()


def limpieza_completa(texto: str) -> str:
    """
    Limpieza completa en UNA sola llamada a la IA.
    Hace todo: limpiar caracteres corruptos + ortografía + redacción mejorada.
    Más rápido y usa menos tokens que hacer 3 llamadas separadas.
    """
    prompt = f"""
Eres un experto en procesamiento y mejora de texto en español. Analiza y mejora el siguiente texto aplicando TODAS estas correcciones en un solo paso:

1. CARACTERES CORRUPTOS: Corrige caracteres mal interpretados (rn→m, cl→d, vv→w, 0→O, l→I), símbolos extraños y problemas de encoding.

2. PALABRAS MAL SEPARADAS/UNIDAS: Une palabras separadas incorrectamente y separa palabras unidas incorrectamente.

3. ORTOGRAFÍA Y GRAMÁTICA: Corrige tildes, b/v, s/c/z, g/j, haches faltantes, concordancia de género/número, preposiciones incorrectas.

4. PUNTUACIÓN Y FORMATO: Corrige signos de puntuación incorrectos, espacios múltiples, saltos de línea que rompen frases.

5. CLARIDAD Y FLUIDEZ: Mejora frases confusas, elimina redundancias, mejora transiciones.

REGLAS ABSOLUTAS:
- NO cambies el significado del texto
- NO agregues información que no exista en el original
- NO inventes ni completes texto truncado
- Mantén la estructura original (párrafos, listas, etc.)
- Devuelve ÚNICAMENTE el texto mejorado, SIN explicaciones ni comentarios

Texto a procesar:
---
{texto}
---
"""
    respuesta = cliente_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return respuesta.choices[0].message.content.strip()


def limpieza_rapida(texto: str) -> str:
    """
    Limpieza rápida en UNA sola llamada.
    Solo limpia caracteres corruptos y problemas de formato.
    No incluye mejora de redacción para máxima velocidad.
    Útil para textos que ya tienen buena ortografía.
    """
    prompt = f"""
Eres un experto en corrección de texto. Limpia el siguiente texto aplicando solo estas correcciones:

1. Caracteres corruptos o mal interpretados (rn→m, cl→d, vv→w, etc.)
2. Palabras separadas/unidas incorrectamente
3. Espacios múltiples o faltantes
4. Saltos de línea que rompen palabras
5. Símbolos extraños por problemas de encoding

NO corrijas ortografía ni gramática, solo limpia el formato y caracteres.

Devuelve ÚNICAMENTE el texto limpio, sin explicaciones.

Texto:
---
{texto}
---
"""
    respuesta = cliente_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return respuesta.choices[0].message.content.strip()
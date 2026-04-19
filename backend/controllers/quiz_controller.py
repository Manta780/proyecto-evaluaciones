from fastapi import UploadFile, HTTPException
from services.pdf_service import extract_text
from services.ia_service import generar_preguntas_ia

# Añadimos 'config' como segundo parámetro
async def generar_quiz(archivo: UploadFile, config: dict): 
    try:
        # 1. Leer el archivo
        contenido = await archivo.read()

        # 2. Extraer texto (esto ya lo tienes bien)
        texto = extract_text(contenido, archivo.filename)

        if not texto.strip():
            raise HTTPException(status_code=400, detail="No se pudo extraer texto")

        # 3. Llamar a la IA pasando el texto Y la configuración
        # IMPORTANTE: Verifica que en ia_service.py la función reciba dos argumentos también
        resultado = generar_preguntas_ia(texto, config)

        return {
            "archivo": archivo.filename,
            "configuracion_aplicada": config, # Es bueno devolver esto para confirmar
            "preguntas": resultado["preguntas"]
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Esto te ayudará a ver errores inesperados en la consola
        print(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Error interno al generar el quiz")
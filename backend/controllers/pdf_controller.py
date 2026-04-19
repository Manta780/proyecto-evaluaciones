from fastapi import UploadFile, HTTPException
from services.pdf_service import extract_text

async def procesar_pdf(archivo: UploadFile):
    contenido = await archivo.read()

    texto = extract_text(contenido, archivo.filename)

    if not texto.strip():
        raise HTTPException(status_code=400, detail="No se pudo extraer texto")

    return {
        "nombre": archivo.filename,
        "texto": texto
    }
from fastapi import UploadFile, HTTPException
from services.pdf_service import extract_text

async def procesar_pdf(archivo: UploadFile, modo_limpieza: str = "completa"):
    """
    Args:
        modo_limpieza: "completa", "rapida", "ninguna"
    """
    try:
        contenido = await archivo.read()

        # extract_text ya aplica la limpieza según el modo
        texto = extract_text(contenido, archivo.filename, modo_limpieza=modo_limpieza)

        if not texto.strip():
            raise HTTPException(status_code=400, detail="No se pudo extraer texto")

        return {
            "nombre": archivo.filename,
            "texto": texto,
            "modo_limpieza": modo_limpieza
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al procesar archivo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar: {str(e)}")
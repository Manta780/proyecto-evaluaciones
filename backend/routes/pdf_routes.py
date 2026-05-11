from fastapi import APIRouter, UploadFile, File, Query
from controllers.pdf_controller import procesar_pdf

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/extraer")
async def extraer(
    archivo: UploadFile = File(...),
    modo_limpieza: str = Query("completa", description="Tipo de limpieza: completa, rapida, ninguna")
):
    return await procesar_pdf(archivo, modo_limpieza=modo_limpieza)
from fastapi import APIRouter, UploadFile, File
from controllers.pdf_controller import procesar_pdf

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/extraer")
async def extraer(archivo: UploadFile = File(...)):
    return await procesar_pdf(archivo)
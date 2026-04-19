from fastapi import APIRouter, UploadFile, File, Form
from controllers.quiz_controller import generar_quiz

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.post("/generar")
async def generar(
    archivo: UploadFile = File(...),
    cantidad: int = Form(5),
    dificultad: str = Form("Comprensión"),
    tipo: str = Form("opción múltiple")
):
    # Creamos un diccionario con la configuración
    config = {
        "cantidad": cantidad,
        "dificultad": dificultad,
        "tipo": tipo
    }
    # Pasamos el archivo y la configuración al controlador
    return await generar_quiz(archivo, config)
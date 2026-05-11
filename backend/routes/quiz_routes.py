from fastapi import APIRouter, UploadFile, File, Form, Depends, Header
from sqlalchemy.orm import Session
from controllers.quiz_controller import generar_quiz
from database import get_db

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.post("/generar")
async def generar(
    archivo: UploadFile = File(...),
    cantidad: int = Form(5),
    dificultad: str = Form("Comprensión"),
    tipo: str = Form("opción múltiple"),
    modo_limpieza: str = Form("completa"),
    title: str = Form(None),
    description: str = Form(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    config = {
        "cantidad": cantidad,
        "dificultad": dificultad,
        "tipo": tipo,
        "title": title,
        "description": description
    }
    return await generar_quiz(archivo, config, modo_limpieza=modo_limpieza, authorization=authorization, db=db)
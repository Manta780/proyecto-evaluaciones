from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from controllers.quiz_CRUD_controller import (
     QuizUpdate, QuestionCreate, QuestionUpdate,
    obtener_quiz, obtener_quiz_por_codigo, listar_quizzes_creador,
    actualizar_quiz, eliminar_quiz, agregar_pregunta, actualizar_pregunta, eliminar_pregunta, buscar_quiz_por_titulo
)

router = APIRouter(prefix="/quiz", tags=["Quiz CRUD"])

@router.get("/obtener_quiz/{quiz_id}")
def get_quiz(quiz_id: str, db: Session = Depends(get_db)):
    """Obtiene un quiz por ID"""
    return obtener_quiz(quiz_id, db)

@router.get("/code/{access_code}")
def get_quiz_by_code(access_code: str, db: Session = Depends(get_db)):
    """Obtiene un quiz por código de acceso"""
    return obtener_quiz_por_codigo(access_code, db)

@router.get("/creator/{creator_id}")
def get_quizzes_by_creator(creator_id: str, db: Session = Depends(get_db)):
    """Lista todos los quizzes de un creador"""
    return listar_quizzes_creador(creator_id, db)

@router.put("/actualizar_quiz/{quiz_id}")
def update_quiz(quiz_id: str, data: QuizUpdate, db: Session = Depends(get_db)):
    """Actualiza un quiz"""
    return actualizar_quiz(quiz_id, data, db)

@router.delete("/eliminar_quiz/{quiz_id}")
def delete_quiz(quiz_id: str, db: Session = Depends(get_db)):
    """Elimina (desactiva) un quiz"""
    return eliminar_quiz(quiz_id, db)

@router.post("/question/agregar_pregunta")
def create_question(data: QuestionCreate, db: Session = Depends(get_db)):
    """Agrega una pregunta a un quiz"""
    return agregar_pregunta(data, db)

@router.put("/question/actualizar_pregunta/{question_id}")
def update_question(question_id: str, data: QuestionUpdate, db: Session = Depends(get_db)):
    """Actualiza una pregunta"""
    return actualizar_pregunta(question_id, data, db)

@router.delete("/question/eliminar_pregunta/{question_id}")
def delete_question(question_id: str, db: Session = Depends(get_db)):
    """Elimina una pregunta"""
    return eliminar_pregunta(question_id, db)

@router.get("/search/{title}")
def buscar_quiz(
    title: str,
    creator_id: int,
    db: Session = Depends(get_db)
):
    return buscar_quiz_por_titulo(
        creator_id,
        title,
        db
    )
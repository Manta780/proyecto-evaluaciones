from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import uuid
from database import get_db
import services.quiz_service as quiz_service

# Pydantic models para request/response

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty_level: Optional[str] = None
    is_active: Optional[bool] = None
    settings: Optional[dict] = None

class QuestionCreate(BaseModel):
    quiz_id: str
    question_type: str
    statement: str
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    points: int = 1

class QuestionUpdate(BaseModel):
    question_type: Optional[str] = None
    statement: Optional[str] = None
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    points: Optional[int] = None


def obtener_quiz(quiz_id: int, db: Session):

    quiz = quiz_service.get_quiz(db, quiz_id)

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")

    questions = quiz_service.get_questions_by_quiz(db, quiz_id)

    return {
        "id": quiz.id,
        "creator_id": quiz.creator_id,
        "title": quiz.title,
        "description": quiz.description,
        "access_code": quiz.access_code,
        "difficulty_level": quiz.difficulty_level,
        "is_active": quiz.is_active,
        "settings": quiz.settings,
        "created_at": quiz.created_at.isoformat(),
        "questions": [
            {
                "id": q.id,
                "question_type": q.question_type,
                "statement": q.statement,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "explanation": q.explanation,
                "points": q.points
            }
            for q in questions
        ]
    }

def obtener_quiz_por_codigo(access_code: str, db: Session):
    quiz = quiz_service.get_quiz_by_code(db, access_code)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")

    questions = quiz_service.get_questions_by_quiz(db, quiz.id)

    return {
        "id": str(quiz.id),
        "title": quiz.title,
        "description": quiz.description,
        "difficulty_level": quiz.difficulty_level,
        "settings": quiz.settings,
        "questions": [
            {
                "id": str(q.id),
                "question_type": q.question_type,
                "statement": q.statement,
                "options": q.options,
                "points": q.points
            }
            for q in questions
        ]
    }

def listar_quizzes_creador(creator_id: str, db: Session):
    quizzes = quiz_service.get_quizzes_by_creator(db, creator_id)
    return [
        {
            "id": str(q.id),
            "title": q.title,
            "description": q.description,
            "access_code": q.access_code,
            "difficulty_level": q.difficulty_level,
            "is_active": q.is_active,
            "created_at": q.created_at.isoformat()
        }
        for q in quizzes
    ]

def actualizar_quiz(quiz_id: int, data: QuizUpdate, db: Session):

    quiz = quiz_service.update_quiz(
        db,
        quiz_id,
        title=data.title,
        description=data.description,
        difficulty_level=data.difficulty_level,
        is_active=data.is_active,
        settings=data.settings
    )

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")

    return {
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "is_active": quiz.is_active,
        "message": "Quiz actualizado correctamente"
    }

def eliminar_quiz(quiz_id: int, db: Session):

    success = quiz_service.delete_quiz(db, quiz_id)

    if not success:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")

    return {"message": "Quiz eliminado correctamente"}

def agregar_pregunta(data: QuestionCreate, db: Session):
    try:
        quiz_uuid = uuid.UUID(data.quiz_id)
        question = quiz_service.add_question(
            db=db,
            quiz_id=quiz_uuid,
            question_type=data.question_type,
            statement=data.statement,
            options=data.options,
            correct_answer=data.correct_answer,
            explanation=data.explanation,
            points=data.points
        )
        return {
            "id": str(question.id),
            "quiz_id": str(question.quiz_id),
            "question_type": question.question_type,
            "statement": question.statement,
            "message": "Pregunta agregada correctamente"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def actualizar_pregunta(question_id: int, data: QuestionUpdate, db: Session):

    question = quiz_service.update_question(
        db,
        question_id,
        question_type=data.question_type,
        statement=data.statement,
        options=data.options,
        correct_answer=data.correct_answer,
        explanation=data.explanation,
        points=data.points
    )

    if not question:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    return {
        "id": question.id,
        "statement": question.statement,
        "message": "Pregunta actualizada correctamente"
    }

def eliminar_pregunta(question_id: int, db: Session):

    success = quiz_service.delete_question(db, question_id)

    if not success:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    return {"message": "Pregunta eliminada correctamente"}


def buscar_quiz_por_titulo(
    creator_id: int,
    title: str,
    db: Session
):

    quizzes = quiz_service.search_quizzes_by_title(
        db,
        creator_id,
        title
    )

    return [
        {
            "id": q.id,
            "title": q.title,
            "description": q.description,
            "access_code": q.access_code,
            "difficulty_level": q.difficulty_level
        }
        for q in quizzes
    ]

from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Quiz, Question
from typing import Optional, List
import random
import string


def generate_access_code() -> str:
    """Genera un código de 6 dígitos único"""
    return ''.join(random.choices(string.digits, k=6))


def create_quiz(
    db: Session,
    creator_id: int,
    title: str,
    description: str = None,
    difficulty_level: str = None,
    settings: dict = None
) -> Quiz:
    """Crea un nuevo quiz"""

    access_code = generate_access_code()

    # Asegurar código único
    while db.query(Quiz).filter(Quiz.access_code == access_code).first():
        access_code = generate_access_code()

    quiz = Quiz(
        creator_id=creator_id,
        title=title,
        description=description,
        access_code=access_code,
        difficulty_level=difficulty_level,
        settings=settings,
        is_active=True
    )

    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return quiz


def get_quiz(db: Session, quiz_id: int) -> Optional[Quiz]:
    """Obtiene un quiz por ID"""
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()


def get_quiz_by_code(db: Session, access_code: str) -> Optional[Quiz]:
    """Obtiene un quiz por código de acceso"""

    return db.query(Quiz).filter(
        and_(
            Quiz.access_code == access_code,
            Quiz.is_active == True
        )
    ).first()


def get_quizzes_by_creator(
    db: Session,
    creator_id: int
) -> List[Quiz]:
    """Obtiene todos los quizzes de un creador"""

    return db.query(Quiz).filter(
        Quiz.creator_id == creator_id
    ).all()


def get_quiz_by_title(
    db: Session,
    creator_id: int,
    title: str
) -> Optional[Quiz]:
    """
    Busca un quiz por título perteneciente a un usuario
    """

    return db.query(Quiz).filter(
        Quiz.creator_id == creator_id,
        Quiz.title.ilike(f"%{title}%"),
        Quiz.is_active == True
    ).first()


def search_quizzes_by_title(
    db: Session,
    creator_id: int,
    title: str
) -> List[Quiz]:
    """
    Busca quizzes por título (retorna lista)
    """
    return db.query(Quiz).filter(
        Quiz.creator_id == creator_id,
        Quiz.title.ilike(f"%{title}%"),
        Quiz.is_active == True
    ).all()


def update_quiz(
    db: Session,
    quiz_id: int,
    **kwargs
) -> Optional[Quiz]:
    """Actualiza un quiz"""

    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id
    ).first()

    if not quiz:
        return None

    allowed_fields = [
        'title',
        'description',
        'difficulty_level',
        'is_active',
        'settings'
    ]

    for field in allowed_fields:
        if field in kwargs and kwargs[field] is not None:
            setattr(quiz, field, kwargs[field])

    db.commit()
    db.refresh(quiz)

    return quiz


def delete_quiz(db: Session, quiz_id: int) -> bool:
    """Soft delete"""

    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id
    ).first()

    if not quiz:
        return False

    quiz.is_active = False

    db.commit()

    return True


def add_question(
    db: Session,
    quiz_id: int,
    question_type: str,
    statement: str,
    options: List[str] = None,
    correct_answer: str = None,
    explanation: str = None,
    points: int = 1
) -> Question:
    """Agrega una pregunta"""

    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id
    ).first()

    if not quiz:
        raise ValueError("Quiz no encontrado")

    question = Question(
        quiz_id=quiz_id,
        question_type=question_type,
        statement=statement,
        options=options,
        correct_answer=correct_answer,
        explanation=explanation,
        points=points
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    return question


def update_question(
    db: Session,
    question_id: int,
    **kwargs
) -> Optional[Question]:
    """Actualiza una pregunta"""

    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        return None

    allowed_fields = [
        'question_type',
        'statement',
        'options',
        'correct_answer',
        'explanation',
        'points'
    ]

    for field in allowed_fields:
        if field in kwargs and kwargs[field] is not None:
            setattr(question, field, kwargs[field])

    db.commit()
    db.refresh(question)

    return question


def delete_question(db: Session, question_id: int) -> bool:
    """Elimina una pregunta"""

    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        return False

    db.delete(question)

    db.commit()

    return True


def get_questions_by_quiz(
    db: Session,
    quiz_id: int
) -> List[Question]:
    """Obtiene preguntas de un quiz"""

    return db.query(Question).filter(
        Question.quiz_id == quiz_id
    ).all()


def bulk_insert_questions(
    db: Session,
    quiz_id: int,
    questions_data: List[dict]
) -> List[Question]:
    """
    Inserta múltiples preguntas
    """

    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id
    ).first()

    if not quiz:
        raise ValueError("Quiz no encontrado")

    questions = []

    for q in questions_data:

        question = Question(
            quiz_id=quiz_id,
            question_type=q.get("question_type", "multiple_choice"),
            statement=q.get("statement", ""),
            options=q.get("options"),
            correct_answer=q.get("correct_answer", ""),
            explanation=q.get("explanation"),
            points=q.get("points", 1)
        )

        questions.append(question)

    db.bulk_save_objects(questions)

    db.commit()

    return db.query(Question).filter(
        Question.quiz_id == quiz_id
    ).all()


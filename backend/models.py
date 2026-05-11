
from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Integer,
    ForeignKey,
    DECIMAL,
    DateTime
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firebase_uid = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(20), default="Estudiante")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    quizzes = relationship("Quiz", back_populates="creator")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)

    creator_id = Column(
        Integer,
        ForeignKey("profiles.id", ondelete="CASCADE")
    )

    title = Column(String(255), nullable=False)

    description = Column(Text)

    access_code = Column(String(6), unique=True, nullable=False)

    difficulty_level = Column(String(50))

    is_active = Column(Boolean, default=True)

    settings = Column(JSONB)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    creator = relationship("Profile", back_populates="quizzes")

    questions = relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan"
    )

    attempts = relationship(
        "Attempt",
        back_populates="quiz",
        cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id", ondelete="CASCADE")
    )

    question_type = Column(String(50), nullable=False)

    statement = Column(Text, nullable=False)

    options = Column(JSONB)

    correct_answer = Column(Text, nullable=False)

    explanation = Column(Text)

    points = Column(Integer, default=1)

    quiz = relationship("Quiz", back_populates="questions")

    responses = relationship(
        "StudentResponse",
        back_populates="question"
    )


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id", ondelete="CASCADE")
    )

    student_name = Column(String(255), nullable=False)

    total_score = Column(DECIMAL(5, 2))

    started_at = Column(DateTime(timezone=True), server_default=func.now())

    finished_at = Column(DateTime(timezone=True))

    quiz = relationship("Quiz", back_populates="attempts")

    responses = relationship(
        "StudentResponse",
        back_populates="attempt",
        cascade="all, delete-orphan"
    )


class StudentResponse(Base):
    __tablename__ = "student_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)

    attempt_id = Column(
        Integer,
        ForeignKey("attempts.id", ondelete="CASCADE")
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id")
    )

    given_answer = Column(Text)

    is_correct = Column(Boolean)

    ai_feedback = Column(Text)

    attempt = relationship("Attempt", back_populates="responses")

    question = relationship("Question", back_populates="responses")



from fastapi import UploadFile, HTTPException, Header, Depends
from sqlalchemy.orm import Session

from database import get_db
from services.pdf_service import extract_text
from services.ia_service import generar_preguntas_ia
from services.quiz_service import create_quiz, bulk_insert_questions
from services.firebase_service import verify_token

from models import Profile


def ensure_profile(db: Session, firebase_uid: str, email: str):
    """
    Verifica si el perfil existe.
    Si no existe, lo crea automáticamente.
    """

    profile = db.query(Profile).filter(
        Profile.firebase_uid == firebase_uid
    ).first()

    if not profile:
        profile = Profile(
            firebase_uid=firebase_uid,
            email=email,
            full_name="",
            role="Estudiante"
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


async def generar_quiz(
    archivo: UploadFile,
    config: dict,
    modo_limpieza: str = "completa",
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Flujo:
    1. Verificar token Firebase
    2. Obtener usuario
    3. Asegurar perfil en DB
    4. Extraer texto PDF
    5. Generar preguntas IA
    6. Crear quiz
    7. Guardar preguntas
    """

    try:

        # =========================
        # 1. Verificar autorización
        # =========================

        if not authorization:
            raise HTTPException(
                status_code=401,
                detail="Se requiere autenticación"
            )

        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Formato de token inválido"
            )

        token = authorization.replace("Bearer ", "")

        try:
            user_info = verify_token(token)

        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=f"Token inválido: {str(e)}"
            )

        # =========================
        # 2. Datos usuario Firebase
        # =========================

        firebase_uid = user_info["uid"]
        user_email = user_info.get("email", "")

        # =========================
        # 3. Asegurar perfil
        # =========================

        profile = ensure_profile(
            db=db,
            firebase_uid=firebase_uid,
            email=user_email
        )

        # =========================
        # 4. Leer archivo
        # =========================

        contenido = await archivo.read()

        texto = extract_text(
            contenido,
            archivo.filename,
            modo_limpieza=modo_limpieza
        )

        if not texto.strip():
            raise HTTPException(
                status_code=400,
                detail="No se pudo extraer texto"
            )

        # =========================
        # 5. Generar preguntas IA
        # =========================

        resultado_ia = generar_preguntas_ia(texto, config)

        preguntas_ia = resultado_ia.get("preguntas", [])

        if not preguntas_ia:
            raise HTTPException(
                status_code=400,
                detail="No se generaron preguntas"
            )

        # =========================
        # 6. Crear Quiz
        # =========================

        quiz = create_quiz(
            db=db,
            creator_id=profile.id,
            title=config.get(
                "title",
                f"Quiz - {archivo.filename}"
            ),
            description=config.get("description"),
            difficulty_level=config.get("dificultad"),
            settings={
                "modo_limpieza": modo_limpieza,
                "tipo": config.get("tipo")
            }
        )

        # =========================
        # 7. Preparar preguntas
        # =========================

        preguntas_data = []

        for p in preguntas_ia:

            pregunta_data = {
                "question_type": (
                    "multiple_choice"
                    if p.get("opciones")
                    else "open_ended"
                ),

                "statement": p.get("pregunta", ""),

                "options": p.get("opciones"),

                "correct_answer": p.get(
                    "respuesta_correcta",
                    ""
                ),

                "explanation": p.get("explicacion"),

                "points": 1
            }

            preguntas_data.append(pregunta_data)

        # =========================
        # 8. Guardar preguntas
        # =========================

        preguntas_guardadas = bulk_insert_questions(
            db,
            quiz.id,
            preguntas_data
        )

        # =========================
        # 9. Respuesta
        # =========================

        return {

            "quiz_id": str(quiz.id),

            "access_code": quiz.access_code,

            "title": quiz.title,

            "description": quiz.description,

            "creator_id": profile.id,

            "firebase_uid": firebase_uid,

            "difficulty_level": quiz.difficulty_level,

            "total_questions": len(preguntas_guardadas),

            "questions": [
                {
                    "id": str(p.id),

                    "question_text": p.statement,

                    "type": p.question_type,

                    "options": p.options,

                    "correct_answer": p.correct_answer,

                    "difficulty": config.get("dificultad")
                }

                for p in preguntas_guardadas
            ]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )




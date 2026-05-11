from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
import services.profile_service as profile_service

router = APIRouter(prefix="/register", tags=["Registro"])

class RegisterRequest(BaseModel):
    email: str
    password: str  # No se guarda, se usa para Firebase
    full_name: str
    role: str
    firebase_uid: Optional[str] = None

class RegisterResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    message: str

@router.post("/", response_model=RegisterResponse)
async def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en PostgreSQL.
    El email debe ser único.
    """
    # Verificar si el email ya existe
    existing = profile_service.get_profile_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Si viene firebase_uid, verificar que no exista
    if data.firebase_uid:
        existing_firebase = profile_service.get_profile_by_firebase_uid(db, data.firebase_uid)
        if existing_firebase:
            raise HTTPException(status_code=400, detail="El usuario de Firebase ya está registrado")

    # Crear el perfil
    profile = profile_service.create_profile(
        db=db,
        email=data.email,
        full_name=data.full_name,
        role=data.role,
        firebase_uid=data.firebase_uid
    )

    return RegisterResponse(
        id=profile.id,
        email=profile.email,
        full_name=profile.full_name,
        role=profile.role,
        message="Usuario registrado correctamente"
    )

@router.get("/{profile_id}")
async def get_profile(profile_id: int, db: Session = Depends(get_db)):
    """Obtiene un perfil por ID"""
    profile = profile_service.get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    return {
        "id": profile.id,
        "firebase_uid": profile.firebase_uid,
        "email": profile.email,
        "full_name": profile.full_name,
        "role": profile.role,
        "created_at": profile.created_at.isoformat()
    }

@router.get("/firebase/{firebase_uid}")
async def get_profile_by_firebase(firebase_uid: str, db: Session = Depends(get_db)):
    """Obtiene un perfil por Firebase UID"""
    profile = profile_service.get_profile_by_firebase_uid(db, firebase_uid)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    return {
        "id": profile.id,
        "firebase_uid": profile.firebase_uid,
        "email": profile.email,
        "full_name": profile.full_name,
        "role": profile.role,
        "created_at": profile.created_at.isoformat()
    }

class FirebaseLoginRequest(BaseModel):
    firebase_token: str
    email: str

@router.post("/firebase/login")
async def firebase_login(data: FirebaseLoginRequest, db: Session = Depends(get_db)):
    """
    Valida el token de Firebase y crea/busca el perfil en PostgreSQL.
    Uso: El frontend envía el token de Firebase y el backend valida y retorna el perfil.
    """
    # Validar token con Firebase Admin SDK
    from services.firebase_service import verify_token

    try:
        firebase_user = verify_token(data.firebase_token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")

    # Verificar que el email del token coincida con el enviado
    if firebase_user.get("email") != data.email:
        raise HTTPException(status_code=401, detail="El email del token no coincide")

    firebase_uid = firebase_user.get("uid")

    # Buscar perfil existente
    profile = profile_service.get_profile_by_firebase_uid(db, firebase_uid)

    if not profile:
        # Crear nuevo perfil si no existe
        profile = profile_service.create_profile(
            db=db,
            email=data.email,
            full_name=firebase_user.get("name", data.email.split("@")[0]),
            role="estudiante",  # Rol por defecto
            firebase_uid=firebase_uid
        )

    return {
        "id": profile.id,
        "firebase_uid": profile.firebase_uid,
        "email": profile.email,
        "full_name": profile.full_name,
        "role": profile.role,
        "created_at": profile.created_at.isoformat()
    }
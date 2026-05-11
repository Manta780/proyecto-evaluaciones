from sqlalchemy.orm import Session
from models import Profile
from typing import Optional

def create_profile(db: Session, email: str, full_name: str, role: str, firebase_uid: str = None) -> Profile:
    """Crea un nuevo perfil de usuario"""
    profile = Profile(
        email=email,
        full_name=full_name,
        role=role,
        firebase_uid=firebase_uid
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def get_profile_by_id(db: Session, profile_id: int) -> Optional[Profile]:
    """Obtiene un perfil por ID"""
    return db.query(Profile).filter(Profile.id == profile_id).first()

def get_profile_by_email(db: Session, email: str) -> Optional[Profile]:
    """Obtiene un perfil por email"""
    return db.query(Profile).filter(Profile.email == email).first()

def get_profile_by_firebase_uid(db: Session, firebase_uid: str) -> Optional[Profile]:
    """Obtiene un perfil por Firebase UID"""
    return db.query(Profile).filter(Profile.firebase_uid == firebase_uid).first()

def update_profile(db: Session, profile_id: int, **kwargs) -> Optional[Profile]:
    """Actualiza un perfil"""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        return None

    allowed_fields = ['full_name', 'role', 'firebase_uid']
    for field in allowed_fields:
        if field in kwargs and kwargs[field] is not None:
            setattr(profile, field, kwargs[field])

    db.commit()
    db.refresh(profile)
    return profile
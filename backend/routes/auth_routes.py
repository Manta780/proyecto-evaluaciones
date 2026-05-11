from fastapi import APIRouter, Header, HTTPException
from services.firebase_service import verify_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/verify")
async def verify_firebase_token(authorization: str = Header(None)):
    """
    Verifica un token de Firebase y retorna la información del usuario.
    Envía el token en el header: Authorization: Bearer <token>
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato de token inválido. Usa: Bearer <token>")

    token = authorization.replace("Bearer ", "")
    user_info = verify_token(token)

    return {
        "success": True,
        "user": user_info
    }

@router.get("/test-user/{uid}")
async def get_test_user(uid: str):
    """
    Endpoint de prueba - retorna información de un usuario por UID
    """
    return {
        "uid": uid,
        "email": f"user_{uid[:8]}@example.com",
        "name": f"Usuario Prueba {uid[:8]}"
    }
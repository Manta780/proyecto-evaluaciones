import os
from functools import wraps
from fastapi import HTTPException, Request, Depends

try:
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import auth
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("Advertencia: firebase_admin no disponible. Usando modo de prueba.")

# Ruta al archivo de credenciales
FIREBASE_CRED_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "..", "quizesai-dcb20-firebase-adminsdk-fbsvc-ed1f0333de.json"
)

_firebase_initialized = False

def initialize_firebase():
    """Inicializa Firebase Admin SDK una sola vez"""
    global _firebase_initialized
    if _firebase_initialized:
        return True

    if not FIREBASE_AVAILABLE:
        return False

    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(FIREBASE_CRED_PATH)
            firebase_admin.initialize_app(cred)
            _firebase_initialized = True
            print("Firebase Admin SDK inicializado correctamente")
            return True
        except Exception as e:
            print(f"Error inicializando Firebase: {e}")
            return False
    _firebase_initialized = True
    return True

def verify_token(token: str) -> dict:
    """Verifica un token de Firebase y retorna la info del usuario"""
    if not FIREBASE_AVAILABLE or not initialize_firebase():
        raise HTTPException(status_code=500, detail="Firebase no está disponible")

    try:
        decoded_token = auth.verify_id_token(token)
        return {
            "uid": decoded_token["uid"],
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name"),
        }
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except auth.ExpiredTokenError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error verificando token: {str(e)}")

def get_current_user(request: Request):
    """Dependencia FastAPI para obtener el usuario actual desde el token"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    token = auth_header.replace("Bearer ", "")
    return verify_token(token)
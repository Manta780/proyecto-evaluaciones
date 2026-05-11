from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import pdf_routes, quiz_routes, quiz_CRUD_routes, auth_routes, register_routes
from database import create_tables
import models

app = FastAPI(title="API Generador de Quizzes IA")

# Configuración CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas al iniciar
create_tables()

app.include_router(auth_routes.router)
app.include_router(register_routes.router)
app.include_router(pdf_routes.router)
app.include_router(quiz_routes.router)
app.include_router(quiz_CRUD_routes.router)

@app.get("/")
def root():
    return {"mensaje": "API funcionando"}


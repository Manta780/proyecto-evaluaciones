from fastapi import FastAPI
from routes import pdf_routes, quiz_routes

app = FastAPI(title="API Generador de Quizzes IA")

app.include_router(pdf_routes.router)
app.include_router(quiz_routes.router)

@app.get("/")
def root():
    return {"mensaje": "API funcionando 🚀"}
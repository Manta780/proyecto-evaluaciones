# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI backend for an AI-powered Quiz Generator. It accepts documents (PDF, DOCX, PPTX, images) and generates quizzes using Groq's Llama model. Supports user authentication via Firebase and stores quizzes in PostgreSQL (Neon).

## Commands

```bash
# Install dependencies (from backend directory)
pip install fastapi uvicorn python-dotenv groq pymupdf python-docx python-pptx pytesseract pillow opencv-python sqlalchemy psycopg2-binary firebase-admin

# Run the server (development)
uvicorn main:app --reload

# Run in production
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Architecture

```
main.py → FastAPI app, includes routers from routes/
routes/ → API endpoints
controllers/ → Request handlers, orchestrate services
services/
  ├── pdf_service.py       → Extracts text from PDF/DOCX/PPTX
  ├── ocr_service.py       → OCR for images and scanned PDFs (uses Tesseract)
  ├── ia_service.py        → Groq API integration for quiz generation
  ├── ia_cleaner_service.py → Cleans AI responses
  ├── quiz_service.py      → CRUD operations for quizzes and questions
  ├── profile_service.py   → CRUD operations for user profiles
  └── firebase_service.py  → Firebase token verification
database.py    → SQLAlchemy connection to PostgreSQL
models.py      → SQLAlchemy models (Profile, Quiz, Question, Attempt, StudentResponse)
Config.py      → Environment variables
```

## Environment Variables (.env)

```
GROQ_API_KEY="..."
DATABASE_URL="postgresql://neondb_owner:...@ep-...neon.tech/neondb?sslmode=require&channel_binding=require"
```

## API Endpoints

### Authentication
- `POST /auth/verify` - Verify Firebase token
- `GET /auth/test-user/{uid}` - Test endpoint for user info

### Registration
- `POST /register/` - Register new user in PostgreSQL
- `GET /register/{profile_id}` - Get profile by ID
- `GET /register/firebase/{firebase_uid}` - Get profile by Firebase UID
- `POST /register/firebase/login` - Login with Firebase token (creates/updates profile)

### Quiz Generation
- `POST /quiz/generar` - Generate quiz with AI (requires Firebase token)

### Quiz CRUD
- `GET /quiz/obtener_quiz/{quiz_id}` - Get quiz by ID
- `GET /quiz/code/{access_code}` - Get quiz by access code
- `GET /quiz/creator/{creator_id}` - List all quizzes by creator
- `GET /quiz/search/{title}?creator_id={id}` - Search quizzes by title
- `PUT /quiz/actualizar_quiz/{quiz_id}` - Update quiz
- `DELETE /quiz/eliminar_quiz/{quiz_id}` - Delete (deactivate) quiz

### Questions CRUD
- `POST /quiz/question/agregar_pregunta` - Add question to quiz
- `PUT /quiz/question/actualizar_pregunta/{question_id}` - Update question
- `DELETE /quiz/question/eliminar_pregunta/{question_id}` - Delete question

### PDF
- `POST /pdf/extraer` - Extract text from document

## Authentication

All endpoints that require authentication must include the Firebase token in the `Authorization` header:
```
Authorization: Bearer <firebase_token>
```

The `firebase_service.py` provides:
- `verify_token(token)` - Verifies Firebase token, returns `{uid, email, name}`
- `get_current_user(request)` - FastAPI dependency for authentication

## Database (Neon PostgreSQL)

Tables (created via SQLAlchemy):
- `profiles` - User profiles (Firebase UID as unique field)
- `quizzes` - Quiz metadata with access_code (6-digit unique code)
- `questions` - Quiz questions (linked to quizzes)
- `attempts` - Student quiz attempts
- `student_responses` - Individual student answers

## Technical Notes

- Text extraction falls back to OCR when PDF has no extractable text
- Quiz generation uses Bloom's Taxonomy for difficulty levels
- The IA service uses `llama-3.3-70b-versatile` model with temperature 0.6
- Access codes are 6-digit numbers, generated uniquely (no duplicates in DB)
- Bulk insert is used when saving questions from IA response
- Quiz deletion is a soft delete (sets is_active = false)

## Requirements

- **Tesseract OCR**: Must be installed on the system. On Windows: https://github.com/UB-Mannheim/tesseract/wiki
- **GROQ_API_KEY**: Required in `.env` for AI features
- **DATABASE_URL**: PostgreSQL connection string (Neon)
- **Firebase credentials**: `quizesai-dcb20-firebase-adminsdk-fbsvc-ed1f0333de.json` in project root
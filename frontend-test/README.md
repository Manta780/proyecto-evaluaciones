# Frontend de Prueba - QuizAI

Este es un frontend de prueba para la plataforma de generación de quizzes con IA.

## Archivos

- `index.html` - Página principal con toda la interfaz
- `styles.css` - Estilos personalizados
- `app.js` - Lógica de la aplicación (auth, logging, quizzes)

## Cómo usar

### 1. Iniciar el backend

```bash
cd backend
uvicorn main:app --reload
```

### 2. Abrir el frontend

Abre el archivo `index.html` en tu navegador:

- Puedes usar la extensión "Live Server" de VS Code
- O simplemente arrastrar el archivo al navegador

### 3. Funcionalidades

#### Sistema de Logging
- Haz clic en el botón 📋 en la esquina inferior derecha para ver los logs
- Muestra todas las acciones y errores con timestamps

#### Registro
- Ingresa correo electrónico
- Ingresa contraseña
- Selecciona el rol: **Estudiante** o **Docente**

#### Login
- Ingresa tus credenciales para acceder

#### Panel de Docente
- **Subir documento**: PDF, DOCX, PPTX, PNG, JPG
- **Título del quiz**: Nombre del quiz
- **Descripción**: Cómo quieres el quiz (temática, enfoque, etc.)
- **Cantidad de preguntas**: Entre 1 y 50
- **Dificultad**: Recordación, Comprensión, Aplicación, Análisis, Evaluación
- **Tipo de preguntas**: Opción múltiple, Verdadero/Falso, Respuesta corta
- **Modo de limpieza IA**: Básica o Completa

#### Panel de Estudiante
- Ingresa el código de 6 dígitos del quiz

## Notas

- Este es un frontend de **prueba** - la autenticación es simulada
- Para producción, conecta con Firebase Authentication real
- El backend debe estar corriendo en `http://localhost:8000`
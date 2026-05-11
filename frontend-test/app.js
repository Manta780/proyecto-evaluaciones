// ============================================
// FRONTEND TEST - QuizAI
// ============================================

// API Configuration
const API_URL = 'http://localhost:8000';

// ============================================
// LOGGER SYSTEM
// ============================================
const Logger = {
    logs: [],
    visible: false,

    log(level, message, data = null) {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = { level, message, data, timestamp };
        this.logs.push(logEntry);

        const loggerContent = document.getElementById('logger-content');
        if (loggerContent) {
            const logLine = document.createElement('div');
            logLine.className = 'mb-1';
            logLine.innerHTML = `<span class="text-gray-500">[${timestamp}]</span> <span class="${this.getLevelColor(level)}">[${level.toUpperCase()}]</span> ${message}${data ? ' ' + JSON.stringify(data) : ''}`;
            loggerContent.appendChild(logLine);
            loggerContent.scrollTop = loggerContent.scrollHeight;
        }

        console.log(`[${level.toUpperCase()}]`, message, data);
    },

    getLevelColor(level) {
        const colors = {
            info: 'text-blue-400',
            success: 'text-green-400',
            warning: 'text-yellow-400',
            error: 'text-red-400'
        };
        return colors[level] || 'text-gray-400';
    },

    info(message, data) { this.log('info', message, data); },
    success(message, data) { this.log('success', message, data); },
    warning(message, data) { this.log('warning', message, data); },
    error(message, data) { this.log('error', message, data); }
};

function toggleLogger() {
    const panel = document.getElementById('logger-panel');
    const toggle = document.getElementById('logger-toggle');
    Logger.visible = !Logger.visible;

    if (Logger.visible) {
        panel.classList.remove('hidden');
        toggle.classList.add('hidden');
    } else {
        panel.classList.add('hidden');
        toggle.classList.remove('hidden');
    }
}

// Show logger toggle after first log
setTimeout(() => {
    if (Logger.logs.length > 0) {
        document.getElementById('logger-toggle').classList.remove('hidden');
    }
}, 1000);

Logger.info('Frontend cargado correctamente');

// ============================================
// AUTH STATE
// ============================================
let currentUser = null;

// ============================================
// UI NAVIGATION
// ============================================
function showLogin() {
    document.getElementById('login-form').classList.remove('hidden');
    document.getElementById('register-form').classList.add('hidden');
    Logger.info('Mostrando formulario de login');
}

function showRegister() {
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('register-form').classList.remove('hidden');
    Logger.info('Mostrando formulario de registro');
}

function showDashboard(role) {
    document.getElementById('auth-container').classList.add('hidden');
    document.getElementById('navbar').classList.add('hidden');

    if (role === 'Docente') {
        document.getElementById('teacher-dashboard').classList.remove('hidden');
        Logger.success('Dashboard de Docente cargado');
    } else {
        document.getElementById('student-dashboard').classList.remove('hidden');
        Logger.success('Dashboard de estudiante cargado');
    }
}

function logout() {
    currentUser = null;
    document.getElementById('teacher-dashboard').classList.add('hidden');
    document.getElementById('student-dashboard').classList.add('hidden');
    document.getElementById('auth-container').classList.remove('hidden');
    document.getElementById('navbar').classList.remove('hidden');

    // Reset forms
    document.getElementById('login-form').reset();
    document.getElementById('register-form').reset();

    // Reset results
    document.getElementById('quiz-result').classList.add('hidden');

    // Logout from Firebase
    logoutFromFirebase();

    // Update nav links
    updateNavLinks();

    Logger.info('Usuario cerró sesión');
}

function updateNavLinks() {
    const navLinks = document.getElementById('nav-links');
    if (currentUser) {
        const displayName = currentUser.full_name || currentUser.email;
        navLinks.innerHTML = `
            <span class="mr-4">${displayName} (${currentUser.role})</span>
            <button onclick="logout()" class="hover:underline">Cerrar Sesión</button>
        `;
    } else {
        navLinks.innerHTML = `
            <button onclick="showLogin()" class="mr-4 hover:underline">Iniciar Sesión</button>
            <button onclick="showRegister()" class="hover:underline">Registrarse</button>
        `;
    }
}

// ============================================
// AUTH HANDLERS
// ============================================
async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    Logger.info('Intentando iniciar sesión', { email });

    try {
        const result = await loginWithFirebase(email, password);

        currentUser = result.user;
        updateNavLinks();
        showDashboard(result.user.role);

        Logger.success('Login exitoso', { email, role: result.user.role });
        alert(`¡Bienvenido${result.user.full_name ? ' ' + result.user.full_name : ''}! Has iniciado sesión como ${result.user.role}`);
    } catch (error) {
        Logger.error('Error en login', error);
        alert('Error al iniciar sesión: ' + error.message);
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const role = document.getElementById('register-role').value;

    Logger.info('Intentando registrar usuario', { email, name, role });

    try {
        const result = await registerWithFirebase(email, password, name, role);

        currentUser = result.user;
        updateNavLinks();
        showDashboard(result.user.role);

        Logger.success('Registro exitoso', { email, name, role: result.user.role });
        alert(`¡Cuenta creada! Has registrado como ${result.user.role}`);
    } catch (error) {
        Logger.error('Error en registro', error);
        alert('Error al registrar: ' + error.message);
    }
}

// ============================================
// STUDENT FUNCTIONS
// ============================================
async function accessQuiz() {
    const code = document.getElementById('quiz-code-input').value;

    if (code.length !== 6 || !/^\d+$/.test(code)) {
        alert('Por favor ingresa un código válido de 6 dígitos');
        Logger.warning('Código de quiz inválido', { code });
        return;
    }

    Logger.info('Accediendo al quiz', { code });

    try {
        const response = await fetch(`${API_URL}/quiz/code/${code}`);
        if (!response.ok) {
            throw new Error('Quiz no encontrado');
        }

        const quiz = await response.json();
        Logger.success('Quiz encontrado', quiz);
        alert(`Quiz encontrado: ${quiz.title}`);
        // Here you would show the quiz questions
    } catch (error) {
        Logger.error('Error al acceder quiz', error);
        alert('Quiz no encontrado con ese código');
    }
}

// ============================================
// TEACHER FUNCTIONS
// ============================================
async function handleCreateQuiz(event) {
    event.preventDefault();

    const title = document.getElementById('quiz-title').value;
    const description = document.getElementById('quiz-description').value;
    const fileInput = document.getElementById('quiz-file');
    const cantidad = parseInt(document.getElementById('quiz-amount').value);
    const dificultad = document.getElementById('quiz-difficulty').value;
    const tipo = document.getElementById('quiz-type').value;
    const modoLimpieza = document.getElementById('quiz-cleaning-mode').value;

    if (!fileInput.files[0]) {
        alert('Por favor selecciona un archivo');
        return;
    }

    const file = fileInput.files[0];

    Logger.info('Creando quiz', { title, cantidad, dificultad, tipo });
    Logger.info('Archivo seleccionado', { name: file.name, size: file.size, type: file.type });
    Logger.info('Conectando a API:', API_URL);

    // Show loading
    document.getElementById('teacher-dashboard').querySelector('form').classList.add('hidden');
    document.getElementById('quiz-loading').classList.remove('hidden');

    try {
        const formData = new FormData();
        formData.append('archivo', file);
        formData.append('cantidad', cantidad);
        formData.append('dificultad', dificultad);
        formData.append('tipo', tipo);
        formData.append('modo_limpieza', modoLimpieza);
        formData.append('title', title);
        formData.append('description', description);

        // Obtener token de Firebase
        const token = localStorage.getItem('firebaseToken');

        Logger.info('Enviando solicitud al servidor...');

        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/quiz/generar`, {
            method: 'POST',
            headers: headers,
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `Error del servidor: ${response.status}`);
        }

        const result = await response.json();
        Logger.success('Quiz generado exitosamente', result);

        // Hide loading and show result
        document.getElementById('quiz-loading').classList.add('hidden');
        displayQuizResult(result);

    } catch (error) {
        Logger.error('Error al crear quiz', { message: error.message, type: error.type });
        document.getElementById('quiz-loading').classList.add('hidden');
        document.getElementById('teacher-dashboard').querySelector('form').classList.remove('hidden');

        // Mensaje más detallado según el tipo de error
        let errorMsg = 'Error al crear quiz: ' + error.message;
        if (error.message === 'Failed to fetch') {
            errorMsg = 'No se puede conectar al servidor. ¿Está el backend corriendo en puerto 8000?';
        }
        alert(errorMsg);
    }
}

function displayQuizResult(result) {
    Logger.info('Mostrando resultado del quiz');

    document.getElementById('quiz-result').classList.remove('hidden');

    // Set quiz info
    document.getElementById('result-title').textContent = result.title || 'Quiz sin título';
    document.getElementById('result-description').textContent = result.description || '';
    document.getElementById('quiz-access-code').textContent = result.access_code || 'N/A';

    // Render questions
    const container = document.getElementById('questions-container');
    container.innerHTML = '';

    if (result.questions && result.questions.length > 0) {
        result.questions.forEach((question, index) => {
            const questionCard = document.createElement('div');
            questionCard.className = 'question-card bg-gray-50 rounded-lg p-4';

            let optionsHTML = '';
            if (question.options && question.options.length > 0) {
                optionsHTML = `
                    <div class="mt-3 space-y-2">
                        ${question.options.map((option, optIndex) => `
                            <div class="option-item flex items-center p-2 rounded ${option === question.correct_answer ? 'bg-green-100 border-green-300' : 'bg-white border'} border">
                                <span class="font-medium mr-2">${String.fromCharCode(65 + optIndex)}.</span>
                                <span>${option}</span>
                                ${option === question.correct_answer ? ' <span class="ml-2 text-green-600 text-sm font-bold">✓ Correcta</span>' : ''}
                            </div>
                        `).join('')}
                    </div>
                `;
            }

            questionCard.innerHTML = `
                <h4 class="text-lg font-semibold text-gray-800">Pregunta ${index + 1}</h4>
                <p class="text-gray-700 mt-2">${question.question_text || question.pregunta || 'Sin texto'}</p>
                ${question.type ? `<span class="inline-block bg-indigo-100 text-indigo-700 text-xs px-2 py-1 rounded mt-2">${question.type}</span>` : ''}
                ${question.difficulty ? `<span class="inline-block bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded mt-2 ml-2">${question.difficulty}</span>` : ''}
                ${optionsHTML}
            `;

            container.appendChild(questionCard);
        });
    } else {
        container.innerHTML = '<p class="text-gray-500">No se pudieron generar preguntas</p>';
    }

    Logger.success('Quiz mostrado en pantalla');
}

function copyQuizCode() {
    const code = document.getElementById('quiz-access-code').textContent;
    navigator.clipboard.writeText(code).then(() => {
        alert('Código copiado al portapapeles');
        Logger.info('Código copiado', { code });
    }).catch(err => {
        Logger.error('Error al copiar código', err);
    });
}

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    Logger.info('DOM cargado, inicializando...');
    updateNavLinks();
});

Logger.info('Script de app.js cargado');
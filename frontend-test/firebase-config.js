// ============================================
// Firebase Configuration - QuizAI
// ============================================

// Configuración de Firebase (reemplaza con tus datos de Firebase Console)
const firebaseConfig = {
    apiKey: "AIzaSyBkm4KN0GKA_Zlc2vPIB1t6JPpUPy2YqJE",
    authDomain: "quizesai.firebaseapp.com",
    projectId: "quizesai",
    storageBucket: "quizesai.appspot.com",
    messagingSenderId: "852386466835",
    appId: "1:852386466835:web:b4f0322245075e2e4ac3e6"
};

// Inicializar Firebase
let auth;
let db;

function initializeFirebase() {
    return new Promise((resolve, reject) => {
        if (typeof firebase !== 'undefined') {
            firebase.initializeApp(firebaseConfig);
            auth = firebase.auth();
            db = firebase.firestore();
            console.log('Firebase inicializado correctamente');
            resolve();
        } else {
            // Firebase SDK no disponible, usar modo simulado
            console.warn('Firebase SDK no disponible, usando modo simulado');
            resolve();
        }
    });
}

// ============================================
// Auth Functions
// ============================================

async function registerWithFirebase(email, password, fullName, role) {
    if (typeof firebase === 'undefined') {
        // Modo simulado
        return simulateRegister(email, fullName, role);
    }

    try {
        // Crear usuario en Firebase Auth
        const userCredential = await auth.createUserWithEmailAndPassword(email, password);
        const firebaseUid = userCredential.user.uid;

        // Registrar en PostgreSQL
        const response = await fetch(`${API_URL}/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password,  // Se usa para Firebase, no se guarda
                full_name: fullName,
                role: role,
                firebase_uid: firebaseUid
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al registrar en PostgreSQL');
        }

        const profile = await response.json();

        // Guardar token para sesiones futuras
        const token = await userCredential.user.getIdToken();
        localStorage.setItem('firebaseToken', token);
        localStorage.setItem('userProfile', JSON.stringify(profile));

        return {
            success: true,
            user: {
                ...profile,
                firebaseUid: firebaseUid,
                token: token
            }
        };
    } catch (error) {
        console.error('Error en registro:', error);
        throw error;
    }
}

async function loginWithFirebase(email, password) {
    if (typeof firebase === 'undefined') {
        // Modo simulado
        return simulateLogin(email);
    }

    try {
        // Iniciar sesión en Firebase
        const userCredential = await auth.signInWithEmailAndPassword(email, password);
        const firebaseUid = userCredential.user.uid;
        const token = await userCredential.user.getIdToken();

        // Obtener perfil de PostgreSQL usando firebase_uid
        const response = await fetch(`${API_URL}/register/firebase/${firebaseUid}`);

        if (!response.ok) {
            // Si no existe en PostgreSQL, crear perfil
            const newProfile = await createProfileFromFirebase(email, firebaseUid);
            localStorage.setItem('firebaseToken', token);
            localStorage.setItem('userProfile', JSON.stringify(newProfile));
            return {
                success: true,
                user: {
                    ...newProfile,
                    firebaseUid: firebaseUid,
                    token: token
                }
            };
        }

        const profile = await response.json();

        localStorage.setItem('firebaseToken', token);
        localStorage.setItem('userProfile', JSON.stringify(profile));

        return {
            success: true,
            user: {
                ...profile,
                firebaseUid: firebaseUid,
                token: token
            }
        };
    } catch (error) {
        console.error('Error en login:', error);
        throw error;
    }
}

async function createProfileFromFirebase(email, firebaseUid) {
    const response = await fetch(`${API_URL}/register/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: 'N/A',  // No se guarda
            full_name: email.split('@')[0],  // Nombre por defecto
            role: 'estudiante',
            firebase_uid: firebaseUid
        })
    });

    if (!response.ok) {
        throw new Error('Error al crear perfil');
    }

    return await response.json();
}

function logoutFromFirebase() {
    if (typeof firebase !== 'undefined' && auth) {
        auth.signOut();
    }
    localStorage.removeItem('firebaseToken');
    localStorage.removeItem('userProfile');
}

function getStoredUser() {
    const profile = localStorage.getItem('userProfile');
    return profile ? JSON.parse(profile) : null;
}

// ============================================
// Modo Simulado (sin Firebase)
// ============================================

async function simulateRegister(email, fullName, role) {
    const response = await fetch(`${API_URL}/register/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: 'simulated',
            full_name: fullName,
            role: role,
            firebase_uid: null
        })
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al registrar');
    }

    const profile = await response.json();
    localStorage.setItem('userProfile', JSON.stringify(profile));

    return {
        success: true,
        user: profile
    };
}

async function simulateLogin(email) {
    // Buscar usuario por email
    const response = await fetch(`${API_URL}/register/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: 'simulated',
            full_name: email.split('@')[0],
            role: email.includes('Docente') ? 'Docente' : 'Estudiante',
            firebase_uid: null
        })
    });

    if (!response.ok) {
        throw new Error('Usuario no encontrado');
    }

    const profile = await response.json();
    localStorage.setItem('userProfile', JSON.stringify(profile));

    return {
        success: true,
        user: profile
    };
}

// Inicializar Firebase al cargar
initializeFirebase();
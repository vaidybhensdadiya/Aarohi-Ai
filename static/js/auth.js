/**
 * Auth.js - Login, Register, Token handling for Aarohi AI
 * Saves JWT in localStorage, redirects unauthenticated users
 */

const API_BASE = '';

function getToken() {
    return localStorage.getItem('aarohi_token');
}

function saveAuth(token, user) {
    localStorage.setItem('aarohi_token', token);
    localStorage.setItem('aarohi_user', JSON.stringify(user));
}

function clearAuth() {
    localStorage.removeItem('aarohi_token');
    localStorage.removeItem('aarohi_user');
}

function requireAuth() {
    if (!getToken()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

function loadUserInfo() {
    const userStr = localStorage.getItem('aarohi_user');
    if (userStr) {
        try {
            const user = JSON.parse(userStr);
            const el = document.getElementById('userName');
            if (el) el.textContent = user.name || user.email_id || 'User';
        } catch (e) {}
    }
}

function handleLogout(e) {
    e.preventDefault();
    clearAuth();
    window.location.href = '/login';
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email_id').value.trim();
    const password = document.getElementById('password').value;
    const errEl = document.getElementById('loginError');

    if (!email || !password) {
        errEl.textContent = 'Email and password are required';
        errEl.style.display = 'block';
        return;
    }

    try {
        const res = await fetch(API_BASE + '/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email_id: email, password })
        });
        const data = await res.json();

        if (!res.ok) {
            errEl.textContent = data.error || 'Login failed';
            errEl.style.display = 'block';
            return;
        }

        saveAuth(data.token, data.user);
        window.location.href = '/dashboard';
    } catch (err) {
        errEl.textContent = 'Network error. Please try again.';
        errEl.style.display = 'block';
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email_id').value.trim();
    const age = parseInt(document.getElementById('age').value, 10);
    const password = document.getElementById('password').value;
    const errEl = document.getElementById('registerError');

    if (!name || !email || !age || !password) {
        errEl.textContent = 'All fields are required';
        errEl.style.display = 'block';
        return;
    }
    if (password.length < 6) {
        errEl.textContent = 'Password must be at least 6 characters';
        errEl.style.display = 'block';
        return;
    }

    try {
        const res = await fetch(API_BASE + '/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email_id: email, age, password })
        });
        const data = await res.json();

        if (!res.ok) {
            errEl.textContent = data.error || 'Registration failed';
            errEl.style.display = 'block';
            return;
        }

        saveAuth(data.token, data.user);
        window.location.href = '/dashboard';
    } catch (err) {
        errEl.textContent = 'Network error. Please try again.';
        errEl.style.display = 'block';
    }
}

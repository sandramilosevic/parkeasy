const BASE_URL = 'http://127.0.0.1:8000/api';

// --- Token helpers ---

function getToken() {
    return localStorage.getItem('access_token');
}

function setTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
}

function removeTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}

function isLoggedIn() {
    return !!getToken();
}

// --- Base fetch with auth header ---

async function apiFetch(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (getToken()) {
        headers['Authorization'] = `Bearer ${getToken()}`;
    }

    const response = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers
    });

    // If 401, try to refresh token
    if (response.status === 401) {
        const refreshed = await tryRefreshToken();
        if (refreshed) {
            headers['Authorization'] = `Bearer ${getToken()}`;
            return fetch(`${BASE_URL}${endpoint}`, { ...options, headers });
        } else {
            removeTokens();
            window.location.href = 'index.html';
        }
    }

    return response;
}

async function tryRefreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) return false;

    const response = await fetch(`${BASE_URL}/auth/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        return true;
    }

    return false;
}

// --- Auth ---
// POST /api/auth/token/  { username, password } → { access, refresh }
async function apiLogin(username, password) {
    return fetch(`${BASE_URL}/auth/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
}

// POST /api/auth/users/  { username, email, password, user_type, phone_number }
async function apiRegister(data) {
    return apiFetch('/auth/users/', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

// GET /api/auth/users/{id}/  — current user (we get ID from token decode or list)
// GET /api/auth/users/  — list (admin only), for regular users returns only their own
async function apiGetCurrentUser() {
    return apiFetch('/auth/users/');
}

// --- Parkings ---
// GET /api/parkings/?city=&parking_type=&distance=&ordering=&page=
async function apiGetParkings(params = {}) {
    const query = new URLSearchParams(params).toString();
    return apiFetch(`/parkings/?${query}`);
}

// GET /api/parkings/{id}/
async function apiGetParking(id) {
    return apiFetch(`/parkings/${id}/`);
}

// POST /api/parkings/  (owner only)
async function apiCreateParking(data) {
    return apiFetch('/parkings/', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

// PATCH /api/parkings/{id}/  (owner only)
async function apiUpdateParking(id, data) {
    return apiFetch(`/parkings/${id}/`, {
        method: 'PATCH',
        body: JSON.stringify(data)
    });
}

// DELETE /api/parkings/{id}/  (owner only)
async function apiDeleteParking(id) {
    return apiFetch(`/parkings/${id}/`, {
        method: 'DELETE'
    });
}

// --- Reservations ---
// GET /api/reservations/  (returns only current user's reservations)
async function apiGetReservations() {
    return apiFetch('/reservations/');
}

// POST /api/reservations/  (driver only) { parking_reservation, date_start, date_end, period_type }
// full_price, reservation_user, reservation_status are set automatically by backend
async function apiCreateReservation(data) {
    return apiFetch('/reservations/', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

// DELETE /api/reservations/{id}/  (owner of reservation only)
async function apiDeleteReservation(id) {
    return apiFetch(`/reservations/${id}/`, {
        method: 'DELETE'
    });
}
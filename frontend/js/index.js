let currentPage = 1;
let nextPage = null;
let prevPage = null;

// --- On page load ---

document.addEventListener('DOMContentLoaded', () => {
    renderNavButtons();
    loadParkings();
    loadCities();
});

// --- Navbar ---

function renderNavButtons() {
    const nav = document.getElementById('nav-buttons');

    if (isLoggedIn()) {
        // Show logged in user options
        nav.innerHTML = `
            <a href="dashboard.html" class="btn btn-outline">My Parking</a>
            <button class="btn btn-primary" onclick="logout()">Logout</button>
        `;
    } else {
        // Show login and register buttons
        nav.innerHTML = `
            <button class="btn btn-outline" onclick="openModal('modal-login')">Login</button>
            <button class="btn btn-primary" onclick="openModal('modal-register')">Register</button>
        `;
    }
}

function logout() {
    removeTokens();
    window.location.reload();
}

// --- Modal helpers ---

function openModal(id) {
    document.getElementById(id).classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}

// --- Login ---

async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const errorEl = document.getElementById('login-error');

    const response = await apiLogin(username, password);
    const data = await response.json();

    if (response.ok) {
        // Save tokens and reload page
        setTokens(data.access, data.refresh);
        closeModal('modal-login');
        window.location.reload();
    } else {
        // Show error message
        errorEl.style.display = 'block';
        errorEl.textContent = 'Invalid username or password.';
    }
}

// --- Register ---

async function register() {
    const errorEl = document.getElementById('register-error');

    const data = {
        username: document.getElementById('register-username').value,
        email: document.getElementById('register-email').value,
        phone_number: document.getElementById('register-phone').value,
        password: document.getElementById('register-password').value,
        user_type: document.getElementById('register-type').value,
    };

    const response = await apiRegister(data);
    const result = await response.json();

    if (response.ok) {
        // Close register modal and open login
        closeModal('modal-register');
        openModal('modal-login');
    } else {
        // Show error message
        errorEl.style.display = 'block';
        errorEl.textContent = JSON.stringify(result.message || result);
    }
}

// --- Load Parkings ---

async function loadParkings(params = {}) {
    params.page = currentPage;

    const response = await apiGetParkings(params);
    const data = await response.json();

    // Update pagination state
    nextPage = data.next;
    prevPage = data.previous;

    document.getElementById('btn-next').style.display = nextPage ? 'block' : 'none';
    document.getElementById('btn-prev').style.display = prevPage ? 'block' : 'none';

    renderParkings(data.results);
}

function renderParkings(parkings) {
    const list = document.getElementById('parking-list');

    if (!parkings || parkings.length === 0) {
        list.innerHTML = '<p style="color: var(--text-light)">No parking spots found.</p>';
        return;
    }

    list.innerHTML = parkings.map(p => `
        <div class="card">
            <div class="card-image">
                ${p.image ? `<img src="${p.image}" style="width:100%;height:100%;object-fit:cover;border-radius:8px">` : 'No image'}
            </div>
            ${p.featured ? '<span class="badge">⭐ Featured</span>' : ''}
            <h3>${p.title}</h3>
            <div class="price">$${p.price_per_hour} <span style="font-weight:400;font-size:13px;color:var(--text-light)">/hour</span></div>
            <div class="meta">${p.parking_type} · ${p.distance} · ${p.city}</div>
            <div class="meta" style="margin-top:4px">${p.address}</div>
            <button class="btn btn-primary" style="width:100%;margin-top:14px" onclick="openReserve(${p.id})">Reserve</button>
        </div>
    `).join('');
}

// --- Load Cities for dropdown ---

async function loadCities() {
    const allCities = new Set();
    let url = '/parkings/';

    // Fetch all pages to collect all cities
    while (url) {
        const response = await apiFetch(url);
        const data = await response.json();

        data.results.forEach(p => allCities.add(p.city));

        // Extract relative path from next URL if it exists
        if (data.next) {
            const nextUrl = new URL(data.next);
            url = nextUrl.pathname.replace('/api', '') + nextUrl.search;
        } else {
            url = null;
        }
    }

    const select = document.getElementById('search-city');
    allCities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        select.appendChild(option);
    });
}

// --- Search ---

function searchParkings() {
    currentPage = 1;
    const params = {};

    const city = document.getElementById('search-city').value;
    const type = document.getElementById('search-type').value;
    const distance = document.getElementById('search-distance').value;
    const ordering = document.getElementById('search-ordering').value;

    if (city) params.city = city;
    if (type) params.parking_type = type;
    if (distance) params.distance = distance;
    if (ordering) params.ordering = ordering;

    loadParkings(params);
}

// --- Pagination ---

function changePage(direction) {
    currentPage += direction;
    searchParkings();
}

// --- Reserve ---

function openReserve(parkingId) {
    if (!isLoggedIn()) {
        openModal('modal-login');
        return;
    }
    document.getElementById('reserve-parking-id').value = parkingId;
    document.getElementById('reserve-error').style.display = 'none';
    document.getElementById('reserve-success').style.display = 'none';
    openModal('modal-reserve');
}

async function createReservation() {
    const errorEl = document.getElementById('reserve-error');
    const successEl = document.getElementById('reserve-success');

    const data = {
        parking_reservation: document.getElementById('reserve-parking-id').value,
        date_start: document.getElementById('reserve-start').value,
        date_end: document.getElementById('reserve-end').value,
        period_type: document.getElementById('reserve-period').value,
    };

    const response = await apiCreateReservation(data);
    const result = await response.json();

    if (response.ok) {
        // Show success message
        successEl.style.display = 'block';
        successEl.textContent = 'Reservation created successfully!';
        errorEl.style.display = 'none';
    } else {
        // Show error message
        errorEl.style.display = 'block';
        errorEl.textContent = result.message?.non_field_errors?.[0] || 'An error occurred.';
        successEl.style.display = 'none';
    }
}
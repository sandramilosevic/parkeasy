// --- On page load ---

document.addEventListener('DOMContentLoaded', () => {
    renderNavButtons();
    loadDashboard();
});

// --- Navbar ---

function renderNavButtons() {
    const nav = document.getElementById('nav-buttons');

    if (isLoggedIn()) {
        nav.innerHTML = `
            <a href="dashboard.html" class="btn btn-outline">My Parking</a>
            <button class="btn btn-primary" onclick="logout()">Logout</button>
        `;
    } else {
        nav.innerHTML = `
            <button class="btn btn-outline" onclick="window.location.href='index.html'">Login</button>
        `;
    }
}

function logout() {
    removeTokens();
    window.location.href = 'index.html';
}

// --- Load dashboard based on user type ---

async function loadDashboard() {
    if (!isLoggedIn()) {
        document.getElementById('not-logged-section').style.display = 'block';
        return;
    }

    const response = await apiFetch('/auth/users/me/');
    const user = await response.json();
    if (!user) return;

    if (user.user_type === 'driver') {
        document.getElementById('driver-section').style.display = 'block';
        loadReservations();
    } else if (user.user_type === 'owner') {
        document.getElementById('owner-section').style.display = 'block';
        loadOwnerParkings();
    }
}

// --- Driver: Load reservations ---

async function loadReservations() {
    const response = await apiGetReservations();
    const data = await response.json();

    const list = document.getElementById('reservations-list');

    if (!data || data.length === 0) {
        list.innerHTML = '<p style="color: var(--text-light)">You have no reservations yet.</p>';
        return;
    }

    list.innerHTML = data.map(r => `
        <div style="background: var(--white); border-radius: 12px; padding: 20px; margin-bottom: 16px; border: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="font-size: 16px; margin-bottom: 4px">${r.parking_reservation}</h3>
                <p style="color: var(--text-light); font-size: 13px">${formatDate(r.date_start)} - ${formatDate(r.date_end)}</p>
                <span class="badge" style="margin-top: 8px">${r.reservation_status}</span>
            </div>
            <div style="text-align: right">
                <p style="font-weight: 600; color: var(--blue-light); font-size: 16px">$${r.full_price}</p>
                <button class="btn btn-outline" style="margin-top: 8px; font-size: 12px" onclick="deleteReservation(${r.id})">Cancel</button>
            </div>
        </div>
    `).join('');
}

async function deleteReservation(id) {
    if (!confirm('Are you sure you want to cancel this reservation?')) return;

    const response = await apiDeleteReservation(id);

    if (response.ok) {
        loadReservations();
    }
}

// --- Owner: Load parkings ---

async function loadOwnerParkings() {
    const response = await apiGetParkings();
    const data = await response.json();

    const list = document.getElementById('owner-parkings');

    if (!data.results || data.results.length === 0) {
        list.innerHTML = '<p style="color: var(--text-light)">You have no parking spots yet.</p>';
        return;
    }

    list.innerHTML = data.results.map(p => `
        <div class="card">
            <h3>${p.title}</h3>
            <div class="price">$${p.price_per_hour} <span style="font-weight:400;font-size:13px;color:var(--text-light)">/hour</span></div>
            <div class="meta">${p.city} · ${p.address}</div>
            <button class="btn btn-outline" style="width:100%; margin-top: 14px; color: #c0392b; border-color: #c0392b" onclick="deleteParking(${p.id})">Delete</button>
        </div>
    `).join('');
}

async function createParking() {
    const errorEl = document.getElementById('parking-error');
    const successEl = document.getElementById('parking-success');

    const data = {
        title: document.getElementById('parking-title').value,
        city: document.getElementById('parking-city').value,
        address: document.getElementById('parking-address').value,
        parking_type: document.getElementById('parking-type').value,
        distance: document.getElementById('parking-distance').value,
        price_per_hour: document.getElementById('parking-price-hour').value,
        price_per_day: document.getElementById('parking-price-day').value,
        price_per_month: document.getElementById('parking-price-month').value,
        description: document.getElementById('parking-description').value,
        image: document.getElementById('parking-image').value,
    };

    const response = await apiCreateParking(data);
    const result = await response.json();

    if (response.ok) {
        // Show success and reload parkings
        successEl.style.display = 'block';
        successEl.textContent = 'Parking spot added successfully!';
        errorEl.style.display = 'none';
        loadOwnerParkings();
    } else {
        // Show error message
        errorEl.style.display = 'block';
        errorEl.textContent = JSON.stringify(result.message || result);
        successEl.style.display = 'none';
    }
}

async function deleteParking(id) {
    if (!confirm('Are you sure you want to delete this parking spot?')) return;

    const response = await apiDeleteParking(id);

    if (response.ok) {
        loadOwnerParkings();
    }
}

// --- Helper: Format date ---

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-GB') + ' ' + date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
}
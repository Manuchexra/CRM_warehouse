// ── Auth Check ────────────────────────────────────────────────────────────
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const isLoginPage = window.location.pathname.endsWith('index.html') || window.location.pathname === '/';
    if (!token && !isLoginPage) {
        window.location.href = 'index.html';
    }
}

function logout() {
    API.logout();
}

// ── Display user info ─────────────────────────────────────────────────────
function displayUserInfo() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const nameEl = document.getElementById('user-name');
    const roleEl = document.getElementById('user-role');
    const avatarEl = document.getElementById('user-avatar');

    const displayName = user.full_name || user.email?.split('@')[0] || 'Admin';
    const roleLabel = {
        admin: 'Administrator',
        sales_manager: 'Sotuv menejer',
        warehouse_manager: 'Ombor menejer',
        employee: 'Xodim'
    }[user.role] || user.role || '';

    if (nameEl) nameEl.textContent = displayName;
    if (roleEl) roleEl.textContent = roleLabel;
    if (avatarEl) avatarEl.textContent = displayName.charAt(0).toUpperCase();
}

// ── Status label helper ───────────────────────────────────────────────────
function statusBadge(status) {
    const map = {
        pending:    ['badge-warning', 'Kutilmoqda'],
        confirmed:  ['badge-muted',   'Tasdiqlangan'],
        processing: ['badge-muted',   'Jarayonda'],
        shipped:    ['badge-muted',   'Yuborildi'],
        delivered:  ['badge-success', 'Yetkazildi'],
        cancelled:  ['badge-danger',  'Bekor'],
    };
    const [cls, label] = map[status] || ['badge-muted', status];
    return `<span class="badge ${cls}">${label}</span>`;
}

// ── Format currency ───────────────────────────────────────────────────────
function formatMoney(n) {
    return '$' + parseFloat(n || 0).toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
}

// ── Format date ───────────────────────────────────────────────────────────
function formatDate(d) {
    if (!d) return '—';
    return new Date(d).toLocaleDateString('uz-UZ', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

// ── Modal helpers ─────────────────────────────────────────────────────────
function openModal(id) {
    const overlay = document.getElementById(id);
    if (overlay) overlay.classList.add('open');
}

function closeModal(id) {
    const overlay = document.getElementById(id);
    if (overlay) overlay.classList.remove('open');
}

// Close modal on overlay click
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('open');
    }
});

// ── DOMContentLoaded ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    displayUserInfo();
    if (window.lucide) lucide.createIcons();
});

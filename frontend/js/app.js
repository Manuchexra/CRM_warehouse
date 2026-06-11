// ── Role-based page access configuration ─────────────────────────────────
// Maps each page to the roles that are allowed to access it
const PAGE_ACCESS = {
    'dashboard.html': ['admin', 'sales_manager', 'warehouse_manager'],
    'crm.html':       ['admin', 'sales_manager', 'employee'],
    'erp.html':       ['admin', 'sales_manager', 'employee'],
    'wms.html':       ['admin', 'warehouse_manager', 'sales_manager', 'employee'],
};

// Navigation items with their icons and labels
const NAV_ITEMS = [
    { href: 'dashboard.html', icon: 'layout-dashboard', label: 'Dashboard' },
    { href: 'crm.html',       icon: 'users',            label: 'CRM – Mijozlar' },
    { href: 'erp.html',       icon: 'shopping-cart',     label: 'ERP – Buyurtmalar' },
    { href: 'wms.html',       icon: 'package',           label: 'WMS – Ombor' },
];

// ── Get current user role ─────────────────────────────────────────────────
function getUserRole() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    return user.role || '';
}

// ── Get current page filename ─────────────────────────────────────────────
function getCurrentPage() {
    const path = window.location.pathname;
    const parts = path.split('/');
    return parts[parts.length - 1] || 'index.html';
}

// ── Check if user has access to a page ────────────────────────────────────
function hasAccess(page, role) {
    if (!PAGE_ACCESS[page]) return true; // pages not in list are open
    return PAGE_ACCESS[page].includes(role);
}

// ── Get first allowed page for a role (for redirect) ──────────────────────
function getFirstAllowedPage(role) {
    for (const item of NAV_ITEMS) {
        if (hasAccess(item.href, role)) return item.href;
    }
    return 'index.html'; // fallback to login
}

// ── Auth Check ────────────────────────────────────────────────────────────
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const currentPage = getCurrentPage();
    const isLoginPage = currentPage === 'index.html' || currentPage === '' || window.location.pathname === '/';

    if (!token && !isLoginPage) {
        window.location.href = 'index.html';
        return;
    }

    // If logged in and on a page, check role-based access
    if (token && !isLoginPage) {
        const role = getUserRole();
        if (role && !hasAccess(currentPage, role)) {
            // User doesn't have access to this page — redirect to first allowed page
            const redirectPage = getFirstAllowedPage(role);
            showNotification('Bu sahifaga ruxsatingiz yo\'q', 'error');
            setTimeout(() => { window.location.href = redirectPage; }, 300);
            return;
        }
    }
}

function logout() {
    API.logout();
}

// ── Build sidebar navigation based on role ────────────────────────────────
function buildSidebarNav() {
    const navEl = document.getElementById('sidebar-nav');
    if (!navEl) return;

    const role = getUserRole();
    const currentPage = getCurrentPage();

    let html = '';
    for (const item of NAV_ITEMS) {
        if (hasAccess(item.href, role)) {
            const isActive = currentPage === item.href ? ' active' : '';
            html += `<a href="${item.href}" class="nav-link${isActive}">
                <i data-lucide="${item.icon}"></i> ${item.label}
            </a>`;
        }
    }

    navEl.innerHTML = html;
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

// ── Check if current user can perform write operations on a module ─────────
// Used by pages to hide create/edit/delete buttons for read-only users
function canWrite(module) {
    const role = getUserRole();
    const writePermissions = {
        crm: ['admin', 'sales_manager'],
        erp: ['admin', 'sales_manager'],
        wms: ['admin', 'warehouse_manager'],
    };
    return (writePermissions[module] || []).includes(role);
}

function canDelete(module) {
    const role = getUserRole();
    // Only admin can delete in all modules
    return role === 'admin';
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
    buildSidebarNav();
    displayUserInfo();
    if (window.lucide) lucide.createIcons();
});
